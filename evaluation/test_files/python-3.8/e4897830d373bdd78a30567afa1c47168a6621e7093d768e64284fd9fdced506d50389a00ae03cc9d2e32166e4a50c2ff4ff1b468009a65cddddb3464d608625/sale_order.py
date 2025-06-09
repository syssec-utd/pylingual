import json
from odoo import api, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.tax_id', 'order_line.price_unit', 'amount_total', 'amount_untaxed')
    def _compute_tax_totals_json(self):

        def compute_taxes(order_line):
            price = 0.0
            if order_line.discounting_type == 'additive':
                total_discount = order_line.discount + order_line.discount2 + order_line.discount3
                price = order_line.price_unit * (1 - total_discount / 100.0)
            elif order_line.discounting_type == 'multiplicative':
                price = order_line.price_unit * (1 - (order_line.discount or 0.0) / 100.0)
                price = price * (1 - (order_line.discount2 or 0.0) / 100.0)
                price = price * (1 - (order_line.discount3 or 0.0) / 100.0)
                order = order_line.order_id
            order = order_line.order_id
            return order_line.tax_id._origin.compute_all(price, order.currency_id, order_line.product_uom_qty, product=order_line.product_id, partner=order.partner_shipping_id)
        vals = super()._compute_tax_totals_json()
        for order in self.filtered(lambda a: any((line.discount2 or line.discount3 for line in a.order_line))):
            account_move = self.env['account.move']
            tax_lines_data = account_move._prepare_tax_lines_data_for_totals_from_object(order.order_line, compute_taxes)
            tax_totals = account_move._get_tax_totals(order.partner_id, tax_lines_data, order.amount_total, order.amount_untaxed, order.currency_id)
            order.tax_totals_json = json.dumps(tax_totals)
        return vals

    @api.depends('order_line.price_total')
    def _amount_all(self):
        prev_values = dict()
        for order in self:
            prev_values.update(order.order_line.triple_discount_preprocess())
        res = super()._amount_all()
        self.env['sale.order.line'].triple_discount_postprocess(prev_values)
        return res