from typing import Dict, Callable, List
from dialogy.plugins.text.intent_entity_mutator.actions_on_primitives import contain_digits, is_number_absent
transcript_functions_map: Dict[str, Callable[[List[str]], int]] = {'is_number_absent': is_number_absent, 'contain_digits': contain_digits}