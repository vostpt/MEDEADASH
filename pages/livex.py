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
import math 

# Import Dash and Dash Bootstrap Components
import dash
import dash_daq as daq
from dash import Input, Output, dcc, html, dash_table, callback
import dash_bootstrap_components as dbc

# -----------------------------------------------
#                   CARD STYLING 
# -----------------------------------------------

card_head_style = {"background": "#273B80","color":"white"}
card_text_style = {"color":"#273B80","font":"bold"}
card_exit_head_style = {"background": "#EE1C24","color":"white"}
card_exit_text_style = {"color": "#EE1C24","font":"bold"}

# -----------------------------------------------
#                   CARD STYLING 
# -----------------------------------------------



layout = html.Div(
	[
		dbc.Row(html.Img(src='/assets/topbar.png')),
		html.Hr(),
		
		dbc.Row(
			[
			# AUTOMATIC UPDATER
				dcc.Interval(
					id='cards_updater_live',
					interval=50 * 1000,  # in milliseconds
					n_intervals=0
				),
			dbc.Col(
				[
				dbc.Card(
					[
					dbc.CardHeader("NUMBER OF REPORTS", style=card_head_style),
					dbc.CardBody(
						[
						html.H4(id="var_total_reports_live",style=card_text_style),
						],

						),
					],
					),
				], xs=12, sm=12, md=6, lg=3, xl=3
				),
			dbc.Col(
				[
				dbc.Card(
					[
					dbc.CardHeader("FIREFIGHTERS", style=card_exit_head_style),
					dbc.CardBody(
						[
						html.H4(id="var_total_firefighters_live",style=card_exit_text_style),
						],

						),
					],
					),
				], xs=12, sm=12, md=6, lg=3, xl=3
				),
			dbc.Col(
				[
				dbc.Card(
					[
					dbc.CardHeader("VEHICULES", style=card_exit_head_style),
					dbc.CardBody(
						[
						html.H4(id="var_total_cars_live",style=card_exit_text_style),
						],

						),
					],
					),
				], xs=12, sm=12, md=6, lg=3, xl=3
				),
			dbc.Col(
				[
					dbc.Card(
						[
						dbc.CardHeader("PLANES", style=card_exit_head_style),
						dbc.CardBody(
							[
							html.H4(id="var_total_planes_live",style=card_exit_text_style),
							],

							),
						],
						),
					], xs=12, sm=12, md=6, lg=3, xl=3
					),
				],
			),
		html.Hr(),
		dbc.Row(
			[
				# AUTOMATIC UPDATER
				dcc.Interval(
					id='table_updater_live',
					interval=50 * 1000,  # in milliseconds
					n_intervals=0
				),

				dbc.Col(
					dcc.Loading(
						id='loader_timeline',
						type='dot',
						color='#273B80', 	
						children=[
							dbc.Col(
								id='timeline_table_live',
								xs=12, sm=12, md=12, lg=12, xl=12
							),
						], 
					),
				xs=12, sm=12, md=12, lg=12, xl=12,
				),
			],
		),
		dbc.Row(
			[
				# AUTOMATIC UPDATER
				dcc.Interval(
					id='graph_updater_live',
					interval=100 * 1000,  # in milliseconds
					n_intervals=0
				),

				dbc.Col(
					dcc.Loading(
						id='loader_timeline_live',
						type='dot',
						color='#273B80', 	
						children=[
							dcc.Graph(id='fire_timeline_live'),
						], 
					),
				xs=12, sm=12, md=12, lg=12, xl=12,
				),
			],
		),
	],
)


@callback(
	
	
	Output(component_id="var_total_reports_live", component_property="children"), 
	Output(component_id="var_total_firefighters_live", component_property="children"),   
	Output(component_id="var_total_cars_live", component_property="children"),  
	Output(component_id="var_total_planes_live", component_property="children"),  
	Input(component_id="cards_updater_live", component_property="n_intervals"),
	)

# WHAT HAPPENS WHEN CALL BACK IS TRIGGERED
def confirm_update_cards(value):
	
	# DATA TREATMENT 

	df_expanded_timeline = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRNKtgbUZQYmuYeSiBxu-Y48ox1aW6b_SaKCfuG2RPVL9eRN9Z8ndr6UL_ZQ5tQU4BrluEPGKc8waM2/pub?gid=1637668700&single=true&output=csv')
	
	df_expanded_timeline['Timestamp'] = pd.to_datetime(df_expanded_timeline['Timestamp'])

	total_reports = str(len(df_expanded_timeline.index))

	df_operationals = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTGCDOlWzYjWL_ri9S0CT2PlzHBYIu9rruyWGiqfDXQxqXQHhmL6nyZpyqDpt7KLiZpXqX6o8PUH7Rz/pub?gid=365135146&single=true&output=csv')
	total_firefighters = str(df_operationals['FIREFIGHTERS'].iloc[0])
	total_cars = str(df_operationals['VEHICLES'].iloc[0])
	total_planes = str(df_operationals['PLANES'].iloc[0])

	df_in_line = df_expanded_timeline.groupby(['Timestamp','ENTITY'],as_index=False)['TARGET'].nunique()
	df_half = df_in_line.resample('30min', on='Timestamp', offset='01s').ENTITY.count().to_frame().reset_index()

	figure_timeline = px.line(df_in_line,x='Timestamp',y='ENTITY',template='plotly_white',labels={"Timestamp":"DATE","ENTITY":"Number of Reports"})
	figure_timeline.update_xaxes(nticks=5)

	return total_reports, total_firefighters, total_cars, total_planes


@callback(
	Output(component_id="fire_timeline_live", component_property="figure"),
	Input(component_id="graph_updater_live", component_property="n_intervals"),
)

def confirm_update_graph(value):

	df_expanded_timeline = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRNKtgbUZQYmuYeSiBxu-Y48ox1aW6b_SaKCfuG2RPVL9eRN9Z8ndr6UL_ZQ5tQU4BrluEPGKc8waM2/pub?gid=1637668700&single=true&output=csv')
	
	df_expanded_timeline['Timestamp'] = pd.to_datetime(df_expanded_timeline['Timestamp'])

	df_in_line = df_expanded_timeline.groupby(['Timestamp','ENTITY'],as_index=False)['TARGET'].nunique()
	df_half = df_in_line.resample('30min', on='Timestamp', offset='01s').ENTITY.count().to_frame().reset_index()

	figure_timeline = px.line(df_half,x='Timestamp',y='ENTITY',template='plotly_white',labels={"Timestamp":"DATE","ENTITY":"Number of Reports"})
	figure_timeline.update_xaxes(nticks=5)

	return figure_timeline


@callback(
	Output(component_id="timeline_table_live",component_property="children"),
	Input(component_id="table_updater_live",component_property="n_intervals"),

)

def confirm_update_table(value):
	
	df_expanded_timeline = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vRNKtgbUZQYmuYeSiBxu-Y48ox1aW6b_SaKCfuG2RPVL9eRN9Z8ndr6UL_ZQ5tQU4BrluEPGKc8waM2/pub?gid=1637668700&single=true&output=csv')


	df_expanded_timeline = df_expanded_timeline.sort_values(by='Timestamp',ascending=False)
	confirm_table = dash_table.DataTable(

		data=df_expanded_timeline.to_dict('records'),                                        
		columns=[                                                                   
					{'name':'Date', 'id':'Timestamp'},                                    
					{'name':'Entity', 'id':'ENTITY'},      
					{'name':'Message', 'id':'MESSAGE'},        		
				],
		fixed_rows={'headers': True},                                               
		style_table={'height': 350},                                               

		style_cell_conditional=[                                                    
			{'if': {'column_id': 'Timestamp'},                                           
			'width': '0.5%','textAlign': 'left'},
			 {'if': {'column_id': 'ENTITY'},                                
			 'width': '5%'},
			{'if': {'column_id': 'MESSAGE'},                                
			'width': '5%'},
			{'if': {'column_id': 'opstatus'},                                       
			'width': '1%','textAlign': 'center'},
			],

		style_as_list_view=True,                                                   
		style_header={'backgroundColor': 'rgb(39,59,128)','fontSize':18,'font-family':'sans-serif'},                     
		style_cell={                                                               
			'backgroundColor': 'rgb(39, 58, 128)',                               
			'color': '#FFFFFF',                                                     
			'fontSize':16, 'font-family':'Lato-Bold, Open Sans, sans-serif',        
			},
		page_size=10,                                                               
		)

	return confirm_table
