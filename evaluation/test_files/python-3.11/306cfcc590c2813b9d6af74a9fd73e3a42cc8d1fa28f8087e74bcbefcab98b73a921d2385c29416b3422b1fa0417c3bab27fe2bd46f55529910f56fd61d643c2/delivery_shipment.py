import collections
from odoo import fields
from odoo.addons.base_rest.components.service import to_bool, to_int
from odoo.addons.component.core import Component

class DeliveryShipment(Component):
    """Methods for the Delivery with Shipment Advices process

    Deliver the goods by processing the PACK and raw products by delivery order
    into a shipment advice.

    Multiple operators could be processing a same delivery order.

    You will find a sequence diagram describing states and endpoints
    relationships [here](../docs/delivery_shipment_diag_seq.png).
    Keep [the sequence diagram](../docs/delivery_shipment_diag_seq.plantuml)
    up-to-date if you change endpoints.

    Three cases:

    * Manager assign shipment advice to loading dock, plan its content and start them
    * Manager assign shipment advice to loading dock without content planning and start them
    * Operators create shipment advice on the fly (option “Allow shipment advice creation”
      in the scenario)

    Expected:

    * Existing packages are moved to customer location
    * Products are moved to customer location as raw products
    * Bin packed products are placed in new shipping package and shipped to customer
    * A shipment advice is marked as done
    """
    _inherit = 'base.shopfloor.process'
    _name = 'shopfloor.delivery.shipment'
    _usage = 'delivery_shipment'
    _description = __doc__

    def scan_dock(self, barcode, confirmation=False):
        """Scan a loading dock.

        Called at the beginning of the workflow to select the shipment advice
        (corresponding to the scanned loading dock) to work on.

        If no shipment advice in progress related to the scanned loading dock
        is found, a new one is created if the menu as the option
        "Allow to create shipment advice" enabled.

        Transitions:
        * scan_document: a shipment advice has been found or created (with or
          without planned moves)
        * scan_dock: no shipment advice found
        """
        search = self._actions_for('search')
        dock = search.dock_from_scan(barcode)
        if dock:
            shipment_advice = self._find_shipment_advice_from_dock(dock)
            if not shipment_advice:
                if not self.work.menu.allow_shipment_advice_create:
                    return self._response_for_scan_dock(message=self.msg_store.no_shipment_in_progress())
                if not confirmation:
                    return self._response_for_scan_dock(message=self.msg_store.scan_dock_again_to_confirm(dock), confirmation_required=True)
                shipment_advice = self._create_shipment_advice_from_dock(dock)
            return self._response_for_scan_document(shipment_advice)
        return self._response_for_scan_dock(message=self.msg_store.barcode_not_found())

    def scan_document(self, shipment_advice_id, barcode, picking_id=None):
        """Scan an operation, a package, a product or a lot.

        If an operation is scanned, reload the screen with the related planned
        content or full content of this operation for this shipment advice.

        If a package, a product or a lot is scanned, it will be loaded in the
        current shipment advice and the screen will be reloaded with the related
        operation listing its planned or full content.

        If all the planned content (if any) has been loaded, redirect the user
        to the next state 'loading_list'.

        Transitions:
        * scan_document: once a good is loaded, or a operation has been
          scanned, or in case of error
        * loading_list: all planned content (if any) have been processed
        * scan_dock: error (shipment not found...)
        """
        shipment_advice = self.env['shipment.advice'].browse(shipment_advice_id).exists()
        if not shipment_advice:
            return self._response_for_scan_dock(message=self.msg_store.record_not_found())
        picking = None
        if picking_id:
            picking = self.env['stock.picking'].browse(picking_id).exists()
            if not picking:
                return self._response_for_scan_document(shipment_advice, message=self.msg_store.stock_picking_not_found())
            message = self._check_picking_status(picking, shipment_advice)
            if message:
                return self._response_for_scan_document(shipment_advice, message=message)
        search = self._actions_for('search')
        scanned_picking = search.picking_from_scan(barcode)
        if scanned_picking:
            return self._scan_picking(shipment_advice, scanned_picking)
        scanned_package = search.package_from_scan(barcode)
        if scanned_package:
            return self._scan_package(shipment_advice, scanned_package)
        move_lines = self.env['stock.move.line'].search(self._find_move_lines_domain(shipment_advice))
        scanned_lot = search.lot_from_scan(barcode, products=move_lines.product_id)
        if scanned_lot:
            return self._scan_lot(shipment_advice, scanned_lot)
        scanned_product = search.product_from_scan(barcode)
        if scanned_product:
            return self._scan_product(shipment_advice, scanned_product, picking)
        return self._response_for_scan_document(shipment_advice, picking, message=self.msg_store.barcode_not_found())

    def _scan_picking(self, shipment_advice, picking):
        """Return the planned or available content of the scanned delivery for
        the current shipment advice.

        If the shipment advice had planned content and that the scanned delivery
        is not part of it, returns an error message.
        """
        message = self._check_picking_status(picking, shipment_advice)
        if message:
            return self._response_for_scan_document(shipment_advice, message=message)
        else:
            move_lines_to_process = self._find_move_lines_to_process_from_picking(shipment_advice, picking)
            if not move_lines_to_process:
                return self._response_for_scan_document(shipment_advice, message=self.msg_store.no_delivery_content_to_load(picking))
        return self._response_for_scan_document(shipment_advice, picking)

    def _scan_package(self, shipment_advice, package):
        """Load the package in the shipment advice.

        Find the package level or move line (of the planned shipment advice in
        priority if any) corresponding to the scanned package and load it.
        If no content is found an error will be returned.
        """
        move_lines = self._find_move_lines_from_package(shipment_advice, package)
        if move_lines:
            message = self._check_picking_status(move_lines.picking_id, shipment_advice)
            if message:
                return self._response_for_scan_document(shipment_advice, message=message)
            package_level = move_lines.package_level_id
            if package_level._is_loaded_in_shipment():
                return self._response_for_scan_document(shipment_advice, move_lines.picking_id, message=self.msg_store.package_already_loaded_in_shipment(package, shipment_advice))
            package_level._load_in_shipment(shipment_advice)
            return self._response_for_scan_document_or_loading_list(shipment_advice, move_lines.picking_id)
        message = self.msg_store.unable_to_load_package_in_shipment(package, shipment_advice)
        if shipment_advice.planned_move_ids:
            message = self.msg_store.package_not_planned_in_shipment(package, shipment_advice)
        return self._response_for_scan_document(shipment_advice, message=message)

    def _scan_lot(self, shipment_advice, lot):
        """Load the lot in the shipment advice.

        Find the first move line (of the planned shipment advice in
        priority if any) corresponding to the scanned lot and load it.
        If no move line is found an error will be returned.
        """
        move_lines = self._find_move_lines_from_lot(shipment_advice, lot)
        if move_lines:
            message = self._check_picking_status(move_lines.picking_id, shipment_advice)
            if message:
                return self._response_for_scan_document(shipment_advice, message=message)
            package_levels_not_loaded = move_lines.package_level_id.filtered(lambda pl: not pl.is_done)
            if package_levels_not_loaded:
                return self._response_for_scan_document(shipment_advice, move_lines.picking_id, message=self.msg_store.lot_owned_by_packages(package_levels_not_loaded.package_id))
            if move_lines._is_loaded_in_shipment():
                return self._response_for_scan_document(shipment_advice, move_lines.picking_id, message=self.msg_store.lot_already_loaded_in_shipment(lot, shipment_advice))
            move_lines._load_in_shipment(shipment_advice)
            return self._response_for_scan_document_or_loading_list(shipment_advice, move_lines.picking_id)
        message = self.msg_store.unable_to_load_lot_in_shipment(lot, shipment_advice)
        if shipment_advice.planned_move_ids:
            message = self.msg_store.lot_not_planned_in_shipment(lot, shipment_advice)
        return self._response_for_scan_document(shipment_advice, message=message)

    def _scan_product(self, shipment_advice, product, picking):
        """Load the product in the shipment advice.

        Find the first move line (of the planned shipment advice in
        priority if any) corresponding to the scanned product and load it.
        If no move line is found an error will be returned.
        """
        if not picking:
            return self._response_for_scan_document(shipment_advice, message=self.msg_store.scan_operation_first())
        move_lines = self._find_move_lines_from_product(shipment_advice, product, picking)
        if move_lines:
            message = self._check_picking_status(move_lines.picking_id, shipment_advice)
            if message:
                return self._response_for_scan_document(shipment_advice, message=message)
            package_levels_not_loaded = move_lines.package_level_id.filtered(lambda pl: not pl.is_done)
            if package_levels_not_loaded:
                return self._response_for_scan_document(shipment_advice, picking, message=self.msg_store.product_owned_by_packages(package_levels_not_loaded.package_id))
            if product.tracking != 'none':
                lots_not_loaded = move_lines.filtered(lambda ml: not ml.package_level_id and ml.qty_done != ml.product_uom_qty and ml.lot_id)
                if len(lots_not_loaded) > 1:
                    return self._response_for_scan_document(shipment_advice, picking, message=self.msg_store.product_owned_by_lots(lots_not_loaded.lot_id))
            if move_lines._is_loaded_in_shipment():
                return self._response_for_scan_document(shipment_advice, picking, message=self.msg_store.product_already_loaded_in_shipment(product, shipment_advice))
            move_lines._load_in_shipment(shipment_advice)
            return self._response_for_scan_document_or_loading_list(shipment_advice, move_lines.picking_id)
        message = self.msg_store.unable_to_load_product_in_shipment(product, shipment_advice)
        if shipment_advice.planned_move_ids:
            message = self.msg_store.product_not_planned_in_shipment(product, shipment_advice)
        return self._response_for_scan_document(shipment_advice, message=message)

    def unload_move_line(self, shipment_advice_id, move_line_id):
        """Unload a move line from a shipment advice.

        Transitions:
        * scan_document: reload the screen once the move line is unloaded
        * scan_dock: error (record ID not found...)
        """
        shipment_advice = self.env['shipment.advice'].browse(shipment_advice_id).exists()
        move_line = self.env['stock.move.line'].browse(move_line_id).exists()
        if not shipment_advice or not move_line:
            return self._response_for_scan_dock(message=self.msg_store.record_not_found())
        move_line._unload_from_shipment()
        return self._response_for_scan_document(shipment_advice, move_line.picking_id)

    def unload_package_level(self, shipment_advice_id, package_level_id):
        """Unload a package level from a shipment advice.

        Transitions:
        * scan_document: reload the screen once the package level is unloaded
        * scan_dock: error (record ID not found...)
        """
        shipment_advice = self.env['shipment.advice'].browse(shipment_advice_id).exists()
        package_level = self.env['stock.package_level'].browse(package_level_id).exists()
        if not shipment_advice or not package_level:
            return self._response_for_scan_dock(message=self.msg_store.record_not_found())
        package_level._unload_from_shipment()
        return self._response_for_scan_document(shipment_advice, package_level.picking_id)

    def loading_list(self, shipment_advice_id):
        """Redirect to the 'loading_list' state listing the loaded (with their
        loading progress) and not loaded deliveries for the given shipment.
        """
        shipment_advice = self.env['shipment.advice'].browse(shipment_advice_id).exists()
        if not shipment_advice:
            return self._response_for_scan_dock(message=self.msg_store.record_not_found())
        return self._response_for_loading_list(shipment_advice)

    def validate(self, shipment_advice_id, confirmation=False):
        """Validate the shipment advice.

        When called the first time with `confirmation=False`, it returns a summary
        of the deliveries (loaded or that can still be loaded) for that shipment.
        """
        shipment_advice = self.env['shipment.advice'].browse(shipment_advice_id).exists()
        if not shipment_advice:
            return self._response_for_scan_dock(message=self.msg_store.record_not_found())
        if not confirmation:
            return self._response_for_validate(shipment_advice)
        shipment_advice.action_done()
        return self._response_for_scan_dock(message=self.msg_store.shipment_validated(shipment_advice))

    def _response_for_scan_dock(self, message=None, confirmation_required=False):
        """Transition to the 'scan_dock' state.

        The client screen invite the user to scan a dock to find or create an
        available shipment advice.

        If `confirmation_required` is set, the client will ask to scan again
        the dock to create a shipment advice.
        """
        data = {'confirmation_required': confirmation_required}
        return self._response(next_state='scan_dock', data=data, message=message)

    def _response_for_scan_document(self, shipment_advice, picking=None, message=None):
        data = {'shipment_advice': self.data.shipment_advice(shipment_advice)}
        if picking:
            data.update(picking=self.data.picking(picking), content=self._data_for_content_to_load(shipment_advice, picking))
        return self._response(next_state='scan_document', data=data, message=message)

    def _response_for_loading_list(self, shipment_advice, message=None):
        data = {'shipment_advice': self.data.shipment_advice(shipment_advice), 'lading': self._data_for_lading(shipment_advice), 'on_dock': self._data_for_on_dock(shipment_advice)}
        return self._response(next_state='loading_list', data=data, message=message)

    def _response_for_scan_document_or_loading_list(self, shipment_advice, picking, message=None):
        """Route on 'scan_document' or 'loading_list' states.

        If all planned moves of the shipment are loaded, route to 'loading_list',
        state otherwise redirect to 'scan_document'.
        """
        planned_moves = shipment_advice.planned_move_ids
        loaded_move_lines = shipment_advice.loaded_move_line_ids
        if planned_moves and planned_moves.move_line_ids == loaded_move_lines:
            return self._response_for_loading_list(shipment_advice, message=self.msg_store.shipment_planned_content_fully_loaded())
        return self._response_for_scan_document(shipment_advice, picking, message=message)

    def _response_for_validate(self, shipment_advice, message=None):
        data = {'shipment_advice': self.data.shipment_advice(shipment_advice), 'lading': self._data_for_lading_summary(shipment_advice), 'on_dock': self._data_for_on_dock_summary(shipment_advice)}
        return self._response(next_state='validate', data=data, message=message)

    def _data_for_content_to_load(self, shipment_advice, picking):
        """Return a tuple list of dictionaries where keys are source locations
        and values are dictionaries listing package_levels and move_lines
        loaded or to load.

        E.g:
            {
                "SRC_LOCATION1": {
                    "package_levels": [{PKG_LEVEL_DATA}, ...],
                    "move_lines": [{MOVE_LINE_DATA}, ...],
                },
                "SRC_LOCATION2": {
                    ...
                },
            }
        """
        data = collections.OrderedDict()
        move_lines = self._find_move_lines_to_process_from_picking(shipment_advice, picking)
        package_level_ids = []
        for move_line in move_lines.sorted(lambda ml: ml.location_id.name):
            location_data = data.setdefault(move_line.location_id.name, {})
            if move_line.package_level_id:
                pl_data = location_data.setdefault('package_levels', [])
                if move_line.package_level_id.id in package_level_ids:
                    continue
                pl_data.append(self.data.package_level(move_line.package_level_id))
                package_level_ids.append(move_line.package_level_id.id)
            else:
                location_data.setdefault('move_lines', []).append(self.data.move_line(move_line))
        return data

    def _data_for_lading(self, shipment_advice):
        """Return a list of deliveries loaded in the shipment advice.

        The deliveries could be partially or fully loaded. For each of them a %
        of content loaded is computed (either based on bulk content or packages).
        """
        pickings = shipment_advice.loaded_picking_ids.filtered(lambda p: p.picking_type_id & self.picking_types).sorted('loaded_progress_f')
        return self.data.pickings_loaded(pickings)

    def _data_for_lading_summary(self, shipment_advice):
        """Return the number of deliveries/packages/bulk lines loaded."""
        pickings = shipment_advice.loaded_picking_ids.filtered(lambda p: p.picking_type_id & self.picking_types).sorted('loaded_progress_f')
        return {'loaded_pickings_count': len(pickings), 'loaded_packages_count': sum(pickings.mapped('loaded_packages_count')), 'total_packages_count': sum(pickings.mapped('total_packages_count')), 'loaded_bulk_lines_count': sum(pickings.mapped('loaded_move_lines_count')), 'total_bulk_lines_count': sum(pickings.mapped('total_move_lines_count')), 'loaded_weight': sum(pickings.mapped('loaded_weight'))}

    def _data_for_on_dock(self, shipment_advice):
        """Return a list of deliveries not loaded in the shipment advice.

        The deliveries are not loaded at all in the shipment.
        """
        return self.data.pickings(self._find_pickings_not_loaded_from_shipment(shipment_advice))

    def _data_for_on_dock_summary(self, shipment_advice):
        """Return the number of deliveries/packages/bulk lines not loaded."""
        pickings = self._find_pickings_not_loaded_from_shipment(shipment_advice)
        return {'total_pickings_count': len(pickings), 'total_packages_count': sum(pickings.mapped('total_packages_count')), 'total_bulk_lines_count': sum(pickings.mapped('total_move_lines_count'))}

    def _find_shipment_advice_from_dock_domain(self, dock):
        return [('dock_id', '=', dock.id), ('state', 'in', ['in_progress']), ('warehouse_id', 'in', self.picking_types.warehouse_id.ids)]

    def _find_shipment_advice_from_dock(self, dock):
        return self.env['shipment.advice'].search(self._find_shipment_advice_from_dock_domain(dock), limit=1, order='arrival_date')

    def _prepare_shipment_advice_from_dock_values(self, dock):
        return {'dock_id': dock.id, 'arrival_date': fields.Datetime.to_string(fields.Datetime.now()), 'warehouse_id': dock.warehouse_id.id}

    def _create_shipment_advice_from_dock(self, dock):
        shipment_advice = self.env['shipment.advice'].create(self._prepare_shipment_advice_from_dock_values(dock))
        shipment_advice.action_confirm()
        shipment_advice.action_in_progress()
        return shipment_advice

    def _find_move_lines_to_process_from_picking(self, shipment_advice, picking):
        """Returns the moves to load or unload for the given shipment and delivery.

        - if the shipment is planned, returns delivery content planned for
          this shipment
        - if the shipment is not planned, returns delivery content to
          load/unload (not planned and not loaded in another shipment)
        """
        picking.ensure_one()
        if shipment_advice.planned_move_ids:
            moves = (shipment_advice.planned_move_ids & picking.move_lines).filtered(lambda m: m.state in ('assigned', 'partially_available'))
        else:
            moves = picking.move_lines.filtered(lambda m: not m.shipment_advice_id)
        return moves.move_line_ids.filtered(lambda ml: not ml.shipment_advice_id or shipment_advice & ml.shipment_advice_id)

    def _find_move_lines_domain(self, shipment_advice):
        """Returns the base domain to look for move lines for a given shipment."""
        domain = [('state', 'in', ('assigned', 'partially_available')), ('picking_code', '=', 'outgoing'), ('picking_id.picking_type_id', 'in', self.picking_types.ids), '|', ('shipment_advice_id', '=', False), ('shipment_advice_id', '=', shipment_advice.id)]
        if shipment_advice.planned_move_ids:
            domain.append(('move_id.shipment_advice_id', '=', shipment_advice.id))
        else:
            domain.append(('move_id.shipment_advice_id', '=', False))
            if shipment_advice.carrier_ids:
                domain.extend(['|', ('picking_id.carrier_id.delivery_type', 'in', shipment_advice.carrier_ids.mapped('delivery_type')), ('picking_id.carrier_id', '=', False)])
        return domain

    def _find_move_lines_from_package(self, shipment_advice, package):
        """Returns the move line corresponding to `package` for the given shipment."""
        domain = self._find_move_lines_domain(shipment_advice)
        domain.append(('package_id', '=', package.id))
        return self.env['stock.move.line'].search(domain)

    def _find_move_lines_from_lot(self, shipment_advice, lot):
        """Returns the move line corresponding to `lot` for the given shipment."""
        domain = self._find_move_lines_domain(shipment_advice)
        domain.append(('lot_id', '=', lot.id))
        return self.env['stock.move.line'].search(domain)

    def _find_move_lines_from_product(self, shipment_advice, product, picking, in_package_not_loaded=False, in_lot=False):
        """Returns the move lines corresponding to `product` and `picking`
        for the given shipment.
        """
        domain = self._find_move_lines_domain(shipment_advice)
        domain.extend([('product_id', '=', product.id), ('picking_id', '=', picking.id)])
        if in_package_not_loaded:
            domain.append(('package_level_id', '!=', False), ('package_level_id.is_done', '=', False))
        if in_lot:
            domain.append(('lot_id', '!=', False))
        return self.env['stock.move.line'].search(domain)

    def _find_move_lines_not_loaded_from_shipment(self, shipment_advice):
        """Returns the move lines not loaded at all from the shipment advice."""
        domain = self._find_move_lines_domain(shipment_advice)
        domain.append(('qty_done', '=', 0))
        return self.env['stock.move.line'].search(domain)

    def _find_pickings_not_loaded_from_shipment(self, shipment_advice):
        """Returns the deliveries that are not loaded for the given shipment."""
        pickings_loaded = shipment_advice.loaded_picking_ids.filtered(lambda p: p.picking_type_id & self.picking_types)
        if shipment_advice.planned_move_ids:
            pickings_planned = shipment_advice.planned_picking_ids.filtered(lambda p: p.picking_type_id & self.picking_types)
            pickings_not_loaded = pickings_planned - pickings_loaded
        else:
            move_lines_not_loaded = self._find_move_lines_not_loaded_from_shipment(shipment_advice)
            pickings_not_loaded = move_lines_not_loaded.picking_id - shipment_advice.loaded_picking_ids
        return pickings_not_loaded

    def _check_picking_status(self, pickings, shipment_advice):
        message = super()._check_picking_status(pickings)
        if message:
            return message
        for picking in pickings:
            if shipment_advice.planned_move_ids:
                if picking not in shipment_advice.planned_picking_ids:
                    return self.msg_store.picking_not_planned_in_shipment(picking, shipment_advice)
            carriers = shipment_advice.carrier_ids
            shipment_carrier_types = set(carriers.mapped('delivery_type'))
            picking_carrier_type = {picking.carrier_id.delivery_type}
            if carriers and (not shipment_carrier_types & picking_carrier_type):
                return self.msg_store.carrier_not_allowed_by_shipment(picking)

class ShopfloorDeliveryShipmentValidator(Component):
    """Validators for the Delivery with Shipment Advices endpoints"""
    _inherit = 'base.shopfloor.validator'
    _name = 'shopfloor.delivery.shipment.validator'
    _usage = 'delivery_shipment.validator'

    def scan_dock(self):
        return {'barcode': {'required': True, 'type': 'string'}, 'confirmation': {'coerce': to_bool, 'required': False, 'nullable': True, 'type': 'boolean'}}

    def scan_document(self):
        return {'shipment_advice_id': {'coerce': to_int, 'required': True, 'type': 'integer'}, 'barcode': {'required': True, 'type': 'string'}, 'picking_id': {'coerce': to_int, 'required': False, 'nullable': True, 'type': 'integer'}}

    def unload_move_line(self):
        return {'shipment_advice_id': {'coerce': to_int, 'required': True, 'type': 'integer'}, 'move_line_id': {'coerce': to_int, 'required': True, 'type': 'integer'}}

    def unload_package_level(self):
        return {'shipment_advice_id': {'coerce': to_int, 'required': True, 'type': 'integer'}, 'package_level_id': {'coerce': to_int, 'required': True, 'type': 'integer'}}

    def loading_list(self):
        return {'shipment_advice_id': {'coerce': to_int, 'required': True, 'type': 'integer'}}

    def validate(self):
        return {'shipment_advice_id': {'coerce': to_int, 'required': True, 'type': 'integer'}, 'confirmation': {'coerce': to_bool, 'required': False, 'nullable': True, 'type': 'boolean'}}

class ShopfloorDeliveryShipmentValidatorResponse(Component):
    """Validators for the Delivery with Shipment Advices endpoints responses"""
    _inherit = 'base.shopfloor.validator.response'
    _name = 'shopfloor.delivery.shipment.validator.response'
    _usage = 'delivery_shipment.validator.response'
    _start_state = 'scan_dock'

    def _states(self):
        """List of possible next states

        With the schema of the data send to the client to transition
        to the next state.
        """
        return {'scan_dock': self._schema_scan_dock, 'scan_document': self._schema_scan_document, 'loading_list': self._schema_loading_list, 'validate': self._schema_validate}

    @property
    def _schema_scan_dock(self):
        return {'confirmation_required': {'type': 'boolean', 'nullable': True, 'required': False}}

    @property
    def _schema_scan_document(self):
        shipment_schema = self.schemas.shipment_advice()
        picking_schema = self.schemas.picking()
        return {'shipment_advice': {'type': 'dict', 'nullable': False, 'schema': shipment_schema}, 'picking': {'type': 'dict', 'nullable': True, 'schema': picking_schema}, 'content': {'type': 'dict', 'nullable': True}}

    @property
    def _schema_loading_list(self):
        shipment_schema = self.schemas.shipment_advice()
        picking_loaded_schema = self.schemas.picking_loaded()
        picking_schema = self.schemas.picking()
        return {'shipment_advice': self.schemas._schema_dict_of(shipment_schema), 'lading': self.schemas._schema_list_of(picking_loaded_schema), 'on_dock': self.schemas._schema_list_of(picking_schema)}

    @property
    def _schema_validate(self):
        shipment_schema = self.schemas.shipment_advice()
        shipment_lading_summary_schema = self.schemas.shipment_lading_summary()
        shipment_on_dock_summary_schema = self.schemas.shipment_on_dock_summary()
        return {'shipment_advice': {'type': 'dict', 'nullable': False, 'schema': shipment_schema}, 'lading': self.schemas._schema_dict_of(shipment_lading_summary_schema), 'on_dock': self.schemas._schema_dict_of(shipment_on_dock_summary_schema)}

    def scan_dock(self):
        return self._response_schema(next_states={'scan_document', 'scan_dock'})

    def scan_document(self):
        return self._response_schema(next_states={'scan_document', 'scan_dock', 'loading_list'})

    def loading_list(self):
        return self._response_schema(next_states={'loading_list', 'scan_dock'})

    def validate(self):
        return self._response_schema(next_states={'validate', 'scan_dock'})