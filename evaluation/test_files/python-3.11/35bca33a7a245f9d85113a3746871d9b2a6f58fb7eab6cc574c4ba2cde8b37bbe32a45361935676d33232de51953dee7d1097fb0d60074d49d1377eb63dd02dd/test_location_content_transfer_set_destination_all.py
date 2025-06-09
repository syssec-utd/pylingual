from .test_location_content_transfer_base import LocationContentTransferCommonCase

class LocationContentTransferSetDestinationAllCase(LocationContentTransferCommonCase):
    """Tests for endpoint used from scan_destination_all

    * /set_destination_all
    * /go_to_single

    """

    @classmethod
    def setUpClassBaseData(cls):
        super().setUpClassBaseData()
        products = cls.product_a + cls.product_b + cls.product_c + cls.product_d
        for product in products:
            cls.env['stock.putaway.rule'].sudo().create({'product_id': product.id, 'location_in_id': cls.stock_location.id, 'location_out_id': cls.shelf1.id})
        cls.picking1 = picking1 = cls._create_picking(lines=[(cls.product_a, 10), (cls.product_b, 10)])
        cls.picking2 = picking2 = cls._create_picking(lines=[(cls.product_c, 10), (cls.product_d, 10)])
        cls.pickings = picking1 | picking2
        cls._fill_stock_for_moves(picking1.move_lines, in_package=True, location=cls.content_loc)
        cls._fill_stock_for_moves(picking2.move_lines, location=cls.content_loc)
        cls.pickings.action_assign()
        cls._simulate_pickings_selected(cls.pickings)

    def assert_all_done(self, destination):
        self.assertRecordValues(self.pickings, [{'state': 'done'}, {'state': 'done'}])
        self.assertRecordValues(self.pickings.move_line_ids, [{'qty_done': 10.0, 'state': 'done', 'location_dest_id': destination.id}, {'qty_done': 10.0, 'state': 'done', 'location_dest_id': destination.id}, {'qty_done': 10.0, 'state': 'done', 'location_dest_id': destination.id}, {'qty_done': 10.0, 'state': 'done', 'location_dest_id': destination.id}])
        self.assertRecordValues(self.picking1.package_level_ids, [{'is_done': True, 'state': 'done', 'location_dest_id': destination.id}])

    def test_set_destination_all_dest_location_ok(self):
        """Scanned destination location valid, moves set to done accepted"""
        sub_shelf1 = self.env['stock.location'].sudo().create({'name': 'Sub Shelf 1', 'barcode': 'subshelf1', 'location_id': self.shelf1.id})
        response = self.service.dispatch('set_destination_all', params={'location_id': self.content_loc.id, 'barcode': sub_shelf1.barcode})
        self.assert_response_start(response, message=self.service.msg_store.location_content_transfer_complete(self.content_loc, sub_shelf1))
        self.assert_all_done(sub_shelf1)

    def test_set_destination_all_with_partially_available_move_without_ancestor(self):
        """Scanned destination location valid, but one of the move to process
        is partially available and has no ancestor move.

        In such case, normal backorder is created with the remaining qty while
        the current pickings is validated.
        """
        self.picking2.do_unreserve()
        self._update_qty_in_location(self.content_loc, self.product_d, 5)
        self.picking2.action_assign()
        self._simulate_pickings_selected(self.picking2)
        move_d = self.picking2.move_lines.filtered(lambda m: m.product_id == self.product_d)
        sub_shelf1 = self.env['stock.location'].sudo().create({'name': 'Sub Shelf 1', 'barcode': 'subshelf1', 'location_id': self.shelf1.id})
        response = self.service.dispatch('set_destination_all', params={'location_id': self.content_loc.id, 'barcode': sub_shelf1.barcode})
        self.assert_response_start(response, message=self.service.msg_store.location_content_transfer_complete(self.content_loc, sub_shelf1))
        self.assertEqual(self.picking2.state, 'done')
        self.assertEqual(move_d.state, 'done')
        self.assertEqual(move_d.product_qty, 5)
        self.assertTrue(self.picking2.backorder_ids)
        self.assertNotEqual(self.picking2.backorder_ids.state, 'done')
        self.assertFalse(self.picking2.backorder_ids.user_id)
        self.assertEqual(self.picking2.backorder_ids.move_lines.product_qty, 5)

    def test_set_destination_all_with_partially_available_move_with_ancestor(self):
        """Scanned destination location valid, but one of the move to process
        is partially available and has an unprocessed ancestor move.

        In such case, new picking is created to validate the moves, and the
        remaining qties stay in their current picking.
        """
        self.picking2.do_unreserve()
        self._update_qty_in_location(self.content_loc, self.product_d, 5)
        self.picking2.action_assign()
        self._simulate_pickings_selected(self.picking2)
        move_d = self.picking2.move_lines.filtered(lambda m: m.product_id == self.product_d)
        move_d.move_orig_ids |= move_d.copy({'picking_id': False})
        sub_shelf1 = self.env['stock.location'].sudo().create({'name': 'Sub Shelf 1', 'barcode': 'subshelf1', 'location_id': self.shelf1.id})
        response = self.service.dispatch('set_destination_all', params={'location_id': self.content_loc.id, 'barcode': sub_shelf1.barcode})
        self.assert_response_start(response, message=self.service.msg_store.location_content_transfer_complete(self.content_loc, sub_shelf1))
        self.assertEqual(self.picking2.state, 'waiting')
        self.assertEqual(self.picking2.move_lines.state, 'waiting')
        self.assertEqual(self.picking2.move_lines.product_qty, 5)
        self.assertEqual(self.picking2.backorder_ids.state, 'done')
        self.assertEqual(move_d.state, 'done')
        self.assertEqual(move_d.product_qty, 5)

    def test_set_destination_all_dest_location_ok_with_completion_info(self):
        """Scanned destination location valid, moves set to done accepted
        and completion info is returned as the next transfer is ready.
        """
        move = self.picking1.move_lines[0]
        next_move = move.copy({'location_id': move.location_dest_id.id, 'location_dest_id': self.customer_location.id, 'move_orig_ids': [(6, 0, move.ids)]})
        next_move._action_confirm(merge=False)
        next_move._assign_picking()
        self.assertEqual(next_move.state, 'waiting')
        sub_shelf1 = self.env['stock.location'].sudo().create({'name': 'Sub Shelf 1', 'barcode': 'subshelf1', 'location_id': self.shelf1.id})
        move_lines = self.service._find_transfer_move_lines(self.content_loc)
        response = self.service.dispatch('set_destination_all', params={'location_id': self.content_loc.id, 'barcode': sub_shelf1.barcode})
        self.assertEqual(next_move.state, 'assigned')
        completion_info = self.service._actions_for('completion.info')
        completion_info_popup = completion_info.popup(move_lines)
        self.assert_response_start(response, message=self.service.msg_store.location_content_transfer_complete(self.content_loc, sub_shelf1), popup=completion_info_popup)

    def test_set_destination_all_dest_location_not_found(self):
        """Barcode scanned for destination location is not found"""
        response = self.service.dispatch('set_destination_all', params={'location_id': self.content_loc.id, 'barcode': 'NOT_FOUND'})
        self.assert_response_scan_destination_all(response, self.pickings, message=self.service.msg_store.barcode_not_found())

    def test_set_destination_all_dest_location_need_confirm(self):
        """Scanned dest. location != child but in picking type location

        So it needs confirmation.
        """
        response = self.service.dispatch('set_destination_all', params={'location_id': self.content_loc.id, 'barcode': self.shelf2.barcode})
        self.assert_response_scan_destination_all(response, self.pickings, message=self.service.msg_store.need_confirmation(), confirmation_required=True)

    def test_set_destination_all_dest_location_confirmation(self):
        """Scanned dest. location != child but in picking type location: confirm

        use the confirmation flag to confirm
        """
        response = self.service.dispatch('set_destination_all', params={'location_id': self.content_loc.id, 'barcode': self.shelf2.barcode, 'confirmation': True})
        self.assert_response_start(response, message=self.service.msg_store.location_content_transfer_complete(self.content_loc, self.shelf2))
        self.assert_all_done(self.shelf2)

    def test_set_destination_all_dest_location_invalid(self):
        """The scanned destination location is not in the menu's picking types"""
        response = self.service.dispatch('set_destination_all', params={'location_id': self.content_loc.id, 'barcode': self.dispatch_location.barcode})
        self.assert_response_scan_destination_all(response, self.pickings, message=self.service.msg_store.dest_location_not_allowed())

    def test_set_destination_all_dest_location_move_invalid(self):
        """The scanned destination location is not in the picking and move's
        dest location
        """
        self.pickings.move_lines[0].location_dest_id = self.shelf1
        self.pickings[0].location_dest_id = self.shelf1
        response = self.service.dispatch('set_destination_all', params={'location_id': self.content_loc.id, 'barcode': self.shelf2.barcode})
        self.assert_response_scan_destination_all(response, self.pickings, message=self.service.msg_store.dest_location_not_allowed())

    def test_go_to_single(self):
        """User used to 'split by lines' button to process line per line"""
        response = self.service.dispatch('go_to_single', params={'location_id': self.content_loc.id})
        self.assert_response_start_single(response, self.pickings)

class LocationContentTransferSetDestinationAllSpecialCase(LocationContentTransferCommonCase):
    """Tests for endpoint used from scan_destination_all (special cases without setup)

    * /set_destination_all
    * /go_to_single

    """

    def test_go_to_single_no_lines_to_process(self):
        """User used to 'split by lines' button to process line per line,
        but no lines to process.
        """
        response = self.service.dispatch('go_to_single', params={'location_id': self.content_loc.id})
        self.assert_response_start(response, message=self.service.msg_store.no_lines_to_process())