from dataclasses import dataclass, field
from typing import List
from quid.match.Match import Match

@dataclass
class TextWithMatches:
    name: str
    text: str
    matches: List[Match] = field(default_factory=list)