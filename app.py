# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal

# -----------------------------------------------
#                  LIBRARIES
# -----------------------------------------------


# Import Core Libraries 
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import date

# Import Dash and Dash Bootstrap Components
import dash
import dash_daq as daq
from dash import Input, Output, dcc, html, dash_table
import dash_bootstrap_components as dbc

from pages import final, livex


# -----------------------------------------------
#              APP STARTS HERE
# -----------------------------------------------





app = dash.Dash(__name__,title='CONFIRM - MEDEA PoC',external_stylesheets=[dbc.icons.FONT_AWESOME],suppress_callback_exceptions=True,update_title=None,
	meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
	)


app.css.config.serve_locally = False 
app.scripts.config.serve_locally = False 

server = app.server

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "21rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
    "background-color": "#FFFFFF",
}

today = date.today()

sidebar = html.Div(
    [
        html.Img(src='/assets/CONFIRM_Logotype.png',style={"width": "10rem"}),
        html.Hr(),
        dbc.Nav(
            [
            	# AUTOMATIC UPDATER
				dcc.Interval(
					id='interval-component',
					interval=10000 * 1000,  # in milliseconds
					n_intervals=0
				),
            	html.Hr(),
                
                dbc.NavLink("EXERCISE", href="/", active="exact"),
                dbc.NavLink("LIVE", href="/livex", active="exact"),
                dbc.NavLink("EVACUATION ZONES", href="/evac", active="exact"),
                dbc.NavLink("AREA OF INTEREST", href="/aoi", active="exact"),
                dbc.NavLink("FINAL", href="/final", active="exact"),
                dbc.NavLink("ABOUT", href="/about", active="exact"),
                html.Hr(),
                html.Hr(),
                html.Hr(),
                html.P(id='today',style={"color":"#D3D3D3"}),
                html.P("Developed by:",style={"color":"#273B80"}),
                html.Img(src='/assets/VOSTPT_LETTERS_2020.png',style={"width": "4rem","textAlign": "center"}),

            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


#def serve_layout():
#    return  html.Div([dcc.Location(id="url"), sidebar, content])

# -----------------------------------------------
#              APP LAYOUT DESIGN
# -----------------------------------------------

# 

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])



# -----------------------------------------------
#              APP CALLBACK
# -----------------------------------------------

@app.callback(
    Output("page-content", "children"), 
    [Input("url", "pathname"),], 
    prevent_initial_call=True
)

def render_page_content(pathname):
    if pathname == "/":
        return summary.layout
    elif pathname == "/livex":
        return livex.layout
    elif pathname == "/occupancy":
        return evac.layout
    elif pathname == "/aoi":
        return aoi.layout
    elif pathname == "/final":
        return final.layout
    elif pathname == "/about":
        return about.layout
    # If the user tries to reach a different page, return a 404 message
    return dbc.Card(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised...")
        ]
    )

@app.callback(
    Output('today','children'),
    [Input('interval-component','n_intervals')]

)

def whatistoday(n_intervals):
    today = date.today()
    return today 
# -------------------------------------------------------------------------------------
# --------------------------------  START THE APP -------------------------------------
# -------------------------------------------------------------------------------------

if __name__ == "__main__":
	app.run_server(host='0.0.0.0', debug=True)
