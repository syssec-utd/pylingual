"""
日ごとユーザごとの生産性
"""
from __future__ import annotations
import abc
import logging
from pathlib import Path
from typing import Optional
import bokeh
import bokeh.layouts
import bokeh.palettes
import pandas
from annofabapi.models import TaskPhase
from bokeh.plotting import ColumnDataSource
from dateutil.parser import parse
from annofabcli.common.utils import datetime_to_date, print_csv
from annofabcli.statistics.linegraph import WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX, LineGraph, get_color_from_palette, get_plotted_user_id_list, get_weekly_sum, write_bokeh_graph
logger = logging.getLogger(__name__)

class AbstractPhaseProductivityPerDate(abc.ABC):
    """ロールごとの日ごとの生産性に関する情報を格納する抽象クラス"""
    PLOT_WIDTH = 1200
    PLOT_HEIGHT = 600

    def __init__(self, df: pandas.DataFrame, phase: TaskPhase) -> None:
        self.df = df
        self.phase = phase

    def _validate_df_for_output(self, output_file: Path) -> bool:
        if len(self.df) == 0:
            logger.warning(f'データが0件のため、{output_file} は出力しません。')
            return False
        return True

    @staticmethod
    def _plot(line_graph_list: list[LineGraph], output_file: Path):
        """
        折れ線グラフを、HTMLファイルに出力します。
        """
        graph_group_list = []
        for line_graph in line_graph_list:
            line_graph.config_legend()
            widget_list = []
            hide_all_button = line_graph.create_button_hiding_all_lines()
            widget_list.append(hide_all_button)
            if len(line_graph.marker_glyphs) > 0:
                checkbox_group = line_graph.create_checkbox_displaying_markers()
                widget_list.append(checkbox_group)
            widgets = bokeh.layouts.column(widget_list)
            graph_group = bokeh.layouts.row([line_graph.figure, widgets])
            graph_group_list.append(graph_group)
        write_bokeh_graph(bokeh.layouts.layout(graph_group_list), output_file)

    @classmethod
    @abc.abstractmethod
    def from_df_task(cls, df_task: pandas.DataFrame) -> AbstractPhaseProductivityPerDate:
        raise NotImplementedError()

    @abc.abstractmethod
    def to_csv(self, output_file: Path):
        raise NotImplementedError()

    @abc.abstractmethod
    def plot_input_data_metrics(self, output_file: Path, target_user_id_list: Optional[list[str]]=None):
        raise NotImplementedError()

    @abc.abstractmethod
    def plot_annotation_metrics(self, output_file: Path, target_user_id_list: Optional[list[str]]=None):
        raise NotImplementedError()

class AnnotatorProductivityPerDate(AbstractPhaseProductivityPerDate):
    """教師付開始日ごとの教師付者の生産性に関する情報"""

    def __init__(self, df: pandas.DataFrame):
        super().__init__(df, phase=TaskPhase.ANNOTATION)

    @classmethod
    def from_df_task(cls, df_task: pandas.DataFrame) -> AnnotatorProductivityPerDate:
        """
        日毎、ユーザごとの情報を出力する。

        Args:
            task_df:

        Returns:

        """
        new_df = df_task.copy()
        new_df['first_annotation_started_date'] = new_df['first_annotation_started_datetime'].map(lambda e: datetime_to_date(e) if e is not None and isinstance(e, str) else None)
        new_df['task_count'] = 1
        group_obj = new_df.groupby(['first_annotation_started_date', 'first_annotation_user_id', 'first_annotation_username'], as_index=False)
        sum_df = group_obj[['first_annotation_worktime_hour', 'annotation_worktime_hour', 'inspection_worktime_hour', 'acceptance_worktime_hour', 'worktime_hour', 'task_count', 'input_data_count', 'annotation_count', 'inspection_comment_count']].sum()
        for denominator_column in ['input_data_count', 'annotation_count']:
            for phase in ['annotation', 'inspection', 'acceptance']:
                numerator_column = f'{phase}_worktime_hour'
                sum_df[f'{numerator_column}/{denominator_column}'] = sum_df[numerator_column] / sum_df[denominator_column]
        sum_df['inspection_comment_count/annotation_count'] = sum_df['inspection_comment_count'] / sum_df['annotation_count']
        sum_df['inspection_comment_count/input_data_count'] = sum_df['inspection_comment_count'] / sum_df['annotation_count']
        return cls(sum_df)

    @staticmethod
    def _get_df_sequential_date(df: pandas.DataFrame) -> pandas.DataFrame:
        """連続した日付のDataFrameを生成する。"""
        df_date = pandas.DataFrame({'first_annotation_started_date': [str(e.date()) for e in pandas.date_range(df['first_annotation_started_date'].min(), df['first_annotation_started_date'].max())]})
        df2 = df_date.merge(df, how='left', on='first_annotation_started_date')
        df2['dt_first_annotation_started_date'] = df2['first_annotation_started_date'].map(lambda e: parse(e).date())
        assert len(df) > 0
        first_row = df.iloc[0]
        df2['first_annotation_user_id'] = first_row['first_annotation_user_id']
        df2['first_annotation_username'] = first_row['first_annotation_username']
        df2.fillna({key: 0 for key in ['first_annotation_worktime_hour', 'annotation_worktime_hour', 'inspection_worktime_hour', 'acceptance_worktime_hour', 'worktime_hour', 'inspection_comment_count', 'task_count', 'input_data_count', 'annotation_count', 'inspection_comment']}, inplace=True)
        return df2

    def plot_annotation_metrics(self, output_file: Path, target_user_id_list: Optional[list[str]]=None):
        """
        生産性を教師付作業者ごとにプロットする。

        Args:
            df:
            first_annotation_user_id_list:

        Returns:

        """
        if not self._validate_df_for_output(output_file):
            return
        df = self.df.copy()
        if target_user_id_list is not None:
            user_id_list = target_user_id_list
        else:
            user_id_list = df.sort_values(by='first_annotation_started_date', ascending=False)['first_annotation_user_id'].dropna().unique().tolist()
        user_id_list = get_plotted_user_id_list(user_id_list)
        x_axis_label = '教師付開始日'
        tooltip_columns = ['first_annotation_user_id', 'first_annotation_username', 'first_annotation_started_date', 'annotation_worktime_hour', 'task_count', 'input_data_count', 'annotation_count', 'inspection_comment_count']
        line_graph_list = [LineGraph(title='教師付開始日ごとの教師付作業時間', y_axis_label='教師付作業時間[hour]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='教師付開始日ごとのアノテーションあたり教師付作業時間', y_axis_label='アノテーションあたり教師付時間[min/annotation]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='教師付開始日ごとのアノテーションあたり教師付作業時間(1週間移動平均)', y_axis_label='アノテーションあたり教師付時間[min/annotation]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='教師付開始日ごとのアノテーションあたり検査コメント数', y_axis_label='アノテーションあたり検査コメント数', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='教師付開始日ごとのアノテーションあたり検査コメント数(1週間移動平均)', y_axis_label='アノテーションあたり検査コメント数', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime')]
        x_column = 'dt_first_annotation_started_date'
        columns_list = [(x_column, 'annotation_worktime_hour'), (x_column, 'annotation_worktime_minute/annotation_count'), (x_column, f'annotation_worktime_minute/annotation_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'), (x_column, 'inspection_comment_count/annotation_count'), (x_column, f'inspection_comment_count/annotation_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}')]
        logger.debug(f'{output_file} を出力します。')
        line_count = 0
        for user_index, user_id in enumerate(user_id_list):
            df_subset = df[df['first_annotation_user_id'] == user_id]
            if df_subset.empty:
                logger.debug(f'dataframe is empty. user_id = {user_id}')
                continue
            df_subset = self._get_df_sequential_date(df_subset)
            df_subset['annotation_worktime_minute/annotation_count'] = df_subset['annotation_worktime_hour'] * 60 / df_subset['annotation_count']
            df_subset[f'annotation_worktime_minute/annotation_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'] = get_weekly_sum(df_subset['annotation_worktime_hour']) * 60 / get_weekly_sum(df_subset['annotation_count'])
            df_subset[f'inspection_comment_count/annotation_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'] = get_weekly_sum(df_subset['inspection_comment_count']) / get_weekly_sum(df_subset['annotation_count'])
            source = ColumnDataSource(data=df_subset)
            color = get_color_from_palette(user_index)
            username = df_subset.iloc[0]['first_annotation_username']
            line_count += 1
            for line_graph, (x_column, y_column) in zip(line_graph_list, columns_list):
                if y_column.endswith(WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX):
                    line_graph.add_moving_average_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
                else:
                    line_graph.add_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
        if line_count == 0:
            logger.warning(f"プロットするデータがなかっため、'{output_file}'は出力しません。")
            return
        self._plot(line_graph_list, output_file)

    def plot_input_data_metrics(self, output_file: Path, target_user_id_list: Optional[list[str]]=None):
        """
        教師付者の入力データ単位の生産性情報を折れ線グラフでプロットする。
        """
        if not self._validate_df_for_output(output_file):
            return
        df = self.df.copy()
        if target_user_id_list is not None:
            user_id_list = target_user_id_list
        else:
            user_id_list = df.sort_values(by='first_annotation_started_date', ascending=False)['first_annotation_user_id'].dropna().unique().tolist()
        user_id_list = get_plotted_user_id_list(user_id_list)
        x_axis_label = '教師付開始日'
        tooltip_columns = ['first_annotation_user_id', 'first_annotation_username', 'first_annotation_started_date', 'annotation_worktime_hour', 'task_count', 'input_data_count', 'inspection_comment_count']
        line_graph_list = [LineGraph(title='教師付開始日ごとの教師付作業時間', y_axis_label='教師付作業時間[hour]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='教師付開始日ごとの入力データあたり教師付作業時間', y_axis_label='入力データあたり教師付時間[min/input_data]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='教師付開始日ごとの入力データあたり教師付作業時間(1週間移動平均)', y_axis_label='入力データあたり教師付時間[min/annotation]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='教師付開始日ごとの入力データあたり検査コメント数', y_axis_label='入力データあたり検査コメント数', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='教師付開始日ごとの入力データあたり検査コメント数(1週間移動平均)', y_axis_label='入力データあたり検査コメント数', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime')]
        x_column = 'dt_first_annotation_started_date'
        columns_list = [(x_column, 'annotation_worktime_hour'), (x_column, 'annotation_worktime_minute/input_data_count'), (x_column, f'annotation_worktime_minute/input_data_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'), (x_column, 'inspection_comment_count/input_data_count'), (x_column, f'inspection_comment_count/input_data_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}')]
        logger.debug(f'{output_file} を出力します。')
        line_count = 0
        for user_index, user_id in enumerate(user_id_list):
            df_subset = df[df['first_annotation_user_id'] == user_id]
            if df_subset.empty:
                logger.debug(f'dataframe is empty. user_id = {user_id}')
                continue
            df_subset = self._get_df_sequential_date(df_subset)
            df_subset['annotation_worktime_minute/input_data_count'] = df_subset['annotation_worktime_hour'] * 60 / df_subset['input_data_count']
            df_subset[f'annotation_worktime_minute/input_data_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'] = get_weekly_sum(df_subset['annotation_worktime_hour']) * 60 / get_weekly_sum(df_subset['input_data_count'])
            df_subset[f'inspection_comment_count/input_data_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'] = get_weekly_sum(df_subset['inspection_comment_count']) / get_weekly_sum(df_subset['input_data_count'])
            source = ColumnDataSource(data=df_subset)
            color = get_color_from_palette(user_index)
            username = df_subset.iloc[0]['first_annotation_username']
            line_count += 1
            for line_graph, (x_column, y_column) in zip(line_graph_list, columns_list):
                if y_column.endswith(WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX):
                    line_graph.add_moving_average_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
                else:
                    line_graph.add_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
        if line_count == 0:
            logger.warning(f"プロットするデータがなかっため、'{output_file}'は出力しません。")
            return
        self._plot(line_graph_list, output_file)

    def to_csv(self, output_file: Path) -> None:
        if not self._validate_df_for_output(output_file):
            return
        production_columns = ['first_annotation_started_date', 'first_annotation_user_id', 'first_annotation_username', 'task_count', 'input_data_count', 'annotation_count', 'inspection_comment_count', 'worktime_hour', 'annotation_worktime_hour', 'inspection_worktime_hour', 'acceptance_worktime_hour']
        velocity_columns = [f'{numerator}/{denominator}' for numerator in ['annotation_worktime_hour', 'inspection_worktime_hour', 'acceptance_worktime_hour'] for denominator in ['input_data_count', 'annotation_count']]
        columns = production_columns + velocity_columns + ['inspection_comment_count/input_data_count', 'inspection_comment_count/annotation_count']
        print_csv(self.df[columns], output=str(output_file))

class InspectorProductivityPerDate(AbstractPhaseProductivityPerDate):
    """検査開始日ごとの検査者の生産性に関する情報"""

    def __init__(self, df: pandas.DataFrame):
        super().__init__(df, phase=TaskPhase.INSPECTION)

    @classmethod
    def from_df_task(cls, df_task: pandas.DataFrame) -> InspectorProductivityPerDate:
        """
        検査開始日ごとの受入者の生産性に関するDataFrameを生成する。

        Args:
            df_task:

        Returns:

        """
        new_df = df_task.copy()
        new_df['first_inspection_started_date'] = new_df['first_inspection_started_datetime'].map(lambda e: datetime_to_date(e) if e is not None and isinstance(e, str) else None)
        new_df['task_count'] = 1
        group_obj = new_df.groupby(['first_inspection_started_date', 'first_inspection_user_id', 'first_inspection_username'], as_index=False)
        sum_df = group_obj[['first_inspection_worktime_hour', 'inspection_worktime_hour', 'task_count', 'input_data_count', 'annotation_count']].sum()
        sum_df['inspection_worktime_hour/annotation_count'] = sum_df['inspection_worktime_hour'] / sum_df['annotation_count']
        sum_df['inspection_worktime_hour/input_data_count'] = sum_df['inspection_worktime_hour'] / sum_df['input_data_count']
        return cls(sum_df)

    @staticmethod
    def _get_df_sequential_date(df: pandas.DataFrame) -> pandas.DataFrame:
        """連続した日付のDataFrameを生成する。"""
        df_date = pandas.DataFrame({'first_inspection_started_date': [str(e.date()) for e in pandas.date_range(df['first_inspection_started_date'].min(), df['first_inspection_started_date'].max())]})
        df2 = df_date.merge(df, how='left', on='first_inspection_started_date')
        df2['dt_first_inspection_started_date'] = df2['first_inspection_started_date'].map(lambda e: parse(e).date())
        assert len(df) > 0
        first_row = df.iloc[0]
        df2['first_inspection_user_id'] = first_row['first_inspection_user_id']
        df2['first_inspection_username'] = first_row['first_inspection_username']
        df2.fillna({key: 0 for key in ['first_inspection_worktime_hour', 'inspection_worktime_hour', 'task_count', 'input_data_count', 'annotation_count']}, inplace=True)
        return df2

    def plot_annotation_metrics(self, output_file: Path, target_user_id_list: Optional[list[str]]=None):
        """
        アノテーション単位の生産性を受入作業者ごとにプロットする。

        """
        if not self._validate_df_for_output(output_file):
            return
        df = self.df.copy()
        if target_user_id_list is not None:
            user_id_list = target_user_id_list
        else:
            user_id_list = df.sort_values(by='first_inspection_started_date', ascending=False)['first_inspection_user_id'].dropna().unique().tolist()
        user_id_list = get_plotted_user_id_list(user_id_list)
        x_axis_label = '検査開始日'
        tooltip_columns = ['first_inspection_user_id', 'first_inspection_username', 'first_inspection_started_date', 'inspection_worktime_hour', 'task_count', 'input_data_count', 'annotation_count']
        line_graph_list = [LineGraph(title='検査開始日ごとの受入作業時間', y_axis_label='検査作業時間[hour]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='検査開始日ごとのアノテーションあたり検査作業時間', y_axis_label='アノテーションあたり検査作業時間[min/annotation]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='検査開始日ごとのアノテーションあたり検査作業時間(1週間移動平均)', y_axis_label='アノテーションあたり検査作業時間[min/annotation]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime')]
        x_column = 'dt_first_inspection_started_date'
        columns_list = [(x_column, 'inspection_worktime_hour'), (x_column, 'inspection_worktime_minute/annotation_count'), (x_column, f'inspection_worktime_minute/annotation_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}')]
        logger.debug(f'{output_file} を出力します。')
        line_count = 0
        for user_index, user_id in enumerate(user_id_list):
            df_subset = df[df['first_inspection_user_id'] == user_id]
            if df_subset.empty:
                logger.debug(f'dataframe is empty. user_id = {user_id}')
                continue
            df_subset = self._get_df_sequential_date(df_subset)
            df_subset['inspection_worktime_minute/annotation_count'] = df_subset['inspection_worktime_hour'] * 60 / df_subset['annotation_count']
            df_subset[f'inspection_worktime_minute/annotation_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'] = get_weekly_sum(df_subset['inspection_worktime_hour']) * 60 / get_weekly_sum(df_subset['annotation_count'])
            source = ColumnDataSource(data=df_subset)
            color = get_color_from_palette(user_index)
            username = df_subset.iloc[0]['first_inspection_username']
            for line_graph, (x_column, y_column) in zip(line_graph_list, columns_list):
                if y_column.endswith(WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX):
                    line_graph.add_moving_average_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
                else:
                    line_graph.add_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
        if line_count == 0:
            logger.warning(f"プロットするデータがなかっため、'{output_file}'は出力しません。")
            return
        self._plot(line_graph_list, output_file)

    def plot_input_data_metrics(self, output_file: Path, target_user_id_list: Optional[list[str]]=None):
        """
        検査者の入力データ単位の生産性情報を折れ線グラフでプロットする。
        """
        if not self._validate_df_for_output(output_file):
            return
        df = self.df.copy()
        if target_user_id_list is not None:
            user_id_list = target_user_id_list
        else:
            user_id_list = df.sort_values(by='first_inspection_started_date', ascending=False)['first_inspection_user_id'].dropna().unique().tolist()
        user_id_list = get_plotted_user_id_list(user_id_list)
        x_axis_label = '検査開始日'
        x_column = 'dt_first_inspection_started_date'
        tooltip_columns = ['first_annotation_user_id', 'first_inspection_username', 'first_inspection_started_date', 'inspection_worktime_hour', 'task_count', 'input_data_count', 'inspection_comment_count']
        line_graph_list = [LineGraph(title='検査開始日ごとの検査作業時間', y_axis_label='検査作業時間[hour]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='検査開始日ごとの入力データあたり検査作業時間', y_axis_label='入力データあたり検査時間[min/input_data]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='検査開始日ごとの入力データあたり検査作業時間(1週間移動平均)', y_axis_label='入力データあたり検査時間[min/annotation]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime')]
        x_column = 'dt_first_inspection_started_date'
        columns_list = [(x_column, 'inspection_worktime_hour'), (x_column, 'inspection_worktime_minute/input_data_count'), (x_column, f'inspection_worktime_minute/input_data_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}')]
        logger.debug(f'{output_file} を出力します。')
        line_count = 0
        for user_index, user_id in enumerate(user_id_list):
            df_subset = df[df['first_inspection_user_id'] == user_id]
            if df_subset.empty:
                logger.debug(f'dataframe is empty. user_id = {user_id}')
                continue
            df_subset = self._get_df_sequential_date(df_subset)
            df_subset['inspection_worktime_minute/input_data_count'] = df_subset['inspection_worktime_hour'] * 60 / df_subset['input_data_count']
            df_subset[f'inspection_worktime_minute/input_data_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'] = get_weekly_sum(df_subset['inspection_worktime_hour']) * 60 / get_weekly_sum(df_subset['input_data_count'])
            source = ColumnDataSource(data=df_subset)
            color = get_color_from_palette(user_index)
            username = df_subset.iloc[0]['first_inspection_username']
            line_count += 1
            for line_graph, (x_column, y_column) in zip(line_graph_list, columns_list):
                if y_column.endswith(WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX):
                    line_graph.add_moving_average_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
                else:
                    line_graph.add_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
        if line_count == 0:
            logger.warning(f"プロットするデータがなかっため、'{output_file}'は出力しません。")
            return
        self._plot(line_graph_list, output_file)

    def to_csv(self, output_file: Path) -> None:
        """
        検査作業者の日ごとの生産性が記載されたCSVを出力する。

        """
        if not self._validate_df_for_output(output_file):
            return
        production_columns = ['first_inspection_started_date', 'first_inspection_user_id', 'first_inspection_username', 'task_count', 'input_data_count', 'annotation_count', 'inspection_worktime_hour']
        velocity_columns = [f'inspection_worktime_hour/{denominator}' for denominator in ['input_data_count', 'annotation_count']]
        columns = production_columns + velocity_columns
        print_csv(self.df[columns], output=str(output_file))

class AcceptorProductivityPerDate(AbstractPhaseProductivityPerDate):
    """受入開始日ごとの受入者の生産性に関する情報"""

    def __init__(self, df: pandas.DataFrame):
        super().__init__(df, phase=TaskPhase.ACCEPTANCE)

    @classmethod
    def from_df_task(cls, df_task: pandas.DataFrame) -> AcceptorProductivityPerDate:
        """
        受入開始日ごとの受入者の生産性に関するDataFrameを生成する。

        Args:
            df_task:

        Returns:

        """
        new_df = df_task.copy()
        new_df['first_acceptance_started_date'] = new_df['first_acceptance_started_datetime'].map(lambda e: datetime_to_date(e) if e is not None and isinstance(e, str) else None)
        new_df['task_count'] = 1
        group_obj = new_df.groupby(['first_acceptance_started_date', 'first_acceptance_user_id', 'first_acceptance_username'], as_index=False)
        sum_df = group_obj[['first_acceptance_worktime_hour', 'acceptance_worktime_hour', 'task_count', 'input_data_count', 'annotation_count']].sum()
        sum_df['acceptance_worktime_hour/annotation_count'] = sum_df['acceptance_worktime_hour'] / sum_df['annotation_count']
        sum_df['acceptance_worktime_hour/input_data_count'] = sum_df['acceptance_worktime_hour'] / sum_df['input_data_count']
        return AcceptorProductivityPerDate(sum_df)

    @staticmethod
    def _get_df_sequential_date(df: pandas.DataFrame) -> pandas.DataFrame:
        """連続した日付のDataFrameを生成する。"""
        df_date = pandas.DataFrame({'first_acceptance_started_date': [str(e.date()) for e in pandas.date_range(df['first_acceptance_started_date'].min(), df['first_acceptance_started_date'].max())]})
        df2 = df_date.merge(df, how='left', on='first_acceptance_started_date')
        df2['dt_first_acceptance_started_date'] = df2['first_acceptance_started_date'].map(lambda e: parse(e).date())
        assert len(df) > 0
        first_row = df.iloc[0]
        df2['first_acceptance_user_id'] = first_row['first_acceptance_user_id']
        df2['first_acceptance_username'] = first_row['first_acceptance_username']
        df2.fillna({key: 0 for key in ['first_acceptance_worktime_hour', 'acceptance_worktime_hour', 'task_count', 'input_data_count', 'annotation_count']}, inplace=True)
        return df2

    def plot_annotation_metrics(self, output_file: Path, target_user_id_list: Optional[list[str]]=None):
        """
        アノテーション単位の生産性を受入作業者ごとにプロットする。

        """
        if not self._validate_df_for_output(output_file):
            return
        df = self.df.copy()
        if target_user_id_list is not None:
            user_id_list = target_user_id_list
        else:
            user_id_list = df.sort_values(by='first_acceptance_started_date', ascending=False)['first_acceptance_user_id'].dropna().unique().tolist()
        user_id_list = get_plotted_user_id_list(user_id_list)
        x_axis_label = '受入開始日'
        x_column = 'dt_first_acceptance_started_date'
        tooltip_columns = ['first_acceptance_user_id', 'first_acceptance_username', 'first_acceptance_started_date', 'acceptance_worktime_hour', 'task_count', 'input_data_count', 'annotation_count']
        line_graph_list = [LineGraph(title='受入開始日ごとの受入作業時間', y_axis_label='受入作業時間[hour]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='受入開始日ごとのアノテーションあたり受入作業時間', y_axis_label='アノテーションあたり受入時間[min/annotation]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='受入開始日ごとのアノテーションあたり受入作業時間(1週間移動平均)', y_axis_label='アノテーションあたり受入時間[min/annotation]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime')]
        x_column = 'dt_first_acceptance_started_date'
        columns_list = [(x_column, 'acceptance_worktime_hour'), (x_column, 'acceptance_worktime_minute/annotation_count'), (x_column, f'acceptance_worktime_minute/annotation_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}')]
        logger.debug(f'{output_file} を出力します。')
        line_count = 0
        for user_index, user_id in enumerate(user_id_list):
            df_subset = df[df['first_acceptance_user_id'] == user_id]
            if df_subset.empty:
                logger.debug(f'dataframe is empty. user_id = {user_id}')
                continue
            df_subset = self._get_df_sequential_date(df_subset)
            df_subset['acceptance_worktime_minute/annotation_count'] = df_subset['acceptance_worktime_hour'] * 60 / df_subset['annotation_count']
            df_subset[f'acceptance_worktime_minute/annotation_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'] = get_weekly_sum(df_subset['acceptance_worktime_hour']) * 60 / get_weekly_sum(df_subset['annotation_count'])
            source = ColumnDataSource(data=df_subset)
            color = get_color_from_palette(user_index)
            username = df_subset.iloc[0]['first_acceptance_username']
            line_count += 1
            for line_graph, (x_column, y_column) in zip(line_graph_list, columns_list):
                if y_column.endswith(WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX):
                    line_graph.add_moving_average_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
                else:
                    line_graph.add_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
        if line_count == 0:
            logger.warning(f"プロットするデータがなかっため、'{output_file}'は出力しません。")
            return
        self._plot(line_graph_list, output_file)

    def plot_input_data_metrics(self, output_file: Path, target_user_id_list: Optional[list[str]]=None):
        """
        教師付者の入力データ単位の生産性情報を折れ線グラフでプロットする。
        """
        if not self._validate_df_for_output(output_file):
            return
        df = self.df.copy()
        if target_user_id_list is not None:
            user_id_list = target_user_id_list
        else:
            user_id_list = df.sort_values(by='first_acceptance_started_date', ascending=False)['first_acceptance_user_id'].dropna().unique().tolist()
        user_id_list = get_plotted_user_id_list(user_id_list)
        x_axis_label = '受入開始日'
        x_column = 'dt_first_acceptance_started_date'
        tooltip_columns = ['first_acceptance_user_id', 'first_acceptance_username', 'first_acceptance_started_date', 'acceptance_worktime_hour', 'task_count', 'input_data_count']
        line_graph_list = [LineGraph(title='受入開始日ごとの受入作業時間', y_axis_label='受入作業時間[hour]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='受入開始日ごとの入力データあたり受入作業時間', y_axis_label='入力データあたり受入作業時間[min/input_data]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime'), LineGraph(title='受入開始日ごとの入力データあたり受入作業時間(1週間移動平均)', y_axis_label='入力データあたり受入作業時間[min/annotation]', tooltip_columns=tooltip_columns, x_axis_label=x_axis_label, x_axis_type='datetime')]
        x_column = 'dt_first_acceptance_started_date'
        columns_list = [(x_column, 'acceptance_worktime_hour'), (x_column, 'acceptance_worktime_minute/input_data_count'), (x_column, f'acceptance_worktime_minute/input_data_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}')]
        logger.debug(f'{output_file} を出力します。')
        line_count = 0
        for user_index, user_id in enumerate(user_id_list):
            df_subset = df[df['first_acceptance_user_id'] == user_id]
            if df_subset.empty:
                logger.debug(f'dataframe is empty. user_id = {user_id}')
                continue
            df_subset = self._get_df_sequential_date(df_subset)
            df_subset['acceptance_worktime_minute/input_data_count'] = df_subset['acceptance_worktime_hour'] * 60 / df_subset['input_data_count']
            df_subset[f'acceptance_worktime_minute/input_data_count{WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX}'] = get_weekly_sum(df_subset['acceptance_worktime_hour']) * 60 / get_weekly_sum(df_subset['input_data_count'])
            source = ColumnDataSource(data=df_subset)
            color = get_color_from_palette(user_index)
            username = df_subset.iloc[0]['first_acceptance_username']
            line_count += 1
            for line_graph, (x_column, y_column) in zip(line_graph_list, columns_list):
                if y_column.endswith(WEEKLY_MOVING_AVERAGE_COLUMN_SUFFIX):
                    line_graph.add_moving_average_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
                else:
                    line_graph.add_line(source=source, x_column=x_column, y_column=y_column, legend_label=username, color=color)
        if line_count == 0:
            logger.warning(f"プロットするデータがなかっため、'{output_file}'は出力しません。")
            return
        self._plot(line_graph_list, output_file)

    def to_csv(self, output_file: Path) -> None:
        """
        受入作業者の日ごとの生産性が記載されたCSVを出力する。

        """
        if not self._validate_df_for_output(output_file):
            return
        production_columns = ['first_acceptance_started_date', 'first_acceptance_user_id', 'first_acceptance_username', 'task_count', 'input_data_count', 'annotation_count', 'acceptance_worktime_hour']
        velocity_columns = [f'acceptance_worktime_hour/{denominator}' for denominator in ['input_data_count', 'annotation_count']]
        columns = production_columns + velocity_columns
        print_csv(self.df[columns], output=str(output_file))