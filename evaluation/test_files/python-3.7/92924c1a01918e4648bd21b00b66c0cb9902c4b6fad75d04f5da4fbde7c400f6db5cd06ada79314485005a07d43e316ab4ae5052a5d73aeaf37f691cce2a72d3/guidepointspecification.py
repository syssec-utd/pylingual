from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from sima.sima.blueprints.moao import MOAOBlueprint

class GuidePointSpecificationBlueprint(MOAOBlueprint):
    """"""

    def __init__(self, name='GuidePointSpecification', package_path='sima/simo', description=''):
        super().__init__(name, package_path, description)
        self.attributes.append(Attribute('_id', 'string', '', default=''))
        self.attributes.append(BlueprintAttribute('scriptableValues', 'sima/sima/ScriptableValue', '', True, Dimension('*')))
        self.attributes.append(BlueprintAttribute('guidePoint', 'sima/simo/GuidePoint', 'Guide point', False))
        self.attributes.append(Attribute('enteredOnLine', 'boolean', 'Guide point entered on line', default=True))