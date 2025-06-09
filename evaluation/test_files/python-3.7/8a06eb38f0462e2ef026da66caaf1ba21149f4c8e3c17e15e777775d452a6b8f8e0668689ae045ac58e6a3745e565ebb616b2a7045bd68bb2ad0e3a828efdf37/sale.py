from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    order_sequence = fields.Boolean(string='Order Sequence', readonly=True, index=True)
    quote_id = fields.Many2one('sale.order', string='Quotation', readonly=True, ondelete='restrict', copy=False, help='For Sales Order, this field references to its Quotation')
    order_id = fields.Many2one('sale.order', string='Order', readonly=True, ondelete='restrict', copy=False, help='For Quotation, this field references to its Sales Order')
    quotation_state = fields.Selection([('draft', 'Draft'), ('sent', 'Mail Sent'), ('cancel', 'Cancelled'), ('done', 'Done')], string='Quotation Status', readonly=True, related='state', help='Only relative quotation states')

    @api.model
    def create(self, vals):
        order_sequence = vals.get('order_sequence') or self.env.context.get('order_sequence')
        if not order_sequence and vals.get('name', '/') == '/':
            vals['name'] = self.env['ir.sequence'].next_by_code('sale.quotation') or '/'
        return super().create(vals)

    def _prepare_order_from_quotation(self):
        return {'name': self.env['ir.sequence'].next_by_code('sale.order') or '/', 'order_sequence': True, 'quote_id': self.id, 'client_order_ref': self.client_order_ref}

    def action_convert_to_order(self):
        self.ensure_one()
        if self.order_sequence:
            raise UserError(_('Only quotation can convert to order'))
        order = self.copy(self._prepare_order_from_quotation())
        self.order_id = order.id
        if self.state == 'draft':
            self.action_done()
        return self.open_duplicated_sale_order()

    @api.model
    def open_duplicated_sale_order(self):
        return {'name': _('Sales Order'), 'view_mode': 'form', 'view_id': False, 'res_model': 'sale.order', 'context': {'default_order_sequence': True, 'order_sequence': True}, 'type': 'ir.actions.act_window', 'nodestroy': True, 'target': 'current', 'domain': "[('order_sequence', '=', True)]", 'res_id': self.order_id and self.order_id.id or False}