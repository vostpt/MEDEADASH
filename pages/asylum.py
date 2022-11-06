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
		html.H4("ŽIADOSTI O AZYL"),
		html.Hr(),
		dbc.Row(html.H6(id="last_update_asylum",style={"color":"#273B80"}),),
		dbc.Row(
			[
				# AUTOMATIC UPDATER
				dcc.Interval(
					id='interval-asylum',
						interval=10000 * 1000,  # in milliseconds
						n_intervals=0
						),
				dbc.Col(html.Div(
					dcc.Loading(id='asylum_bar_graph',
						type='dot',
						color='#273B80', 	
						children=[
						dcc.Graph(id="asylum_graph"),
						],

						),
					),
				),


			],
		className="h-30",
		),

		],
	)

@callback(
	Output(component_id="last_update_asylum", component_property="children"),  
	Output(component_id="asylum_graph", component_property="figure"), 

	Input(component_id="interval-asylum", component_property="n_intervals"),
	)

# WHAT HAPPENS WHEN CALL BACK IS TRIGGERED
def confirm_update(value):
	# ________________________________________
	# DATA TREATMENT

	# Import latest data - Asylum  - entry 
	df_asylum = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=841026453&single=true&output=csv')
	df_asylum.columns = ['Štátna príslušnosť', 'Chlapci', 'Dievčatá', 'Muži','Ženy','Deti celkom','Dospelí celkom','Spolu','Dátum aktualizácie']

	last_update_asylum = df_asylum.tail(1).reset_index()
	last_update = str(last_update_asylum.at[0, 'Dátum aktualizácie'])
	last_update_text = "Aktualizované k dátumu: "
	last_update_return = last_update_text + last_update


	df_asylum_numbers = df_asylum.drop('Dátum aktualizácie',axis=1)
	df_asylum_melt = pd.melt(df_asylum_numbers, id_vars='Štátna príslušnosť',var_name='Skupina',value_name='Počet žiadostí o azyl')


	asylum_graph = px.bar(df_asylum_melt, x='Skupina',y='Počet žiadostí o azyl',color='Skupina',facet_col='Štátna príslušnosť',facet_col_wrap=4,template='plotly_white',height=1200,text_auto=True)
	asylum_graph.update_yaxes(matches=None)
	asylum_graph.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

	asylum_graph.update_traces(hovertemplate="%{x}<br><b>%{y}</b>")
	asylum_graph.update_layout(
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
	)

	


	return last_update_return, asylum_graph






