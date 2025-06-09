from dmt.blueprint import Blueprint
from dmt.dimension import Dimension
from dmt.attribute import Attribute
from dmt.enum_attribute import EnumAttribute
from dmt.blueprint_attribute import BlueprintAttribute
from sima.sima.blueprints.moao import MOAOBlueprint

class CurrentItemBlueprint(MOAOBlueprint):
    """"""

    def __init__(self, name='CurrentItem', package_path='sima/environment', description=''):
        super().__init__(name, package_path, description)
        self.attributes.append(Attribute('_id', 'string', '', default=''))
        self.attributes.append(BlueprintAttribute('scriptableValues', 'sima/sima/ScriptableValue', '', True, Dimension('*')))
        self.attributes.append(Attribute('level', 'number', 'Global z-coordinate of current level', default=0.0))
        self.attributes.append(Attribute('direction', 'number', 'Current propagation direction', default=0.0))
        self.attributes.append(Attribute('velocity', 'number', 'Current velocity', default=0.0))