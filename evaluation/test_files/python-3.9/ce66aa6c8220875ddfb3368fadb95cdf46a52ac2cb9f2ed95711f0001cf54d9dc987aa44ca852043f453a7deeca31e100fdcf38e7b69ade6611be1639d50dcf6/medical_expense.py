from openfisca_us.model_api import *

class medical_expense(Variable):
    value_type = float
    entity = Person
    label = 'Total medical expenses'
    unit = USD
    definition_period = YEAR
    formula = sum_of_variables(['health_insurance_premiums', 'medical_out_of_pocket_expenses'])