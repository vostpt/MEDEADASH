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
import plotly.express as px 
import json 

# Import Dash and Dash Bootstrap Components
import dash
import dash_daq as daq
from dash import Input, Output, dcc, html, dash_table, callback
import dash_bootstrap_components as dbc


# LAYOUT 

layout = html.Div(
	[
		dbc.Row(html.Img(src='/assets/topbar.png')),
		html.Hr(),
		
		dbc.Row(
			[
			# AUTOMATIC UPDATER
				dcc.Interval(
					id='maps_updater_live',
					interval=50 * 1000,  # in milliseconds
					n_intervals=0
				),
			],
		),
		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("GRAVENSON"),
						html.Div(
							dcc.Loading(
								id='graveson_loader',
								type='dot',
								color='#0F55A1',  
								children=[
									dcc.Graph(id="graveson_map"),
								],
							),
						),
					],
				xs=12, sm=12, md=12, lg=12, xl=6 
				),
				
				dbc.Col(
					[
						html.H3("BOULBON"),
						html.Div(
							dcc.Loading(
								id='boulbon_loader',
								type='dot',
								color='#0F55A1',  
								children=[
									dcc.Graph(id="boulbon_map"),
								],
							),
						),
					],
				xs=12, sm=12, md=12, lg=12, xl=6 
				),
			],
		),
		html.Hr(),
		dbc.Row(
			[
				dbc.Col(
					[
						html.H3("BARBENTANE"),
						html.Div(
							dcc.Loading(
								id='barbentane_loader',
								type='dot',
								color='#0F55A1',  
								children=[
									dcc.Graph(id="barbentane_map"),
								],
							),
						),
					],
				xs=12, sm=12, md=12, lg=12, xl=6 
				),
			],
		),
	],
)

@callback(
  Output(component_id="graveson_map", component_property="figure"),  
  Input(component_id="maps_updater_live", component_property="n_intervals"), 
)

def maps_update_gravenson(value):
	
	with open('assets/GRAVESON.geojson') as response:
		graveson_geo = json.load(response)
		


	df_evacs = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTGCDOlWzYjWL_ri9S0CT2PlzHBYIu9rruyWGiqfDXQxqXQHhmL6nyZpyqDpt7KLiZpXqX6o8PUH7Rz/pub?gid=701738636&single=true&output=csv')

	gravenson = px.choropleth_mapbox(df_evacs, geojson=graveson_geo,locations='AREA',featureidkey='properties.Name',color='CAPACITY',
									color_continuous_scale=[(0, "#00D26A"), (0.5, "#FCD53F"),(0.70, "#FF6723"),(1, "#F8312F")],                         
									mapbox_style="carto-positron",
									center=dict(lat=43.85264527627229, lon=4.7705014871076905),
									zoom=18,
									opacity=0.8,
									range_color=[0,100],
									height=300
	)

	gravenson.update_layout(margin={"r":15,"t":0,"l":15,"b":0},coloraxis_showscale=False)


	gravenson.update_layout(
	  hoverlabel=dict(
		bgcolor="#273B80",
		font_size=16,
		font_family="sans-serif"
		)
	)

	return gravenson

@callback(
  Output(component_id="boulbon_map", component_property="figure"),  
  Input(component_id="maps_updater_live", component_property="n_intervals"), 
)

def maps_update_gravenson(value):
	
	with open('assets/BOULBON.geojson') as response:
		boulbon_geo = json.load(response)
		


	df_evacs = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTGCDOlWzYjWL_ri9S0CT2PlzHBYIu9rruyWGiqfDXQxqXQHhmL6nyZpyqDpt7KLiZpXqX6o8PUH7Rz/pub?gid=701738636&single=true&output=csv')

	boulbon = px.choropleth_mapbox(df_evacs, geojson=boulbon_geo,locations='AREA',featureidkey='properties.Name',color='CAPACITY',
									color_continuous_scale=[(0, "#00D26A"), (0.5, "#FCD53F"),(0.70, "#FF6723"),(1, "#F8312F")],                         
									mapbox_style="carto-positron",
									center=dict(lat=43.86135580176815, lon=4.69157169080373),
									zoom=18,
									opacity=0.8,
									range_color=[0,100],
									height=300
	)

	boulbon.update_layout(margin={"r":15,"t":0,"l":15,"b":0},coloraxis_showscale=False)


	boulbon.update_layout(
	  hoverlabel=dict(
		bgcolor="#273B80",
		font_size=16,
		font_family="sans-serif"
		)
	)

	return boulbon

@callback(
  Output(component_id="barbentane_map", component_property="figure"),  
  Input(component_id="maps_updater_live", component_property="n_intervals"), 
)

def maps_update_barbentane(value):
	
	with open('assets/BARBENTANE.geojson') as response:
		barbentane_geo = json.load(response)
		


	df_evacs = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTGCDOlWzYjWL_ri9S0CT2PlzHBYIu9rruyWGiqfDXQxqXQHhmL6nyZpyqDpt7KLiZpXqX6o8PUH7Rz/pub?gid=701738636&single=true&output=csv')

	barbentane = px.choropleth_mapbox(df_evacs, geojson=barbentane_geo,locations='AREA',featureidkey='properties.Name',color='CAPACITY',
									color_continuous_scale=[(0, "#00D26A"), (0.5, "#FCD53F"),(0.70, "#FF6723"),(1, "#F8312F")],                         
									mapbox_style="carto-positron",
									center=dict(lat=43.901470921942476, lon=4.754010991405127),
									
									zoom=18,
									opacity=0.8,
									range_color=[0,100],
									height=300
	)

	barbentane.update_layout(margin={"r":15,"t":0,"l":15,"b":0},coloraxis_showscale=False)


	barbentane.update_layout(
	  hoverlabel=dict(
		bgcolor="#273B80",
		font_size=16,
		font_family="sans-serif"
		)
	)

	return barbentane
