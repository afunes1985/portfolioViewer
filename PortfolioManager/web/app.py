'''
Created on 4 nov. 2018

@author: afunes
'''
import dash
import dash_bootstrap_components as dbc

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_stylesheets = [dbc.themes.BOOTSTRAP]

app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = 'Portfolio Viewer'
