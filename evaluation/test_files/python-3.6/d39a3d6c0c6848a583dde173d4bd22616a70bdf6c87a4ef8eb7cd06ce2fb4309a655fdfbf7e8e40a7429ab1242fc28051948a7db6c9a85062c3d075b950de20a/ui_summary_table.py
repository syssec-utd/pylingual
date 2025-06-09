"""
Authors:    Francesco Gabbanini <gabbanini_francesco@lilly.com>, 
            Manjunath C Bagewadi <bagewadi_manjunath_c@lilly.com>, 
            Henson Tauro <tauro_henson@lilly.com> 
            (MQ IDS - Data Integration and Analytics)
License:    MIT
"""
from dash import html
from dash import dcc
from dash import dash_table
import dash_bootstrap_components as dbc
from diaadfpro.adfpro_ui.constants import ADFPCUI

class UISummaryTableBuilder:

    def __init__(self, ct, tabdata):
        self.__sct = str(ct)
        self.__tabdata = tabdata
        self.__version = 'Dashboard version: 1.0'
        self.__tomato = '#ff000080'
        self.__green = '#00ff0095'
        self.__gold = '#ffff0080'

    def build(self):
        tab = html.Div([dbc.Row([dbc.Col(html.Div([self.__build_header_refresh_button(), self.__build_table(), html.Br(), self.__build_status_inspect_button()]), width=12)])], style={'margin-top': '1em', 'width': '100%', 'border': 'solid 0px black'})
        return tab

    def __build_header_refresh_button(self):
        cnt = html.Div([dbc.Row([dbc.Col(html.H4(ADFPCUI.LBL_ST_TBL_TITLE), width='7'), dbc.Col(html.P(ADFPCUI.LBL_ST_LATEST_REFRESH + self.__sct, id=ADFPCUI.ID_LATESTFETCH)), dbc.Col(dbc.Button(ADFPCUI.BTN_ST_REFRESH_TABLE, id=ADFPCUI.ID_REFRESH, className='btn btn-primary btn-sm'), style={'text-align': 'right'})])], style={'margin-top': '1em', 'width': '100%', 'border': 'solid 0px black'})
        return cnt

    def __build_table(self):
        table = dcc.Loading(id=ADFPCUI.ID_LOADING_TABLE, children=[html.Div([dash_table.DataTable(id=ADFPCUI.ID_TAB_SUMMARY_TABLE, columns=[{'name': i, 'id': i} for i in self.__tabdata.columns], data=self.__tabdata.to_dict('records'), fixed_rows={'headers': True}, style_table={'height': 520}, sort_action='native', editable=True, filter_action='native', sort_mode='multi', column_selectable='single', style_header={'color': 'black', 'fontWeight': 'bold'}, style_data_conditional=[{'if': {'column_id': 'Equipment'}, 'textAlign': 'left', 'width': '35%'}, {'if': {'column_id': 'id'}, 'color': 'black', 'fontWeight': 'bold'}, {'if': {'filter_query': '{Last_4hr} > 0.6 && {Last_4hr} < 1', 'column_id': 'Last_4hr'}, 'backgroundColor': self.__tomato, 'color': 'black', 'fontWeight': 'bold'}, {'if': {'filter_query': '{Last_4hr} > 0.3 && {Last_4hr} < 0.7', 'column_id': 'Last_4hr'}, 'backgroundColor': self.__gold, 'color': 'black', 'fontWeight': 'bold'}, {'if': {'filter_query': '{Last_4hr} > 0 && {Last_4hr} < 0.4', 'column_id': 'Last_4hr'}, 'backgroundColor': self.__green, 'color': 'black', 'fontWeight': 'bold'}, {'if': {'filter_query': '{Last_24hr} > 0.6 && {Last_24hr} < 1', 'column_id': 'Last_24hr'}, 'backgroundColor': self.__tomato, 'color': 'black', 'fontWeight': 'bold'}, {'if': {'filter_query': '{Last_24hr} > 0.3 && {Last_24hr} < 0.7', 'column_id': 'Last_24hr'}, 'backgroundColor': self.__gold, 'color': 'black', 'fontWeight': 'bold'}, {'if': {'filter_query': '{Last_24hr} > 0 && {Last_24hr} < 0.4', 'column_id': 'Last_24hr'}, 'backgroundColor': self.__green, 'color': 'black', 'fontWeight': 'bold'}, {'if': {'filter_query': '{Last_Week} > 0.6 && {Last_Week} < 1', 'column_id': 'Last_Week'}, 'backgroundColor': self.__tomato, 'color': 'black', 'fontWeight': 'bold'}, {'if': {'filter_query': '{Last_Week} > 0.3 && {Last_Week} < 0.7', 'column_id': 'Last_Week'}, 'backgroundColor': self.__gold, 'color': 'black', 'fontWeight': 'bold'}, {'if': {'filter_query': '{Last_Week} > 0 && {Last_Week} < 0.4', 'column_id': 'Last_Week'}, 'backgroundColor': self.__green, 'color': 'black', 'fontWeight': 'bold'}])])], type=ADFPCUI.LOADIND_TYPE)
        return table

    def __build_status_inspect_button(self):
        status_inspect_button = dbc.Row([dbc.Col(html.Div([dcc.Loading(id=ADFPCUI.ID_LOADING_STATUS, children=[html.Div([html.P('', id=ADFPCUI.ID_NO_CELL_SELECTED)])], type=ADFPCUI.LOADIND_TYPE)]), width=11), dbc.Col(html.Div([dbc.Button(ADFPCUI.BTN_ST_INSPECT, id=ADFPCUI.ID_INSPECT, className='btn btn-primary btn-lg')]), width=1)])
        return status_inspect_button