'''
Created on Apr 27, 2019

@author: afunes
'''
from datetime import datetime

import dash
from dash.dependencies import Output, Input
import dash_table
from pandas.core.frame import DataFrame
import dash_html_components as html
from engine.positionEngine import PositionEngine
import pandas as pd

#maincache = PositionEngine.refreshAll(datetime(2001, 7, 14).date(), datetime.now().date())
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')
#print(maincache.positionDict.items())
#print(maincache.positionDict.keys())
print(df)
#df.columns = maincache.positionDict.keys()

app = dash.Dash(__name__)

app.layout = html.Div([
    dash_table.DataTable(
        id='datatable-filtering-fe',
        #columns=[
        #    {"name": i, "id": i, "deletable": True} for i in df.columns
        #],
        data=df.to_dict('records'),
        filtering=True,
        style_cell={'fontSize':20, 'font-family':'sans-serif'}
    ),
    html.Div(id='datatable-filter-container')
])


@app.callback(
    Output('datatable-filter-container', "children"),
    [Input('datatable-filtering-fe', "data")])
def update_graph(rows):
    if rows is None:
        dff = df
    else:
        dff = DataFrame(rows)

    return dff


if __name__ == '__main__':
    app.run_server(debug=True)

    