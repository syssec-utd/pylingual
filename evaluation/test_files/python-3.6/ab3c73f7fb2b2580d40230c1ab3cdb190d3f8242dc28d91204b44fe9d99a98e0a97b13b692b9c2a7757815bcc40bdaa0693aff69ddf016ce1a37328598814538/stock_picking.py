from odoo import models

class StockPicking(models.Model):
    _name = 'stock.picking'
    _inherit = ['stock.picking', 'l10n.ro.mixin']

    def _is_dropshipped(self):
        if not self.is_l10n_ro_record:
            return False
        self.ensure_one()
        return self.location_id.usage == 'supplier' and self.location_dest_id.usage == 'customer'

    def _is_dropshipped_returned(self):
        if not self.is_l10n_ro_record:
            return super()._is_dropshipped()
        self.ensure_one()
        return self.location_id.usage == 'customer' and self.location_dest_id.usage == 'supplier'