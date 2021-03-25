import logging

from dash.dependencies import Input, Output

from core.constant import Constant
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from tools.tools import createLog
from web.app import app
from web.apps import app1, app2, app3, app4

dropDownMenu = dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem(dcc.Link("Administration Tools", href="/apps/app3"))
            ],
            #nav=True,
            in_navbar=True,
            label="More"
        )

navbar = dbc.Navbar(
    [
        html.A(
            dbc.Row(
                [
                    dbc.Col(dbc.NavbarBrand("Portfolio Viewer", className="ml-2")),
                    dbc.Col(dcc.Link("Positions", href="/apps/app1")),
                    dbc.Col(dcc.Link("PnL Report", href="/apps/app2")),
                    dbc.Col(dcc.Link("Movement Report", href="/apps/app4")),
                    dbc.Col(dropDownMenu)
                ],
                align="center",
                justify="end"
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
    elif pathname == '/apps/app3':
        return app3.layout
    elif pathname == '/apps/app4':
        return app4.layout
    else:
        return app1.layout

if __name__ == '__main__':
    logging.info("START")
    createLog(Constant.LOGGER_IMPORT_GENERAL, logging.DEBUG)
    app.run_server(debug=True, port=8051)