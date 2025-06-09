import json
from pathlib import Path
from typing import List, Dict
from .property import Property
from .event import WeightedEvent

class AgeManager:

    def __init__(self, prop: Property):
        self.prop = prop
        self.ages: Dict[int, List[WeightedEvent]] = {}

    def load(self, path: Path):
        data: Dict[str, dict] = json.load(path.open('r', encoding='utf8'))
        self.ages = {int(k): [WeightedEvent(s) for s in v.get('event', [])] for (k, v) in data.items()}

    def get_events(self) -> List[WeightedEvent]:
        return self.ages[self.prop.AGE]

    def grow(self):
        self.prop.AGE += 1