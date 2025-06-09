from odoo import models, fields, api

class SaleOrderCancel(models.TransientModel):
    """ Ask a reason for the sale order cancellation."""
    _name = 'sale.order.cancel'
    _description = __doc__
    reason_id = fields.Many2one('sale.order.cancel.reason', string='Reason', required=True)

    @api.multi
    def confirm_cancel(self):
        self.ensure_one()
        act_close = {'type': 'ir.actions.act_window_close'}
        sale_ids = self._context.get('active_ids')
        if sale_ids is None:
            return act_close
        assert len(sale_ids) == 1, 'Only 1 sale ID expected'
        sale = self.env['sale.order'].browse(sale_ids)
        sale.cancel_reason_id = self.reason_id.id
        sale.action_cancel()
        return act_close