import datetime
from odoo import _, api, exceptions, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_round

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    default_start_date = fields.Date(string='Default Start Date', compute='_compute_default_start_date', readonly=False)
    default_end_date = fields.Date(string='Default End Date', compute='_compute_default_end_date', readonly=False)
    is_rental_order = fields.Boolean(string='Is Rental Order', compute='_compute_is_rental_order', store=True)

    @api.depends('order_line.start_date')
    def _compute_default_start_date(self):
        for order in self:
            dates = []
            so_lines = order.order_line
            if so_lines:
                for line in so_lines:
                    if line.start_date:
                        dates.append(line.start_date)
            if dates:
                order.update({'default_start_date': min(dates)})

    @api.depends('order_line.end_date')
    def _compute_default_end_date(self):
        for order in self:
            dates = []
            so_lines = order.order_line
            if so_lines:
                for line in so_lines:
                    if line.end_date:
                        dates.append(line.end_date)
            if dates:
                order.update({'default_end_date': max(dates)})

    @api.depends('type_id')
    def _compute_is_rental_order(self):
        try:
            rental_type = self.env['ir.model.data'].sudo().get_object('rental_base', 'rental_sale_type')
        except ValueError:
            for order in self:
                order.is_rental_order = False
            return
        for order in self:
            order.is_rental_order = False
            if order.type_id.id == rental_type.id:
                order.is_rental_order = True

    @api.multi
    def unlink(self):
        for rec in self:
            rentals = self.env['sale.rental'].search([('start_order_line_id', 'in', rec.order_line.ids)])
            rentals.unlink()
        return super().unlink()

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    rental_qty_uom = fields.Many2one(string='Product Unit of Measure', related='product_id.rented_product_id.uom_id')
    start_date = fields.Date(states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]})
    end_date = fields.Date(states={'draft': [('readonly', False)], 'sent': [('readonly', False)], 'sale': [('readonly', False)]})

    @api.constrains('rental_type', 'extension_rental_id', 'start_date', 'end_date', 'rental_qty', 'product_uom_qty', 'product_id')
    def _check_sale_line_rental(self):
        for line in self:
            if line.rental_type == 'rental_extension':
                if not line.extension_rental_id:
                    raise ValidationError(_('Missing "Rental to Extend" on the sale order line with rental service %s.') % line.product_id.name)
                if line.rental_qty != line.extension_rental_id.rental_qty:
                    raise ValidationError(_('On the sale order line with rental service %s, you are trying to extend a rental with a rental quantity (%s) that is different from the quantity of the original rental (%s). This is not supported.') % (line.product_id.name, line.rental_qty, line.extension_rental_id.rental_qty))
            if line.rental_type in ('new_rental', 'rental_extension'):
                if not line.product_id.rented_product_id:
                    raise ValidationError(_('On the "new rental" sale order line with product "%s", we should have a rental service product!') % line.product_id.name)
            elif line.sell_rental_id:
                if line.product_uom_qty != line.sell_rental_id.rental_qty:
                    raise ValidationError(_('On the sale order line with product %s you are trying to sell a rented product with a quantity (%s) that is different from the rented quantity (%s). This is not supported.') % (line.product_id.name, line.product_uom_qty, line.sell_rental_id.rental_qty))
    order_type = fields.Selection(string='Order Type', selection=[('normal', 'Normal'), ('rental', 'Rental')], compute='_compute_order_type', inverse='_inverse_order_type')

    @api.depends('rental')
    def _compute_order_type(self):
        for rec in self:
            rec.order_type = 'rental' if rec.rental else 'normal'

    def _inverse_order_type(self):
        for rec in self:
            rec.rental = rec.order_type == 'rental'

    @api.onchange('order_type')
    def _onchange_order_type(self):
        self.rental = self.order_type == 'rental'

    @api.multi
    def _prepare_invoice_line(self, qty):
        res = super()._prepare_invoice_line(qty)
        if self.product_id.income_analytic_account_id:
            res['account_analytic_id'] = self.product_id.income_analytic_account_id.id
        return res

    @api.model
    def _get_time_uom(self):
        uom_month = self.env.ref('rental_base.product_uom_month')
        uom_day = self.env.ref('uom.product_uom_day')
        uom_hour = self.env.ref('uom.product_uom_hour')
        return {'month': uom_month, 'day': uom_day, 'hour': uom_hour}

    @api.multi
    def _get_number_of_time_unit(self):
        self.ensure_one()
        number = False
        time_uoms = self._get_time_uom()
        if self.product_uom.id == time_uoms['day'].id:
            number = (self.end_date - self.start_date).days + 1
        elif self.product_uom.id == time_uoms['hour'].id:
            number = ((self.end_date - self.start_date).days + 1) * 8
        elif self.product_uom.id == time_uoms['month'].id:
            number = ((self.end_date - self.start_date).days + 1) / 30.4167
            number = float_round(number, precision_rounding=1)
        return number

    @api.multi
    def update_start_end_date(self, date_start, date_end):
        for line in self:
            update_date_start_later = False
            if date_start > line.end_date:
                update_date_start_later = True
            else:
                line.with_context(allow_write=True).start_date = date_start
            line.with_context(allow_write=True).end_date = date_end
            if update_date_start_later:
                line.with_context(allow_write=True).start_date = date_start
            datetime_start = fields.Datetime.to_datetime(date_start)
            datetime_end = fields.Datetime.to_datetime(date_end)
            if line.rental:
                rentals = self.env['sale.rental'].search([('start_order_line_id', '=', line.id), ('state', '!=', 'cancel'), ('out_move_id.state', '!=', 'cancel'), ('in_move_id.state', '!=', 'cancel')])
                if rentals and date_start:
                    rental = rentals[0]
                    date_move_out = fields.Date.to_date(rental.out_move_id.date_expected)
                    if date_start != date_move_out:
                        if rental.out_move_id.state not in ['draft', 'confirmed', 'waiting']:
                            raise exceptions.UserError(_('Outgoing shipment is in state %s. You cannot change the start date anymore.') % rental.out_move_id.state)
                        rental.out_move_id.date_expected = datetime_start
                if rentals and date_end:
                    rental = rentals[0]
                    date_move_in = fields.Date.to_date(rental.in_move_id.date_expected)
                    if date_end != date_move_in:
                        if rental.in_move_id.state not in ['draft', 'confirmed', 'waiting']:
                            raise exceptions.UserError(_('Incoming shipment is in state %s. You cannot change the end date anymore.') % rental.in_move_id.state)
                        rental.in_move_id.date_expected = datetime_end

    @api.multi
    def write(self, values):
        """
        Both fields start_date and end_date were made editable in state draft, sent and sale,
        in order to allow the creation of new sale order lines with start and end dates.
        However, it is forbidden to write the dates of already existing sale order lines.
        To update these existing line, the method 'update_start_end_date' should be called.
        :param values: dictionary
        :return: Boolean
        """
        for sol in self:
            if sol.order_id.state not in ('draft', 'sent'):
                messages = []
                if 'start_date' in values and (not self._context.get('allow_write', False)):
                    if isinstance(values['start_date'], str) and sol.start_date != datetime.datetime.strptime(values['start_date'], '%Y-%m-%d').date() or (isinstance(values['start_date'], datetime.date) and sol.start_date != values['start_date']):
                        messages.append(_("You are not allowed to change the 'start date' in an order line of a confirmed order."))
                if 'end_date' in values and (not self._context.get('allow_write', False)):
                    if isinstance(values['end_date'], str) and sol.end_date != datetime.datetime.strptime(values['end_date'], '%Y-%m-%d').date() or (isinstance(values['end_date'], datetime.date) and sol.end_date != values['end_date']):
                        messages.append(_("You are not allowed to change the 'end date' in an order line of a confirmed order."))
                if messages:
                    messages.append(_("\nOrder: %s\nLine with product: '%s'\n\nPlease use instead the button 'Update Times' in the order to correctly update the order line's times, its timeline entry, contract and its stock moves and pickings as required.") % (sol.order_id.name, sol.product_id.display_name))
                    raise exceptions.UserError('\n'.join(messages))
        return super(SaleOrderLine, self).write(values)