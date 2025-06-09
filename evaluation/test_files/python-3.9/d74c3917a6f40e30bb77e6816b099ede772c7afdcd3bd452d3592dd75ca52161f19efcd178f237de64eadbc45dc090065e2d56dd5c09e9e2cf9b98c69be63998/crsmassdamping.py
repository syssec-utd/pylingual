from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from sima.sima.blueprints.moao import MOAOBlueprint

class CRSMassDampingBlueprint(MOAOBlueprint):
    """"""

    def __init__(self, name='CRSMassDamping', package_path='sima/riflex', description=''):
        super().__init__(name, package_path, description)
        self.attributes.append(Attribute('_id', 'string', '', default=''))
        self.attributes.append(BlueprintAttribute('scriptableValues', 'sima/sima/ScriptableValue', '', True, Dimension('*')))
        self.attributes.append(Attribute('axialFactor', 'number', 'Factor for mass proportional damping in axial dof', default=0.0))
        self.attributes.append(Attribute('torsionalFactor', 'number', 'Factor for mass proportional damping in torsional dof', default=0.0))
        self.attributes.append(Attribute('bendingFactor', 'number', 'Factor for mass proportional damping in bending dof', default=0.0))