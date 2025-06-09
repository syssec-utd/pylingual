from openfisca_us.model_api import *

class is_ccdf_initial_income_eligible(Variable):
    value_type = bool
    entity = SPMUnit
    definition_period = YEAR
    label = 'Initial income eligibility for CCDF'