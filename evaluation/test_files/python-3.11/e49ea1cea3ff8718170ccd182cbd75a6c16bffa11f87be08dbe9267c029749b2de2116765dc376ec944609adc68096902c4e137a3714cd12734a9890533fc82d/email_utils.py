import pandas as pd
from pandas.api.types import is_string_dtype
from upgini.utils.base_search_key_detector import BaseSearchKeyDetector

class EmailSearchKeyDetector(BaseSearchKeyDetector):

    def _is_search_key_by_name(self, column_name: str) -> bool:
        return column_name.lower() in ['email', 'e_mail', 'e-mail']

    def _is_search_key_by_values(self, column: pd.Series) -> bool:
        if not is_string_dtype(column):
            return False
        all_count = len(column)
        is_countries_count = len(column.loc[column.str.contains('@') & column.str.contains('.', regex=False)])
        return is_countries_count / all_count > 0.1