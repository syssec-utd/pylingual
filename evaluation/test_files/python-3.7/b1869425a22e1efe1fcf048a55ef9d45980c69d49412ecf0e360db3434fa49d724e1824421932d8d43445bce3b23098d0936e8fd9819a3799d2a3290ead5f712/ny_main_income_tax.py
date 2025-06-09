from openfisca_us.model_api import *

class ny_main_income_tax(Variable):
    value_type = float
    entity = TaxUnit
    label = 'NY main income tax (before credits and supplemental tax)'
    unit = USD
    definition_period = YEAR
    defined_for = StateCode.NY

    def formula(tax_unit, period, parameters):
        taxable_income = tax_unit('ny_taxable_income', period)
        filing_status = tax_unit('filing_status', period)
        status = filing_status.possible_values
        rates = parameters(period).gov.states.ny.tax.income.main
        single = rates.single
        joint = rates.joint
        hoh = rates.head_of_household
        widow = rates.widow
        separate = rates.separate
        return select([filing_status == status.SINGLE, filing_status == status.JOINT, filing_status == status.HEAD_OF_HOUSEHOLD, filing_status == status.WIDOW, filing_status == status.SEPARATE], [single.calc(taxable_income), joint.calc(taxable_income), hoh.calc(taxable_income), widow.calc(taxable_income), separate.calc(taxable_income)])