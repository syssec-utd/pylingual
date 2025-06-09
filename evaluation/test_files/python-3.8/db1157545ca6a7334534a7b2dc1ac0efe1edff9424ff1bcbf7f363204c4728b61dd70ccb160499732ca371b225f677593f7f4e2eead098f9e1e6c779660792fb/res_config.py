from odoo import fields, models

class ResConfig(models.TransientModel):
    _inherit = 'res.config.settings'
    employee_timesheet_cost_policy = fields.Selection(related='company_id.employee_timesheet_cost_policy', readonly=False)
    use_manual_employee_timesheet_cost = fields.Boolean(related='company_id.use_manual_employee_timesheet_cost', readonly=False)