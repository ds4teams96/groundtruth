import dash
import dash_bootstrap_components as dbc
import flask

server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__, suppress_callback_exceptions=False, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                server=server
                )
                
#server = app.server
