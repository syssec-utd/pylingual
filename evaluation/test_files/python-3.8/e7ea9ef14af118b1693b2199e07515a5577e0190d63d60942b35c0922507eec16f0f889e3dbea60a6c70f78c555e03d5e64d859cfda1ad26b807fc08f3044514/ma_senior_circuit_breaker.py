from openfisca_us.model_api import *

class ma_senior_circuit_breaker(Variable):
    value_type = float
    entity = TaxUnit
    label = 'MA Senior Circuit Breaker Credit'
    unit = USD
    definition_period = YEAR
    reference = 'https://www.mass.gov/info-details/mass-general-laws-c62-ss-6'
    defined_for = StateCode.MA

    def formula(tax_unit, period, parameters):
        scb = parameters(period).gov.states.ma.tax.income.credits.senior_circuit_breaker
        person = tax_unit.members
        age = person('age', period)
        is_dependent = person('is_tax_unit_dependent', period)
        aged = age >= scb.eligibility.min_age
        meets_age_condition = tax_unit.any(~is_dependent & aged)
        real_estate_tax = add(tax_unit, period, ['real_estate_taxes'])
        rent = add(tax_unit, period, ['rent'])
        equivalent_rent = rent * scb.amount.rent_tax_share
        real_estate_tax_or_equiv = real_estate_tax + equivalent_rent
        income = tax_unit('ma_scb_total_income', period)
        income_threshold = income * scb.amount.min_real_estate_tax
        ret_over_threshold = max_(0, real_estate_tax_or_equiv - income_threshold)
        max_payment = min_(ret_over_threshold, scb.amount.max)
        filing_status = tax_unit('filing_status', period)
        meets_max_income_condition = income <= scb.eligibility.max_income[filing_status]
        assessed_value = add(tax_unit, period, ['assessed_property_value'])
        meets_max_property_value_condition = assessed_value <= scb.eligibility.max_property_value
        eligible = meets_age_condition & meets_max_income_condition & meets_max_property_value_condition
        return eligible * max_payment