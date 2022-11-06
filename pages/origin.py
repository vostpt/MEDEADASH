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
	dbc.Row(html.Img(src='/assets/topbar.png')),
	html.Hr(),
	dbc.Row(html.H6(id="last_update_origin",style={"color":"#273B80"}),),
	dbc.Row(
		[
						# AUTOMATIC UPDATER
						dcc.Interval(
							id='interval-component',
								interval=10000 * 1000,  # in milliseconds
								n_intervals=0
								),
						dbc.Col(html.Div(
							dcc.Loading(id='loader_bar_graph',
								type='dot',
								color='#273B80', 	
								children=[
								dcc.Graph(id="bar_graph"),
								],

								),
							),
						),


						],
						className="h-30",
						),

	dbc.Row(
		[
		dbc.Col(html.Div(
			dcc.Loading(id='loader_piegraph',
				type='dot',
				color='#273B80', 	
				children=[
				dcc.Graph(id='pie_graph'),
				], 
				),
			),
		),
		],
		className="h-70",
		),
	dbc.Row(
		[
		dbc.Col(html.Div(
			dcc.Loading(id='loader_linegraph',
				type='dot',
				color='#273B80', 	
				children=[
				dcc.Graph(id='line_graph'),
				], 
				),
			),
		),
		],
		className="h-70",
		),
	html.Hr(),

	],
	)

@callback(
	Output(component_id="last_update_origin", component_property="children"),  
	Output(component_id="bar_graph", component_property="figure"),  # returns tab 2 bar graph
	Output(component_id="pie_graph", component_property="figure"),  # returns tab 2 pie graph
	Output(component_id="line_graph", component_property="figure"),  # returns tab 2 line graph

	Input(component_id="interval-component", component_property="n_intervals"),
	)

# WHAT HAPPENS WHEN CALL BACK IS TRIGGERED
def confirm_update(value):
	# ________________________________________
	# DATA TREATMENT

	# Import latest data - Citizenships - entry 
	df = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=0&single=true&output=csv')

	

	# From Wide to Long using pandas melt
	df_filtered = pd.melt(df, id_vars=['country', 'region'], var_name='date', value_name='refugees')

	# Data Treatment: get rid of N/A values
	df_filtered['refugees'] = df_filtered['refugees'].fillna(0)

	# Create Dataframe with the totals per country
	df_totals = df_filtered.groupby(["country", "region"]).refugees.sum().reset_index()

	# Create Variable with the total of refugees
	total_refugees = df_totals['refugees'].sum()

	# Create a dataframe with the last of row of the filtered dataframe
	df_last_update = df_filtered.tail(1).reset_index()

	# Create variable with the latest date
	last_update = str(df_last_update.at[0, 'date'])
	last_update_text = "Aktualizované k dátumu: "
	last_update_return = last_update_text + last_update

	# Create Dataframe only for Ukranian Citizens
	df_ua = df_filtered.loc[(df_filtered['country'] == 'Ukraine')]

	# Create Color Map
	color_map = {"Europe": "#005c8d",
	"Middle east": "#646ffa",
	"Asia & Pacific": "#1177a7",
	"South/Latin America": "#588bff",
	"Africa": "#565182",
	"European Union": "#60b2ff",
	"Arab States": "#534798",
	"North America": "#94b5ea",
	"South/Central America": "#DCC48E",
	"Russia": "#EF1C24",
	"Ukraine": "#273B80",
	}

	# CREATE BAR GRAPH
	fig_bar = px.bar(df_filtered, x='date', y='refugees', color='region', template='plotly_white', hover_name="country",
		color_discrete_map=color_map, custom_data=['country'],labels={"region":"OBČIANSTVO / Region","date":"Dátum / Date","refugees":"Celkom / Total"})
	fig_bar.update_xaxes(tickangle=45, tickfont=dict(color='black', size=7))
	fig_bar.update_yaxes(tickangle=45, tickfont=dict(color='black', size=9))
	fig_bar.update_xaxes(nticks=5)
	fig_bar.update_traces(hovertemplate="Datúm:  %{x}<br><b>%{customdata[0]}</b><br><b>Celkom: %{y}</b>")
	fig_bar.update_layout(
		height=500,
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
		)   
	fig_bar.update_xaxes(rangeslider_visible=True)


	# CREATE DONUT CHART
	fig_pie = px.pie(df_totals, names='region', values='refugees', hole=0.5, color='region',
		labels={"region":"OBČIANSTVO / Region"},
		color_discrete_map=color_map,custom_data=['region','refugees'])
	
	# Donut Chart Styling
	fig_pie.update_traces(textposition='inside')
	fig_pie.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
	fig_pie.update_traces(hovertemplate="<b>Okres:</b>  %{customdata[0]}<br><b>Celkom:</b> %{customdata[1]}")
	fig_pie.update_layout(
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
		)   

	# CREATE LINE GRAPH
	fig_line = px.line(df_ua, x='date', y='refugees', color='region', template='plotly_white',
		color_discrete_map=color_map, line_shape='spline', render_mode='svg',labels={"region":"OBČIANSTVO / Region","date":"Dátum / Date","refugees":"Celkom / Total"})
	fig_line.update_xaxes(tickangle=45, tickfont=dict(color='black', size=9))
	fig_line.update_yaxes(tickangle=45, tickfont=dict(color='black', size=9))
	fig_line.update_xaxes(nticks=5)
	fig_line.update_traces(hovertemplate="Datúm:  %{x}<br><b>Celkom: %{y}</b>")
	fig_line.update_layout(
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
		)

	fig_line.update_xaxes(rangeslider_visible=True)


	return last_update_return, fig_bar, fig_pie, fig_line 






