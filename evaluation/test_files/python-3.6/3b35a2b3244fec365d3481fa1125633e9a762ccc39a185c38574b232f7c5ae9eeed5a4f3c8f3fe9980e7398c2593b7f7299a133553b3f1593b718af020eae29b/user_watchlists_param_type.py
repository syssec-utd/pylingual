from typing import List, Tuple
import investor8_sdk
import pandas as pd
from i8_terminal.config import USER_SETTINGS
from i8_terminal.types.auto_complete_choice import AutoCompleteChoice

def get_user_watchlists() -> List[Tuple[str, str]]:
    results = investor8_sdk.UserApi().get_watchlists_by_user(user_id=USER_SETTINGS.get('user_id'))
    df = pd.DataFrame([d.to_dict() for d in results.watchlists])[['name']]
    df['name'] = df['name'].apply(lambda x: f'"{x}"' if ' ' in x else x)
    df['desc'] = ''
    return list(df.to_records(index=False))

class UserWatchlistsParamType(AutoCompleteChoice):
    name = 'userwatchlists'

    def get_suggestions(self, keyword: str, pre_populate: bool=False) -> List[Tuple[str, str]]:
        if not self.is_loaded:
            self.set_choices(get_user_watchlists())
        if pre_populate and keyword.strip() == '':
            return self._choices[:self.size]
        return self.search_keyword(keyword)

    def __repr__(self) -> str:
        return 'USERWATCHLISTS'