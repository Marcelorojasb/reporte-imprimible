# -*- coding: utf-8 -*-
import dash
from dash import dcc, html
from PIL import Image
import pandas as pd
import pathlib
from utils import Header
from flask_caching import Cache
import flask
from environment.settings import APP_HOST, APP_PORT, APP_DEBUG, DEV_TOOLS_PROPS_CHECK

# get relative data folder
PATH = pathlib.Path(__file__)
DATA_PATH = PATH.joinpath("../data").resolve()

server = flask.Flask(__name__) # define flask app.server

app = dash.Dash(__name__, server=server, use_pages=True, #2.0
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    prevent_initial_callbacks=True, 
    suppress_callback_exceptions=True,
)
app.title = "neocity-empresas"


# Describe the layout/ UI of the app
app.layout = html.Div([
        Header(app),
        html.Hr(className='no-print'),
        dash.page_container
])

if __name__ == "__main__":
    app.run_server(
        host=APP_HOST,
        port=APP_PORT,
        debug=APP_DEBUG,
        dev_tools_props_check=DEV_TOOLS_PROPS_CHECK
    )