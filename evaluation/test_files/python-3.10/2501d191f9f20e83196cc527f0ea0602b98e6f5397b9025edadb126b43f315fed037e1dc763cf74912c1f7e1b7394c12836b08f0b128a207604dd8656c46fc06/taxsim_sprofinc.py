from policyengine_us.model_api import *

class taxsim_sprofinc(Variable):
    value_type = float
    entity = TaxUnit
    label = 'SSTB income for the spouse of the taxpayer (TAXSIM). Assumed zero.'
    unit = USD
    definition_period = YEAR