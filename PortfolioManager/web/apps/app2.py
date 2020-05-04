'''
Created on 4 nov. 2018

@author: afunes
'''

from datetime import datetime

from dash.dependencies import Output, Input, State
from dash_table import FormatTemplate

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from engine.pnlEngine import PnlEngine
from web.app import app


formatColumns = [{"name": 'Custody Name', 'id': 'Custody Name', "deletable": False},
                 {"name": 'Initial Position', 'id': 'Initial Position', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Final Position', 'id': 'Final Position', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Cash In', 'id': 'Cash In', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Cash Out', 'id': 'Cash Out', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'PnL', 'id': 'PnL', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'TIR', 'id': 'TIR', "deletable": False, 'type': 'numeric','format': FormatTemplate.percentage(2)}]
today = datetime.now().date()
dps_fromDate = dcc.DatePickerSingle(
        id='dps_fromDate',
        max_date_allowed=today,
        display_format='YYYY-MM-DD',
        date=datetime(today.year, 1, 1).date()
    )
dps_toDate = dcc.DatePickerSingle(
        id='dps_toDate',
        max_date_allowed=today,
        display_format='YYYY-MM-DD',
        date=today
    )

layout = dbc.Container([
            dbc.Row([dbc.Col(dps_fromDate, style = {'margin': 5}, width={"size": 2, "offset": 1}), 
                     dbc.Col(dps_toDate,style = {'margin': 5}, width={"size": 2, "offset": 1})]),
            dbc.Row([dbc.Col(html.Button(id='btn-submit', n_clicks=0, children='Submit', style = {'margin': 5}))]),
            dbc.Row([dbc.Col(html.Div(dt.DataTable(data=[{}], id='dt-pnl-report'), style={'display': 'none'}), width={"size": 0}),
                     dbc.Col(html.Div(id='dt-pnl-report-container', style = {'width':'90%'}), width={"size": 12,"offset": 1})],
                     justify="center")
        ],style={"max-width":"100%"})

@app.callback(
    Output('dt-pnl-report-container', "children"),
    [Input('btn-submit', 'n_clicks')],
    [State('dps_fromDate', "date"),
     State('dps_toDate', "date")])
def doSubmit(n_clicks, fromDate, toDate):
    if (n_clicks > 0):
        df = PnlEngine().calculatePnl(datetime.strptime(fromDate, '%Y-%m-%d').date(), datetime.strptime(toDate, '%Y-%m-%d').date())
        if (len(df) != 0):
            dt2 = dt.DataTable(
                    id='dt-pnl-report',
                    data=df.to_dict("rows"),
                    columns=formatColumns,
                    style_as_list_view=True,
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    #filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi")
            return dt2
    

