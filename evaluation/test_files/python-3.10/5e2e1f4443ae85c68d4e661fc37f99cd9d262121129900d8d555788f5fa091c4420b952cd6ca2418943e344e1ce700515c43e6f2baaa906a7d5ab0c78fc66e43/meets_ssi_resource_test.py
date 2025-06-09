from policyengine_us.model_api import *
from policyengine_core.simulations import Simulation

class meets_ssi_resource_test(Variable):
    value_type = bool
    entity = Person
    label = 'Meets SSI resource test'
    unit = USD
    definition_period = YEAR

    def formula(person, period, parameters):
        simulation: Simulation = person.simulation
        if hasattr(simulation, 'dataset'):
            pass_rate = parameters(period).gov.ssa.ssi.eligibility.resources.pass_rate
            return random(person) < pass_rate
        joint_claim = person('ssi_claim_is_joint', period)
        personal_resources = person('ssi_countable_resources', period)
        countable_resources = where(joint_claim, person.marital_unit.sum(personal_resources), personal_resources)
        ssi = parameters(period).gov.ssa.ssi
        resource_limits = ssi.eligibility.resources.limit
        resource_limit = where(joint_claim, resource_limits.couple, resource_limits.individual)
        return countable_resources <= resource_limit