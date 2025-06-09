from openfisca_us.model_api import *

class ny_exemptions(Variable):
    value_type = float
    entity = TaxUnit
    label = 'NY exemptions'
    unit = USD
    definition_period = YEAR
    reference = 'https://www.nysenate.gov/legislation/laws/TAX/616'
    defined_for = StateCode.NY

    def formula(tax_unit, period, parameters):
        count_dependents = tax_unit('tax_unit_count_dependents', period)
        dependent_exemption = parameters(period).gov.states.ny.tax.income.exemptions.dependent
        return dependent_exemption * count_dependents