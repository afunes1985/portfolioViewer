'''
Created on 4 nov. 2018

@author: afunes
'''

from _decimal import Decimal
from datetime import datetime

from dash_table import FormatTemplate
from pandas.core.frame import DataFrame

from base.initializer import Initializer
from core.cache import MainCache
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from engine.positionEngine import PositionEngine


Initializer()
MainCache.refreshReferenceData()
PositionEngine().refreshPositions(datetime(2001, 7, 14).date(), datetime.now().date())

df2 = MainCache.positionDf
formatColumns = [{"name": 'Asset Name', 'id': 'Asset Name', "deletable": False},
                 {"name": 'Asset Type', 'id': 'Asset Type', "deletable": False},
                 {"name": 'Position', 'id': 'Position', "deletable": False, 'type': 'numeric'},
                 {"name": 'Market Price', 'id': 'Market Price', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Change', 'id': 'Change', "deletable": False},
                 {"name": 'Invested Amount', 'id': 'Invested Amount', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Valuated Amount', 'id': 'Valuated Amount', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Tenor', 'id': 'Tenor', "deletable": False, 'type': 'numeric'},
                 {"name": 'Maturity Date', 'id': 'Maturity Date', "deletable": False},
                 {"name": 'Gross PnL', 'id': 'Gross PnL', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Net PnL', 'id': 'Net PnL', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Gross%PNL', 'id': 'Gross%PNL', "deletable": False, 'type': 'numeric','format': FormatTemplate.percentage(2)},
                 {"name": 'Net%PNL', 'id': 'Net%PNL', "deletable": False, 'type': 'numeric','format': FormatTemplate.percentage(2)},
                 {"name": 'Realized PnL', 'id': 'Realized PnL', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": '%Portfolio', 'id': '%Portfolio', "deletable": False, 'type': 'numeric'},
                 {"name": 'WeightedPnL%', 'id': 'WeightedPnL%', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)}]

layout = html.Div([
    html.Div(dt.DataTable(
                    id='dt-position',
                    data=df2.to_dict("rows"),
                    columns= formatColumns,
                    style_as_list_view=True,
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    )),
    html.Div(id='dt-position-container')])
