from contrast.agent.protect.rule.base_rule import BaseRule
from contrast.api.settings_pb2 import ProtectionRule

class MalformedHeader(BaseRule):
    """
    Malformed Header Protection rule
    """
    RULE_NAME = 'malformed-header'

    @property
    def mode(self):
        """
        Always block at perimeter
        """
        return ProtectionRule.BLOCK_AT_PERIMETER