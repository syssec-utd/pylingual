from odoo import models, _
from odoo.exceptions import ValidationError

class ContractIbanChangeWizard(models.TransientModel):
    _name = 'contract.iban.change.force.wizard'
    _inherit = 'contract.iban.change.wizard'

    def enqueue_OC_iban_update(self):
        self.env['contract.contract'].with_delay().update_subscription_force(self.contract_ids, 'iban')

    def button_change(self):
        if len(self.contract_ids) > 1:
            raise ValidationError(_('Only one contract is allowed in Contract Iban Change Force Wizard'))
        return super().button_change()