from policyengine_us.model_api import *

class is_wa_adult(Variable):
    value_type = bool
    entity = Person
    label = 'Is a working-age adult'
    definition_period = YEAR

    def formula(person, period, parameters):
        return ~person('is_child', period) & ~person('is_senior', period)