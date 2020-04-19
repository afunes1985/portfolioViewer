import logging

from dash.dependencies import Input, Output

from base.initializer import Initializer
from core.constant import Constant
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from tools.tools import createLog
from web.app import app
from web.apps import app1, app2


Initializer()

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Portfolio Viewer", className="ml-2")),
                    dbc.Col(dcc.Link("PnL Report", href="/apps/app2")),
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
    elif pathname == '/apps/app2':
        return app2.layout
    else:
        return app1.layout

if __name__ == '__main__':
    logging.info("START")
    createLog(Constant.LOGGER_IMPORT_GENERAL, logging.DEBUG)
    app.run_server(debug=True, port=8051)