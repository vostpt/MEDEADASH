# -*- coding: utf-8 -*-
# author: Jorge Gomes for VOST Portugal

# ------------------------------
#      VERSIONS
# ------------------------------

# V 0.1 11 OCTOBER 2022 

# CONFIRM MEDEA DASHBOARD  - BOILERPLATE ONLY

# ------------------------------
#       IMPORT LIBRARIES
# ------------------------------

# IMPORT STANDARD LIBREARIES 


import json
import requests
import pandas as pd 
import datetime as dt 
from datetime import datetime, timedelta, date 

# IMPORT PLOTLY LIBRARIES ------------

import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

# IMPORT DASH LIBRARIES ------------
import dash
import dash_daq as daq
from dash import Input, Output, dcc, html
import dash_mantine_components as dmc


# ------------------------------
#      START DASH APP
# ------------------------------

app = dash.Dash(__name__,title='VOST PORTUGAL',suppress_callback_exceptions=True,update_title=None,
    external_stylesheets=[
        # include google fonts
        "https://fonts.googleapis.com/css2?family=Inter:wght@100;200;300;400;500;900&display=swap"
    ],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    )

app.css.config.serve_locally = True
app.scripts.config.serve_locally = True

# ------------------------------
#      START APP LAYOUT
# ------------------------------

app.layout = html.Div(
    [
        dmc.Grid(
            children=[
                
                dmc.Col(
                        dmc.Text(
                            "VOST Portugal",
                            weight=700,
                            variant="gradient",
                            gradient={"from":"green", "to":"orange","deg":45},
                            style={"fontSize":24},
                            align="left",
                        ),
                span=1,xs=12,
                ),
                dmc.Col(
                        dmc.Text(
                            "MEDEA DASHBOARD",
                            variant="gradient",
                            gradient={"from":"orange", "to":"red","deg":45},
                            style={"fontSize":24},
                            align="right",
                        ),
                span=2,xs=12,offset=6,
                ),
            ],
        ),
          
    ],
)

 # -------------------------------------------------------------------------------------
# --------------------------------  START THE APP -------------------------------------
# -------------------------------------------------------------------------------------

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=False)


