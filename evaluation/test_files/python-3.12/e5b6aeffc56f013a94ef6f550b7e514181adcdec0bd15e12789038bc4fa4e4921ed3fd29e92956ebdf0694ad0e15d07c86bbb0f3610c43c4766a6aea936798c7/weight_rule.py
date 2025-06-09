from enum import Enum
from typing import Set
from airflow.compat.functools import cache

class WeightRule(str, Enum):
    """Weight rules."""
    DOWNSTREAM = 'downstream'
    UPSTREAM = 'upstream'
    ABSOLUTE = 'absolute'

    @classmethod
    def is_valid(cls, weight_rule: str) -> bool:
        """Check if weight rule is valid."""
        return weight_rule in cls.all_weight_rules()

    @classmethod
    @cache
    def all_weight_rules(cls) -> Set[str]:
        """Returns all weight rules"""
        return set(cls.__members__.values())

    def __str__(self) -> str:
        return self.value