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
		dbc.Row(
			dbc.Col(
					dcc.Loading(id='loader_occupancy',
						type='dot',
						color='#273B80', 	
						children=[
							dcc.Graph(id='occupancy_graph'),
						], 
					),
			xs=12, sm=12, md=12, lg=12, xl=12,
			),
		),
		dbc.Row(
			[
			dbc.Col(
					[
					dbc.Card(
							[
							dbc.CardHeader("Total Beds",style=card_head_style),
							dbc.CardBody(
							[
							html.H6("Celková kapacita",className="card-title"),
							html.H4(id="var_total_beds",style=card_text_style),
							],   
							),
							dbc.CardFooter("Загальна місткість",style=card_head_style), 
							],
							
					),
					],
			xs=12, sm=12, md=3, lg=3, xl=3,
			),
			dbc.Col(
					[									
					dbc.Card(
							[
							dbc.CardHeader("Free Beds",style=card_head_style),
							dbc.CardBody(
										[
										html.H6("Voľné",className="card-title"),
										html.H4(id="var_free_beds",style=card_text_style),
										],   
							),
							dbc.CardFooter("Безкоштовні",style=card_head_style), 
							],
							color="#33B763", inverse=True,
					),
					],		
			xs=12, sm=12, md=3, lg=3, xl=3,
			),
			dbc.Col(
					[
					dbc.Card(
							[
							dbc.CardHeader("Occupied Beds",style=card_head_style),
							dbc.CardBody(
										[
										html.H6("Obsadené",className="card-title"),
										html.H4(id="var_occupied_beds"),
										],   
							),
							dbc.CardFooter("Безкоштовні",style=card_head_style), 
							],
							color="#273B80", inverse=True,
					),
					],
			xs=12, sm=12, md=3, lg=3, xl=3,
			),
			dbc.Col(
					[								
					dbc.Card(
							[
							dbc.CardHeader("Percentage Free",style=card_head_style),
							dbc.CardBody(
										[
										html.H6("Voľné v percentách",className="card-title"),
										html.H4(id="var_percentage_free"),
										],   
							),
							dbc.CardFooter("Відсоток безкоштовних",style=card_head_style), 
							],
							inverse=False,
					),
					],
			xs=12, sm=12, md=3, lg=3, xl=3,
										
			), 
					
		],
	
		),
	],className="g-0"
)


@callback(
	Output(component_id="occupancy_graph",component_property="figure"),
	Output(component_id="var_total_beds",component_property="children"),                    # returns variable
	Output(component_id="var_free_beds",component_property="children"),                     # returns variable
	Output(component_id="var_occupied_beds",component_property="children"),                 # returns variable
	Output(component_id="var_percentage_free",component_property="children"),  
	Input(component_id="interval-component", component_property="n_intervals"),
	)

# WHAT HAPPENS WHEN CALL BACK IS TRIGGERED
def confirm_update(value):

	# -----------------------------------------------
	#               DATA TREATMENT
	# -----------------------------------------------

	# Import Data - Occupancy_Numbers

	df_raw = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=432913788&single=true&output=csv')
	df_melt = pd.melt(df_raw, id_vars=['center', 'total_capacity'], var_name='date', value_name='occupancy')
	df_latest_melt = df_melt.tail(21)

	
	
	df_latest_melt['obsadený'] = round((df_latest_melt.occupancy / df_latest_melt.total_capacity) * 100, 2)
	df_latest_melt['neobsadený'] = (100 - df_latest_melt.obsadený)
	df_latest_melt_drop= df_latest_melt.drop(columns=["total_capacity", "date", "occupancy"])
	df_occupancy = pd.melt(df_latest_melt_drop, id_vars='center')

	occupancy_bar_graph = px.bar(df_occupancy, x='center', y='value',
		color='variable',
		text_auto=True,
		color_discrete_map={"obsadený": "#273B80", "neobsadený": "#33b864"},
		template='plotly_white',
		labels={
		"center": "Zariadenie",
		"value": "číslo (%)",
		"variable": "Legend"
		},
		)
	occupancy_bar_graph.update_traces(hovertemplate="<b>%{x}</b> <br><b>%{y} % ")
	occupancy_bar_graph.update_layout(
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
		)
	occupancy_bar_graph.update_yaxes(range=[-20, 120])

	# CARDS

	total_beds_num = df_latest_melt['total_capacity'].sum()
	total_beds_str = str(total_beds_num)

	occupied_beds_num = df_latest_melt['occupancy'].sum()
	occupied_beds_str = str(occupied_beds_num)

	free_beds_num = total_beds_num - occupied_beds_num
	free_beds_str = str(free_beds_num)

	percentage_free_beds_num = round(((free_beds_num/total_beds_num)*100),2)
	percentage_free_beds_number_str = str(percentage_free_beds_num)
	percentage_sign = " %"
	percentage_free_str = percentage_free_beds_number_str + percentage_sign

	return occupancy_bar_graph, total_beds_str, free_beds_str, occupied_beds_str, percentage_free_str




