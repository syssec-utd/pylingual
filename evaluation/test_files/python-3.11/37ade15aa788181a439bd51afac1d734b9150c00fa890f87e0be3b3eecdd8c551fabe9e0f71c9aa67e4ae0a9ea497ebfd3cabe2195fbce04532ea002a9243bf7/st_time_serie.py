"""
   Descp: Strategy pattern for create simple metrics based on time series.

   Created on: 13-mar-2020

   Copyright 2020-2021 Youssef 'FRYoussef' El Faqir El Rhazoui
        <f.r.youssef@hotmail.com>
"""
import pandas as pd
from dao_analyzer.apps.common.data_access.daos.metric.strategy import IMetricStrategy
from dao_analyzer.apps.common.business.transfers.stacked_serie import StackedSerie
from dao_analyzer.apps.common.business.transfers.serie import Serie
import dao_analyzer.apps.common.data_access.pandas_utils as pd_utl
NEW_USERS: int = 0
NEW_PROPOSAL: int = 1
TOTAL_VOTES: int = 2
TOTAL_STAKES: int = 3

class StTimeSerie(IMetricStrategy):
    __DF_DATE = 'createdAt'
    __DF_COUNT = 'count'
    __DF_COLS = [__DF_DATE, __DF_COUNT]

    def __init__(self, m_type: int):
        self.__m_type = m_type

    def clean_df(self, df: pd.DataFrame) -> pd.DataFrame:
        return df[[self.__DF_DATE]]

    def process_data(self, df: pd.DataFrame) -> StackedSerie:
        if pd_utl.is_an_empty_df(df):
            return StackedSerie()
        df = self.clean_df(df=df)
        df = pd_utl.unix_to_date(df, self.__DF_DATE)
        df = pd_utl.transform_to_monthly_date(df, self.__DF_DATE)
        df = pd_utl.count_cols_repetitions(df, [self.__DF_DATE], self.__DF_COUNT)
        idx = pd_utl.get_monthly_serie_from_df(df, self.__DF_DATE)
        dff = pd_utl.get_df_from_lists([idx, 0], self.__DF_COLS)
        dff = pd_utl.datetime_to_date(dff, self.__DF_DATE)
        df = pd.concat([df, dff], ignore_index=True)
        df = df.drop_duplicates(subset=self.__DF_DATE, keep='first')
        df = df.sort_values(self.__DF_DATE)
        serie: Serie = Serie(x=df[self.__DF_DATE].tolist())
        metric: StackedSerie = StackedSerie(serie=serie, y_stack=[df[self.__DF_COUNT].tolist()])
        return metric