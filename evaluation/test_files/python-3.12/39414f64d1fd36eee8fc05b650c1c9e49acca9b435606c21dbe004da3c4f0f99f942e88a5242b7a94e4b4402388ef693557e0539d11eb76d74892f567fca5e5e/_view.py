from typing import Any, Dict, List, Optional, Tuple, Union, Type
from dataclasses import dataclass
import sys
from dash.development.base_component import Component
from dash import html, Input, Output, State, callback
from dash.exceptions import PreventUpdate
import pandas as pd
import webviz_core_components as wcc
from webviz_config import WebvizPluginABC, EncodedFile
from webviz_config.webviz_plugin_subclasses import ViewABC, ViewElementABC, SettingsGroupABC, callback_typecheck
from webviz_config.utils import StrEnum
from webviz_config.generic_plugins._example_wlf_plugin._shared_view_elements import TextViewElement
if sys.version_info >= (3, 9):
    from typing import Annotated
else:
    from typing_extensions import Annotated

class Kindness(StrEnum):
    FRIENDLY = 'friendly'
    UNFRIENDLY = 'unfriendly'

class Coordinates(StrEnum):
    XY = 'xy'
    YX = 'yx'

class PlotViewSettingsGroup(SettingsGroupABC):

    class Ids(StrEnum):
        COORDINATES_SELECTOR = 'coordinates-selector'

    def __init__(self) -> None:
        super().__init__('Plot coordinate system')

    def layout(self) -> List[Component]:
        return [wcc.Dropdown(id=self.register_component_unique_id(PlotViewSettingsGroup.Ids.COORDINATES_SELECTOR), label='Coordinates', options=[{'label': 'x - y', 'value': Coordinates.XY}, {'label': 'y - x', 'value': Coordinates.YX}], value=Coordinates.XY, clearable=False)]

class PlotViewElement(ViewElementABC):

    class Ids(StrEnum):
        GRAPH = 'graph'

    def __init__(self, data: List[Tuple[int, int]]) -> None:
        super().__init__(flex_grow=8)
        self.data = data

    def inner_layout(self) -> Union[str, Type[Component]]:
        return html.Div(style={'height': '20vh'}, children=[wcc.Graph(id=self.register_component_unique_id(PlotViewElement.Ids.GRAPH), figure={'data': [{'x': [x[0] for x in self.data], 'y': [x[1] for x in self.data]}], 'layout': {'title': 'Example Graph Swapped'}}, config={'responsive': True})])

    @staticmethod
    def download_data_df(graph_figure: Dict[str, Any]) -> pd.DataFrame:
        graph_data: Optional[List[Dict[str, Any]]] = graph_figure.get('data', None)
        if not graph_data:
            return 'No data present in graph figure'
        x_values = graph_data[0].get('x', None)
        y_values = graph_data[0].get('y', None)
        if x_values is None or y_values is None:
            return f'Missing x or y data: x = {x_values} and y = {y_values}'
        df = pd.DataFrame(columns=['x', 'y'])
        df['x'] = x_values
        df['y'] = y_values
        return df

    def compressed_plugin_data(self, graph_figure: Dict[str, Any]) -> Union[EncodedFile, str]:
        return WebvizPluginABC.plugin_data_compress([{'filename': f'{self.component_unique_id(PlotViewElement.Ids.GRAPH).to_string()}.csv', 'content': self.download_data_df(graph_figure).to_csv(index=False)}])

    def set_callbacks(self) -> None:

        @callback(self.view_element_data_output(), self.view_element_data_requested(), State(self.component_unique_id(PlotViewElement.Ids.GRAPH).to_string(), 'figure'))
        def _download_data(data_requested: Union[int, None], graph_figure: Dict[str, Any]) -> Union[EncodedFile, str]:
            if data_requested is None:
                raise PreventUpdate
            return self.compressed_plugin_data(graph_figure)

class PlotView(ViewABC):

    class Ids(StrEnum):
        TEXT = 'text'
        PLOT = 'plot'
        PLOT_SETTINGS = 'plot-settings'

    @dataclass
    class Slots:
        kindness_selector: Annotated[Input, str]
        power_selector: Annotated[Input, str]

    def __init__(self, data: List[Tuple[int, int]], slots: Slots) -> None:
        super().__init__('Plot')
        self.data = data
        self.slots = slots
        self._plot_view = PlotViewElement(self.data)
        row = self.add_row()
        row.add_view_element(TextViewElement(), PlotView.Ids.TEXT)
        row.add_view_element(self._plot_view, PlotView.Ids.PLOT)
        self.add_settings_group(PlotViewSettingsGroup(), PlotView.Ids.PLOT_SETTINGS)

    def set_callbacks(self) -> None:

        @callback(Output(self.view_element(PlotView.Ids.TEXT).component_unique_id(TextViewElement.Ids.TEXT).to_string(), 'children'), self.slots.kindness_selector)
        @callback_typecheck
        def _change_kindness(kindness: Kindness) -> Component:
            if kindness == Kindness.FRIENDLY:
                return [html.H1('Hello'), '\n                    I am an example plugin.\n                    Please have a look how views and settings are working in my environment =).\n                    ']
            return [html.H1('Goodbye'), 'I am a bloody example plugin. Leave me alone! =(']

        @callback(Output(self.view_elements()[1].component_unique_id(PlotViewElement.Ids.GRAPH).to_string(), 'figure'), self.slots.power_selector, Input(self.settings_group(PlotView.Ids.PLOT_SETTINGS).component_unique_id(PlotViewSettingsGroup.Ids.COORDINATES_SELECTOR).to_string(), 'value'))
        @callback_typecheck
        def _change_power_and_coordinates(power: int, coordinates: Coordinates) -> dict:
            layout = {'title': 'Example Graph Swapped', 'margin': {'t': 50, 'r': 20, 'b': 20, 'l': 20}}
            if power == 2:
                self.data = [(x, x * x) for x in range(0, 10)]
            else:
                self.data = [(x, x * x * x) for x in range(0, 10)]
            if coordinates == Coordinates.YX:
                return {'data': [{'x': [x[1] for x in self.data], 'y': [x[0] for x in self.data]}], 'layout': layout}
            return {'data': [{'x': [x[0] for x in self.data], 'y': [x[1] for x in self.data]}], 'layout': layout}

        @callback(self.view_data_output(), self.view_data_requested(), State(self._plot_view.component_unique_id(PlotViewElement.Ids.GRAPH).to_string(), 'figure'))
        def _download_data(data_requested: Union[int, None], graph_figure: Dict[str, Any]) -> Union[EncodedFile, str]:
            if data_requested is None:
                raise PreventUpdate
            return self._plot_view.compressed_plugin_data(graph_figure)