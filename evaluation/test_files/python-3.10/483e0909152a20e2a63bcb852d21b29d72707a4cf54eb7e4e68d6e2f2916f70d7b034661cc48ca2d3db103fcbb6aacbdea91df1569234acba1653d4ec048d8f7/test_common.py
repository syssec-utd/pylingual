from odoo.tests import Form, common

class TestsCommon(common.SavepointCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.location_obj = cls.env['stock.location']
        product_obj = cls.env['product.product']
        cls.wizard_obj = cls.env['wiz.stock.move.location']
        cls.quant_obj = cls.env['stock.quant']
        cls.company = cls.env.ref('base.main_company')
        cls.internal_loc_1 = cls.location_obj.create({'name': 'INT_1', 'usage': 'internal', 'active': True, 'company_id': cls.company.id})
        cls.internal_loc_2 = cls.location_obj.create({'name': 'INT_2', 'usage': 'internal', 'active': True, 'company_id': cls.company.id})
        cls.internal_loc_2_shelf = cls.location_obj.create({'name': 'Shelf', 'usage': 'internal', 'active': True, 'company_id': cls.company.id, 'location_id': cls.internal_loc_2.id})
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.product_no_lots = product_obj.create({'name': 'Pineapple', 'type': 'product', 'tracking': 'none'})
        cls.product_lots = product_obj.create({'name': 'Apple', 'type': 'product', 'tracking': 'lot'})
        cls.lot1 = cls.env['stock.production.lot'].create({'name': 'lot1', 'product_id': cls.product_lots.id, 'company_id': cls.company.id})
        cls.lot2 = cls.env['stock.production.lot'].create({'name': 'lot2', 'product_id': cls.product_lots.id, 'company_id': cls.company.id})
        cls.lot3 = cls.env['stock.production.lot'].create({'name': 'lot3', 'product_id': cls.product_lots.id, 'company_id': cls.company.id})

    def setup_product_amounts(self):
        self.set_product_amount(self.product_no_lots, self.internal_loc_1, 123)
        self.set_product_amount(self.product_lots, self.internal_loc_1, 1.0, lot_id=self.lot1)
        self.set_product_amount(self.product_lots, self.internal_loc_1, 1.0, lot_id=self.lot2)
        self.set_product_amount(self.product_lots, self.internal_loc_1, 1.0, lot_id=self.lot3)

    def set_product_amount(self, product, location, amount, lot_id=None):
        self.env['stock.quant']._update_available_quantity(product, location, amount, lot_id=lot_id)

    def check_product_amount(self, product, location, amount, lot_id=None):
        self.assertEqual(self.env['stock.quant']._get_available_quantity(product, location, lot_id=lot_id), amount)

    def _create_wizard(self, origin_location, destination_location):
        move_location_wizard = self.env['wiz.stock.move.location']
        return move_location_wizard.create({'origin_location_id': origin_location.id, 'destination_location_id': destination_location.id})

    def _create_picking(self, picking_type):
        with Form(self.env['stock.picking']) as picking_form:
            picking_form.picking_type_id = picking_type
        return picking_form.save()

    def _create_putaway_for_product(self, product, loc_in, loc_out):
        putaway = self.env['stock.putaway.rule'].create({'product_id': product.id, 'location_in_id': loc_in.id, 'location_out_id': loc_out.id})
        loc_in.write({'putaway_rule_ids': [(4, putaway.id, 0)]})