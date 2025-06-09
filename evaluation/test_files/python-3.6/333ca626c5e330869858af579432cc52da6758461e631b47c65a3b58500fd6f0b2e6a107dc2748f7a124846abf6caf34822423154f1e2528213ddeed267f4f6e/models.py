from typing import List
from pydantic import BaseModel

class CaseStep(BaseModel):
    id: int
    name: str
    key_word: str
    args: List[str]

class Case(BaseModel):
    id: int
    name: str
    steps: List[CaseStep]

class Suite(BaseModel):
    name: str
    case_list: List[Case]