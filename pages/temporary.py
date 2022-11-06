# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal


# -----------------------------------------------------
#                 DESCRIPTION
# -----------------------------------------------------
# This script deals with the temporary asylum data


# -----------------------------------------------
#                  LIBRARIES
# -----------------------------------------------


# Import Core Libraries 
import pandas as pd
import numpy as np
import plotly.express as px
import json

# Import Dash and Dash Bootstrap Components
import dash
import dash_daq as daq
from dash import Input, Output, dcc, html, dash_table, callback
import dash_bootstrap_components as dbc

# -----------------------------------------------
#                  CARD STYLE
# -----------------------------------------------

card_head_style = {"background": "#273B80","color":"white"}
card_text_style = {"color":"#273B80","font":"bold"}


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
		dbc.Col(html.H6(id="last_update_temporary",style={"color":"#273B80"}), xs=12, sm=10, md=6, lg=6, xl=3),
		dbc.Row(
			[
			dbc.Col(
				dcc.Loading(id='loader_temporary',
					type='dot',
					color='#273B80', 	
					children=[
					dcc.Graph(id='temporary_graph'),
					], 
					),
				xs=12, sm=12, md=12, lg=12, xl=12,
				),
			dbc.Col(
				dcc.Loading(id='loader_temporary',
					type='dot',
					color='#273B80', 	
					children=[
					dcc.Graph(id='temporary_world'),
					], 
					),
				xs=12, sm=12, md=12, lg=12, xl=12,
				),
			],
			),

		],className="g-0"
		)


@callback(
	Output(component_id="last_update_temporary", component_property="children"),  
	Output(component_id="temporary_graph",component_property="figure"), 
	Output(component_id="temporary_world",component_property="figure"), 
	Input(component_id="interval-component", component_property="n_intervals"),
	)

# WHAT HAPPENS WHEN CALL BACK IS TRIGGERED
def confirm_update(value):

	# -----------------------------------------------
	#               DATA TREATMENT
	# -----------------------------------------------

	# Import Data - Temporary Protection Daily

	df_temp_daily = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=779433687&single=true&output=csv')
	df_temp_daily = df_temp_daily.fillna(0)

	df_temp_daily_melt = pd.melt(df_temp_daily,id_vars='Dátum žiadosti',var_name='Dátum',value_name='Utečenci')

	df_last_update = df_temp_daily_melt.tail(1).reset_index()

	# Create variable with the latest date
	last_update = str(df_last_update.at[0, 'Dátum'])
	
	last_update_text = "Aktualizované k dátumu: "
	last_update_return = last_update_text + last_update


	temp_daily_map={"Muži - vek: 0 - 17" : "#005c8d",
	"Muži - vek: 18 - 65" : "#588bff",
	"Muži - vek: 66+" : "#646ffa",
	"Ženy - vek: 0 - 17" : "#B94C98",
	"Ženy - vek: 18 - 65" : "#D52A6A",
	"Ženy - vek: 66+" : "#F0073B",
	}

	fig_daily = px.scatter(df_temp_daily_melt,x='Dátum',y='Utečenci',color='Dátum žiadosti', template='plotly_white', color_discrete_map=temp_daily_map, 
		title='<b>Dočasné útočisko - denný prehľad</b>',
		labels={"Dátum žiadosti":"Vek a pohlavie"})
	fig_daily.update_traces(hovertemplate="<b>Dátum: %{x}</b><br><b>Utečenci: %{y}")
	fig_daily.update_layout(
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
		)

	fig_daily.update_xaxes(rangeslider_visible=True)
	fig_daily.update_xaxes(tickangle=0, tickfont=dict(color='black', size=7))
	fig_daily.update_yaxes(tickangle=90, tickfont=dict(color='black', size=7))
	fig_daily.update_xaxes(nticks=5)


	# Import Data - Temporary Protection 

	with open('assets/custom.geo.json') as response:
		countries = json.load(response)

	df_temp_all = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=777445378&single=true&output=csv")
	
	fig_total = px.choropleth_mapbox(df_temp_all, geojson=countries,locations='country',
                          featureidkey="properties.geounit",
                          color='total',
                          color_continuous_scale="Blues",
                          #range_color=(0, 12),
                          mapbox_style="carto-positron",
                          zoom=2, 
                          center=dict(lon=20.0068, lat=48.8264),
                          #center = {"lat": 37.0902, "lon": -95.7129},
                          opacity=0.5,
                          height=900,
                          custom_data=['Štátna príslušnosť','total']

                          )
	fig_total.update_traces(hovertemplate="<b>Dátum: %{customdata[0]}</b><br><b>Utečenci: %{customdata[1]}")

	return last_update_return, fig_daily, fig_total



