'''
Created on 4 nov. 2018

@author: afunes
'''

from dash.dependencies import Output, Input, State

from base.dumpexporter import DumpExporter
import dash_bootstrap_components as dbc
import dash_html_components as html
from web.app import app


layout = dbc.Container([
            dbc.Row([dbc.Col(html.Button(id='btn-submit', n_clicks=0, children='Submit', style = {'margin': 5}))]),
            dbc.Row([]),
            html.Div(id = 'div-hidden')
        ],style={"max-width":"80%"})

@app.callback(
    Output('div-hidden', "children"),
    [Input('btn-submit', 'n_clicks')])
def doSubmit(n_clicks):
    if (n_clicks > 0):
        DumpExporter().exportAllDump()
    

