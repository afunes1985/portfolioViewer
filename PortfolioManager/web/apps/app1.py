'''
Created on 4 nov. 2018

@author: afunes
'''

from datetime import datetime

from dash.dependencies import Output, Input
from dash_table import FormatTemplate

from base.initializer import Initializer
from core.cache import MainCache
import dash_html_components as html
import dash_table as dt
from engine.positionEngine import PositionEngine
from web.app import app
import dash_bootstrap_components as dbc


Initializer()

formatColumns = [{"name": 'Asset Name', 'id': 'Asset Name', "deletable": False},
                 {"name": 'Asset Type', 'id': 'Asset Type', "deletable": False},
                 {"name": 'Position', 'id': 'Position', "deletable": False, 'type': 'numeric'},
                 {"name": 'Unit Cost', 'id': 'Unit Cost', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Market Price', 'id': 'Market Price', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Change', 'id': 'Change', "deletable": False, 'type': 'numeric','format': FormatTemplate.percentage(2)},
                 {"name": 'Invested Amount', 'id': 'Invested Amount', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Valuated Amount', 'id': 'Valuated Amount', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Tenor', 'id': 'Tenor', "deletable": False, 'type': 'numeric'},
#                 {"name": 'Maturity Date', 'id': 'Maturity Date', "deletable": False},
                 {"name": 'Gross PnL', 'id': 'Gross PnL', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Net PnL', 'id': 'Net PnL', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Gross%PNL', 'id': 'Gross%PNL', "deletable": False, 'type': 'numeric','format': FormatTemplate.percentage(2)},
                 {"name": 'Net%PNL', 'id': 'Net%PNL', "deletable": False, 'type': 'numeric','format': FormatTemplate.percentage(2)},
                 {"name": 'Realized PnL', 'id': 'Realized PnL', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": '%Portfolio', 'id': '%Portfolio', "deletable": False, 'type': 'numeric'},
                 {"name": 'WeightedPnL%', 'id': 'WeightedPnL%', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)}]

styleDataCondition = [{ 'if': {'column_id': 'Gross PnL','filter_query': '{Gross PnL} > 0'},'color': 'green', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Gross PnL','filter_query': '{Gross PnL} < 0'},'color': 'red', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Change','filter_query': '{Change} > 0'},'color': 'green', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Change','filter_query': '{Change} < 0'},'color': 'red', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Gross%PNL','filter_query': '{Gross%PNL} > 0'},'color': 'green', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Gross%PNL','filter_query': '{Gross%PNL} < 0'},'color': 'red', 'fontWeight': 'bold'},]

layout = dbc.Container([
            dbc.Row([dbc.Col(html.Button(id='btn-submit', n_clicks=0, children='Submit', style = {'margin': 5})),
                     dbc.Col(html.Label("USD/MXN", style = {'margin': 5}), width = {"size": 1, "offset": 9}),
                     dbc.Col(html.Div(id='lbl-exchangeRate' ,children='', style = {'margin': 5}), width = {"size": 1})]),
            dbc.Row([dbc.Col(html.Div(dt.DataTable(data=[{}], id='dt-position'), style={'display': 'none'}), width={"size": 0}),
                     dbc.Col(html.Div(id='dt-position-container', style = {'width':'90%'}), width={"size": 12,"offset": 1})],
                     justify="center")
        ],style={"max-width":"100%"})

@app.callback(
    [Output('dt-position-container', "children"),
     Output('lbl-exchangeRate', "children")],
    [Input('btn-submit', 'n_clicks')])
def doSubmit(n_clicks):
    if (n_clicks > 0):
        MainCache.refreshReferenceData()
        PositionEngine().refreshPositions(datetime(2001, 7, 14).date(), datetime.now().date())
        df = MainCache.positionDf
        if (len(df) != 0):
            dt2 = dt.DataTable(
                    id='dt-position',
                    data=df.to_dict("rows"),
                    columns= formatColumns,
                    style_as_list_view=True,
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    #filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    style_data_conditional= styleDataCondition)
            return dt2, MainCache.usdMXN
    else:
        return None, None
    

