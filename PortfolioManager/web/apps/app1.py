'''
Created on 4 nov. 2018

@author: afunes
'''

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
layout = html.Div([
    html.Div(dt.DataTable(
                    id='dt-position',
                    data=df2.to_dict("rows"),
                    columns=[
                        {"name": i, "id": i, "deletable": False, 'type': 'numeric'} for i in df2.columns
                        #{'id': 'Invested Amount', 'type': 'numeric','format': FormatTemplate.money(0)}
                    ],
                    style_as_list_view=True,
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    style_cell_conditional=[
                        {
                            'if': {'column_id': c},
                            'type': 'numeric',
                            'format': FormatTemplate.money(0)
                        } for c in ['Unit Cost', 'MarketPrice', 'Invested Amount', 'Valuated Amount']
                    ]
                    )),
    html.Div(id='dt-position-container')])
