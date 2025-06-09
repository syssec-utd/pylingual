import re
from odoo import api, fields, models
from odoo.tools.safe_eval import safe_eval

def is_one_value(result):
    if type(result) is dict and 'value' in result.dictfetchone():
        return True
    elif type(result) is list and 'value' in result[0]:
        return True
    else:
        return False
RE_SELECT_QUERY = re.compile('.*(' + '|'.join(('INSERT', 'UPDATE', 'DELETE', 'CREATE', 'ALTER', 'DROP', 'GRANT', 'REVOKE', 'INDEX')) + ')')

def is_sql_or_ddl_statement(query):
    """Check if sql query is a SELECT statement"""
    return not RE_SELECT_QUERY.match(query.upper())

class KPIThresholdRange(models.Model):
    """
    KPI Threshold Range
    """
    _name = 'kpi.threshold.range'
    _description = 'KPI Threshold Range'

    @api.model
    def _selection_value_type(self):
        return [('static', 'Fixed value'), ('python', 'Python Code'), ('local', 'SQL - Local DB'), ('external', 'SQL - External DB')]
    name = fields.Char('Name', size=50, required=True)
    valid = fields.Boolean(string='Valid', required=True, compute='_compute_is_valid_range', default=True)
    invalid_message = fields.Char(string='Message', size=100, compute='_compute_is_valid_range')
    min_type = fields.Selection(selection='_selection_value_type', string='Min Type', required=True)
    min_value = fields.Float(string='Minimum Value', compute='_compute_min_value')
    min_fixed_value = fields.Float('Minimum Fixed Value')
    min_code = fields.Text('Minimum Computation Code')
    min_error = fields.Char('Minimum Error', compute='_compute_min_value')
    min_dbsource_id = fields.Many2one('base.external.dbsource', 'External DB Source Minimum')
    max_type = fields.Selection(selection='_selection_value_type', string='Max Type', required=True)
    max_value = fields.Float(string='Maximum Value', compute='_compute_max_value')
    max_fixed_value = fields.Float('Maximum Fixed Value')
    max_code = fields.Text('Maximum Computation Code')
    max_error = fields.Char('Maximum Error', compute='_compute_max_value')
    max_dbsource_id = fields.Many2one('base.external.dbsource', 'External DB Source Maximum')
    color = fields.Char(string='Color', help='Choose your color')
    threshold_ids = fields.Many2many('kpi.threshold', 'kpi_threshold_range_rel', 'range_id', 'threshold_id', 'Thresholds')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company)

    def _compute_min_value(self):
        for obj in self:
            value = None
            error = None
            try:
                if obj.min_type == 'local' and is_sql_or_ddl_statement(obj.min_code):
                    self.env.cr.execute(obj.min_code)
                    dic = self.env.cr.dictfetchall()
                    if is_one_value(dic):
                        value = dic[0]['value']
                elif obj.min_type == 'external' and obj.min_dbsource_id.id and is_sql_or_ddl_statement(obj.min_code):
                    dbsrc_obj = obj.min_dbsource_id
                    res = dbsrc_obj.execute(obj.min_code)
                    if is_one_value(res):
                        value = res[0]['value']
                elif obj.min_type == 'python':
                    value = safe_eval(obj.min_code)
                else:
                    value = obj.min_fixed_value
            except Exception as e:
                value = None
                error = str(e)
            obj.min_value = value
            obj.min_error = error

    def _compute_max_value(self):
        for obj in self:
            value = None
            error = None
            try:
                if obj.max_type == 'local' and is_sql_or_ddl_statement(obj.max_code):
                    self.env.cr.execute(obj.max_code)
                    dic = self.env.cr.dictfetchall()
                    if is_one_value(dic):
                        value = dic[0]['value']
                elif obj.max_type == 'external' and obj.max_dbsource_id.id and is_sql_or_ddl_statement(obj.max_code):
                    dbsrc_obj = obj.max_dbsource_id
                    res = dbsrc_obj.execute(obj.max_code)
                    if is_one_value(res):
                        value = res[0]['value']
                elif obj.max_type == 'python':
                    value = safe_eval(obj.max_code)
                else:
                    value = obj.max_fixed_value
            except Exception as e:
                value = None
                error = str(e)
            obj.max_value = value
            obj.max_error = error

    def _compute_is_valid_range(self):
        for obj in self:
            if obj.min_error or obj.max_error:
                obj.valid = False
                obj.invalid_message = 'Either minimum or maximum value has computation errors. Please fix them.'
            elif obj.max_value < obj.min_value:
                obj.valid = False
                obj.invalid_message = 'Minimum value is greater than the maximum value! Please adjust them.'
            else:
                obj.valid = True
                obj.invalid_message = ''