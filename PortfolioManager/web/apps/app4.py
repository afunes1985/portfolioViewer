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
from web.app import app
from engine.movementEngine import MovementEngine

formatColumns = [{"name": 'Asset Name', 'id': 'Asset Name', "deletable": False},
                 {"name": 'Buy Sell', 'id': 'Buy Sell', "deletable": False},
                 {"name": 'Acquisition Date', 'id': 'Acquisition Date', "deletable": False},
                 {"name": 'Quantity', 'id': 'Quantity', "deletable": False, 'type': 'numeric'},
                 {"name": 'Price', 'id': 'Price', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Gross Amount', 'id': 'Gross Amount', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Net Amount', 'id': 'Net Amount', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Comm %', 'id': 'Comm %', "deletable": False, 'type': 'numeric','format': FormatTemplate.percentage(2)},
                 {"name": 'Comm Amount', 'id': 'Comm Amount', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Comm VAT Amount', 'id': 'Comm VAT Amount', "deletable": False, 'type': 'numeric','format': FormatTemplate.money(2)},
                 {"name": 'Custody', 'id': 'Custody', "deletable": False},
                 {"name": 'External ID', 'id': 'External ID', "deletable": False},
                 {"name": 'ID', 'id': 'ID', "deletable": False}]
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
            dbc.Row([dbc.Col(html.Div(dt.DataTable(data=[{}], id='dt-movement-report'), style={'display': 'none'}), width={"size": 0}),
                     dbc.Col(html.Div(id='dt-movement-report-container', style = {'width':'90%'}), width={"size": 12,"offset": 1})],
                     justify="center")
        ],style={"max-width":"100%"})

@app.callback(
    Output('dt-movement-report-container', "children"),
    [Input('btn-submit', 'n_clicks')],
    [State('dps_fromDate', "date"),
     State('dps_toDate', "date")])
def doSubmit(n_clicks, fromDate, toDate):
    if (n_clicks > 0):
        df = MovementEngine().getMovementsForReport(datetime.strptime(fromDate, '%Y-%m-%d').date(), datetime.strptime(toDate, '%Y-%m-%d').date())
        if (len(df) != 0):
            dt2 = dt.DataTable(
                    id='dt-movement-report',
                    data=df.to_dict("rows"),
                    columns=formatColumns,
                    style_as_list_view=True,
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi")
            return dt2
    

