'''
Created on 4 nov. 2018

@author: afunes
'''

from datetime import datetime

import dash
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate
from dash_table import FormatTemplate

from core.cache import MainCache
from core.constant import Constant
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from engine.movementEngine import MovementEngine
from engine.positionEngine import PositionEngine
from web.app import app

assetTypeOptions = MovementEngine().getAssetTypeList()
custodyOptions = MovementEngine().getCustodyList()
ddAssetType = dcc.Dropdown(
    id='dd-assetType',
    value=None,
    clearable=False,
    options=assetTypeOptions
)

ddAsset = dcc.Dropdown(
    id='dd-asset',
    value=None,
    clearable=False
)

ddCustody = dcc.Dropdown(
    id='dd-custody',
    value=None,
    clearable=False,
    options=custodyOptions
)

ddBuySell = dcc.Dropdown(
    id='dd-buySell',
    value=None,
    clearable=False
)

riByAmount = dcc.RadioItems(
    id='ri-ByAmount',
    options=[
        {'label': 'By Quantity', 'value': 'BY_QUANTITY'},
        {'label': 'By Amount', 'value': 'BY_AMOUNT'}
    ],
    value='BY_QUANTITY'
)  

today = datetime.now().date()
dps_acquisitionDate = dcc.DatePickerSingle(
    id='dps-acquisitionDate',
    max_date_allowed=today,
    display_format='YYYY-MM-DD',
    date=today
)

modal = dbc.Modal(
                    [
                        dbc.ModalHeader("Add Movement"),
                        dbc.ModalBody(
                            dbc.Container([  
                                dbc.Row([ dbc.Col(html.Label("Asset Type", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(ddAssetType)]),
                                dbc.Row([ dbc.Col(html.Label("Asset", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(ddAsset)]),
                                dbc.Row([ dbc.Col(html.Label("Custody", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(ddCustody)]),
                                dbc.Row([ dbc.Col(html.Label("Buy Sell", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(ddBuySell)]),
                                dbc.Row([ dbc.Col(riByAmount)]),
                                dbc.Row([ dbc.Col(html.Label("Gross Amount", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dbc.Input(id='input-grossAmount', type="number", min=0, step=0.01))]),
                                dbc.Row([ dbc.Col(html.Label("Acquisition Date", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dps_acquisitionDate)]),
                                dbc.Row([ dbc.Col(html.Label("Quantity", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dbc.Input(id='input-quantity', type="number", min=0, step=1))]),
                                dbc.Row([ dbc.Col(html.Label("Price", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dbc.Input(id='input-price', type="number", min=0, step=1))]),
                                dbc.Row([ dbc.Col(html.Label("Rate", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dbc.Input(id='input-rate', type="number", min=0, max=10, step=0.01))]),
                                dbc.Row([ dbc.Col(html.Label("Net Amount", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dbc.Input(id='input-netAmount', type="number", min=0, step=1, disabled=True))]),
                                dbc.Row([ dbc.Col(html.Label("Commission Percentage", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dbc.Input(id='input-commissionPercentage', type="number", min=0, max=1, step=0.0001))]),
                                dbc.Row([ dbc.Col(html.Label("Commission Amount", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dbc.Input(id='input-commissionAmount', type="number", min=0, step=1, disabled=True))]),
                                dbc.Row([ dbc.Col(html.Label("Commission VAT Amount", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dbc.Input(id='input-commissionVATAmount', type="number", min=0, step=1, disabled=True))]),
                                dbc.Row([ dbc.Col(html.Label("Tenor", style={'margin': 5}), width={"size": 6}),
                                                dbc.Col(dbc.Input(id='input-tenor', type="number", min=0, step=1))]),
                            ])
                        ),
                        dbc.ModalFooter(
                            dbc.Row([dbc.Button("Save", id="save", className="ml-auto", style={'margin': 5}),
                                    dbc.Button("Close", id="close", className="ml-auto", style={'margin': 5})])
                        ),
                    ],
                    id="modal",
                )

formatColumns = [{"name": 'Asset Name', 'id': 'Asset Name', "deletable": False},
#                  {"name": 'Asset Type', 'id': 'Asset Type', "deletable": False},
                 {"name": 'Position', 'id': 'Position', "deletable": False, 'type': 'numeric'},
                 {"name": 'Unit Cost', 'id': 'Unit Cost', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.money(2)},
                 {"name": 'Market Price', 'id': 'Market Price', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.money(2)},
                 {"name": 'Change', 'id': 'Change', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.percentage(2)},
                 {"name": 'Invested Amount', 'id': 'Invested Amount', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.money(2)},
                 {"name": 'Valuated Amount', 'id': 'Valuated Amount', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.money(2)},
                 {"name": 'Tenor', 'id': 'Tenor', "deletable": False, 'type': 'numeric'},
#                 {"name": 'Maturity Date', 'id': 'Maturity Date', "deletable": False},
                 {"name": 'Gross PnL', 'id': 'Gross PnL', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.money(2)},
                 {"name": 'Net PnL', 'id': 'Net PnL', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.money(2)},
                 {"name": 'Gross%PNL', 'id': 'Gross%PNL', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.percentage(2)},
                 {"name": 'Net%PNL', 'id': 'Net%PNL', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.percentage(2)},
                 {"name": 'Realized PnL', 'id': 'Realized PnL', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.money(2)},
                 {"name": '%Portfolio', 'id': '%Portfolio', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.percentage(2)},
                 {"name": 'WeightedPnL%', 'id': 'WeightedPnL%', "deletable": False, 'type': 'numeric', 'format': FormatTemplate.percentage(2)}]

styleDataCondition = [{ 'if': {'column_id': 'Gross PnL', 'filter_query': '{Gross PnL} > 0'}, 'color': 'green', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Gross PnL', 'filter_query': '{Gross PnL} < 0'}, 'color': 'red', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Change', 'filter_query': '{Change} > 0'}, 'color': 'green', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Change', 'filter_query': '{Change} < 0'}, 'color': 'red', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Gross%PNL', 'filter_query': '{Gross%PNL} > 0'}, 'color': 'green', 'fontWeight': 'bold'},
                        {'if': {'column_id': 'Gross%PNL', 'filter_query': '{Gross%PNL} < 0'}, 'color': 'red', 'fontWeight': 'bold'}, ]

layout = dbc.Container([
            dbc.Row([dbc.Col(html.Button(id='btn-submit', n_clicks=0, children='Submit', style={'margin': 5})),
                     dbc.Col(html.Label("USD/MXN", style={'margin': 5}), width={"size": 1, "offset": 9}),
                     dbc.Col(html.Div(id='lbl-exchangeRate' , children='', style={'margin': 5}), width={"size": 1})]),
            dbc.Row([dbc.Col(html.Div(dt.DataTable(data=[{}], id='dt-position'), style={'display': 'none'}), width={"size": 0}),
                     dbc.Col(html.Div(id='dt-position-container', style={'width':'90%'}), width={"size": 12, "offset": 1})],
                     justify="center"),
            modal,
            dbc.Button("Open modal", id="open")
        ], style={"max-width":"100%"})


@app.callback(
    [Output('dd-asset', 'options'),
     Output('dd-buySell', 'options'),
     Output('input-rate', 'disabled'),
     Output('input-tenor', 'disabled'),
     Output('input-commissionPercentage', 'value')],
    [Input('dd-assetType', 'value')])
def updateDDAsset(assetType):
    assetList = MovementEngine().getAssetList(assetType)
    buySellList = Constant.BUY_SELL_IN_OUT_DICT.get(assetType, Constant.BUY_SELL_IN_OUT_DICT.get('OTHER'))
    inputBondDisabled = True
    if(assetType == 'BOND'):
        inputBondDisabled = False
    commissionPercentage = Constant.CONST_DEF_OTHER_COMMISSION_PERCENTAGE
    if(assetType == 'EQUITY'):
        commissionPercentage = Constant.CONST_DEF_EQUITY_COMMISSION_PERCENTAGE 
    return assetList, buySellList, inputBondDisabled, inputBondDisabled, commissionPercentage


@app.callback(
    Output('dd-custody', 'value'),
    [Input('dd-asset', 'value')])
def updateDDCustody(assetID):
    if assetID is not None:
        custody = MovementEngine().getCustodyByAssetID(assetID)
        return custody.ID

    
@app.callback(
    [Output('input-price', 'disabled'),
     Output('input-grossAmount', 'disabled')],
    [Input('ri-ByAmount', 'value')])
def updateRIByAmount(byAmount):
    if byAmount is not None:
        if(byAmount == 'BY_AMOUNT'):
            return True, False
        else:
            return False, True

        
@app.callback(
    [Output('input-grossAmount', 'value'),
     Output('input-netAmount', 'value'),
     Output('input-commissionAmount', 'value'),
     Output('input-commissionVATAmount', 'value')],
    [Input('input-price', 'value'),
     Input('input-quantity', 'value'),
     Input('input-commissionPercentage', 'value')],
    [State("ri-ByAmount", "value"),
     State('input-grossAmount', 'value')])
def calculateGrossAmount(price, quantity, commissionPercentage, byAmount, grossAmount2):
    print(price, quantity, commissionPercentage)
    if(byAmount == 'BY_QUANTITY'):
        if quantity is not None and price is not None:
            grossAmount = quantity * price
            commissionAmount = grossAmount * commissionPercentage
            commissionVATAmount = commissionAmount * Constant.CONST_IVA_PERCENTAGE
            netAmount = grossAmount - commissionAmount
            return grossAmount, netAmount, commissionAmount, commissionVATAmount
        else:
            raise PreventUpdate()
    elif(byAmount == 'BY_AMOUNT'):
        if grossAmount2 is not None:
            commissionAmount = grossAmount2 * commissionPercentage
            commissionVATAmount = commissionAmount * Constant.CONST_IVA_PERCENTAGE
            netAmount = grossAmount2 - commissionAmount
            return grossAmount2, netAmount, commissionAmount, commissionVATAmount
        else:
            raise PreventUpdate()
    else:
        raise PreventUpdate()

    
@app.callback(
    [Output('input-price', 'value')],
    [Input('input-quantity', 'value')],
    [State("input-grossAmount", "value"),
     State("ri-ByAmount", "value")])
def calculatePrice(quantity, grossAmount, byAmount):
    print(grossAmount, quantity)
    ctx = dash.callback_context
    print(ctx.triggered[0]['prop_id'])
    if(byAmount == 'BY_AMOUNT'):
        if grossAmount is not None and quantity is not None:
            price = grossAmount / quantity
            return [price]
        else:
            raise PreventUpdate()
    else:
            raise PreventUpdate()


@app.callback(
    Output("modal", "is_open"),
    [Input("open", "n_clicks"), Input("close", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    [Output('dt-position-container', "children"),
     Output('lbl-exchangeRate', "children")],
    [Input('btn-submit', 'n_clicks')])
def doSubmit(n_clicks):
    if (n_clicks > 0):
        MainCache.refreshReferenceData()
        df = PositionEngine().refreshPositions(datetime(2001, 7, 14).date(), datetime.now().date())
        if (len(df) != 0):
            dt2 = dt.DataTable(
                    id='dt-position',
                    data=df.to_dict("rows"),
                    columns=formatColumns,
                    style_as_list_view=True,
                    style_header={
                        'backgroundColor': 'white',
                        'fontWeight': 'bold'
                    },
                    # filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    style_data_conditional=styleDataCondition)
            return dt2, MainCache.usdMXN
    else:
        return None, None

