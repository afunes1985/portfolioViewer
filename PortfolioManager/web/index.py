import logging

from dash.dependencies import Input, Output

from core.constant import Constant
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from tools.tools import createLog
from web.app import app
from web.apps import app1

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Portfolio Viewer", className="ml-2")),
                ],
                align="center",
                no_gutters=True,
            )
        ),
    ],
    color="dark",
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='navBar', children=navbar, style={"max-width":"100%"}),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/app1':
        return app1.layout
    else:
        return app1.layout

if __name__ == '__main__':
    logging.info("START")
    createLog(Constant.LOGGER_IMPORT_GENERAL, logging.DEBUG)
    app.run_server(debug=True, port=8051)