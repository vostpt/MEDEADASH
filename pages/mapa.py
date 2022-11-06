# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal


# -----------------------------------------------------
#                 DESCRIPTION
# -----------------------------------------------------
# This script deals with the summary on the front page


# -----------------------------------------------
#                  LIBRARIES
# -----------------------------------------------


# Import Core Libraries 
import pandas as pd
import numpy as np
import plotly.express as px

# Import Dash and Dash Bootstrap Components
import dash
import dash_daq as daq
from dash import Input, Output, dcc, html, dash_table, callback
import dash_bootstrap_components as dbc


layout = html.Div(
	[
		# AUTOMATIC UPDATER
		dcc.Interval(
			id='interval-component',
			interval=10000 * 1000,  # in milliseconds
			n_intervals=0
		),
		dbc.Row(html.Img(src='/assets/topbar.png')),
		html.Hr(),
		dbc.Row(
				[
				dbc.Col(
						dcc.Loading(id='loader_citizens',
									type='dot',
                                	color='#273B80', 	
                                	children=[
												dcc.Graph(id='map_graph'),
									], 
									),
				xs=12, sm=12, md=12, lg=12, xl=12,
				),
				],
		),
	],
)

@callback(
	Output(component_id="map_graph",component_property="figure"),
	#Output(component_id="table",component_property="children"), 

	Input(component_id="interval-component", component_property="n_intervals"),
)

# WHAT HAPPENS WHEN CALL BACK IS TRIGGERED
def confirm_update(value):

	# -----------------------------------------------
	#               DATA TREATMENT
	# -----------------------------------------------

	df_raw = pd.read_csv(
		'https://docs.google.com/spreadsheets/d/e/2PACX-1vTSnUP4UWex1vuhJ_cyMk81bSyD7ez1CKUcNd_NBKky'
		'-Wbz3tnYeTpVGddpv7f4qMc4dCrgmgTiIyXr/pub?gid=0&single=true&output=csv')
	df_map_tab = pd.melt(df_raw, id_vars=['center', 'total_capacity'], var_name='date', value_name='occupancy')
	df_latest_map_tab = df_map_tab.tail(11)
	df_latest_map = df_latest_map_tab.tail(11)

	df_map = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTSnUP4UWex1vuhJ_cyMk81bSyD7ez1CKUcNd_NBKky-Wbz3tnYeTpVGddpv7f4qMc4dCrgmgTiIyXr/pub?gid=65156759&single=true&output=csv')

	map_dataframe = pd.merge(df_latest_map, df_map, on ='center', how ='inner')

	print(map_dataframe.info())

	fig_map = px.scatter_mapbox(map_dataframe, lat="lat", lon="lon",
		color="total_capacity", size="total_capacity",
		color_continuous_scale=["#ee5f5a","#f89406","yellow","#61c462"],
		center=dict(lon=20.0068, lat=48.8264),
		zoom=6,
		size_max=15,
		height=800,
		custom_data=['center','total_capacity','occupancy','phone_number']
		)

	# Update hover_label background color, font-size, and font-family
	fig_map.update_layout(
		hoverlabel=dict(
			bgcolor="#272b30",
			font_size=16,
			font_family="Open Sans, sans-serif")
		)
	

	# Hide Color Scale. It usually appears next to the map. 
	fig_map.update_layout(coloraxis_showscale=False)
	# Choose Map Layout 
	fig_map.update_layout(mapbox_style="stamen-toner")
	# Update ToolTip
	fig_map.update_traces(hovertemplate="<b>%{customdata[0]}</b><br><b>Celková kapacita: %{customdata[1]}</b><br><b>Obsadené: %{customdata[02]}")

	return fig_map

