import base64
import json
from odoo import api, fields, models

class SpreadsheetDashboard(models.Model):
    _name = 'spreadsheet.dashboard'
    _inherit = ['spreadsheet.dashboard', 'spreadsheet.abstract']
    spreadsheet_raw = fields.Serialized(inverse='_inverse_spreadsheet_raw', compute='_compute_spreadsheet_raw')

    @api.depends('data')
    def _compute_spreadsheet_raw(self):
        for dashboard in self:
            if dashboard.data:
                dashboard.spreadsheet_raw = json.loads(base64.decodebytes(dashboard.data).decode('UTF-8'))
            else:
                dashboard.spreadsheet_raw = {}

    def _inverse_spreadsheet_raw(self):
        for record in self:
            record.data = base64.encodebytes(json.dumps(record.spreadsheet_raw).encode('UTF-8'))