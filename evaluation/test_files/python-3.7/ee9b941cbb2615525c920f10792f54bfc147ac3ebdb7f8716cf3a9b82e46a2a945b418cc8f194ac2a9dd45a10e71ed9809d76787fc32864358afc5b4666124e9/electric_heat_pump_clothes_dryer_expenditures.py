from policyengine_us.model_api import *

class electric_heat_pump_clothes_dryer_expenditures(Variable):
    value_type = float
    entity = TaxUnit
    label = 'Expenditures on electric heat pump clother dryers'
    unit = USD
    definition_period = YEAR
    reference = 'https://www.democrats.senate.gov/imo/media/doc/inflation_reduction_act_of_2022.pdf#page=585'