from policyengine_us.model_api import *

class recovery_rebate_credit(Variable):
    value_type = float
    entity = TaxUnit
    label = 'Recovery Rebate Credit'
    unit = USD
    definition_period = YEAR
    reference = 'https://www.law.cornell.edu/uscode/text/26/6428'
    adds = ['rrc_cares', 'rrc_caa', 'rrc_arpa']