# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal


# -----------------------------------------------------
#                 DESCRIPTION
# -----------------------------------------------------
# This script deals with the human aid section


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
from dash_iconify import DashIconify
from babel.numbers import format_currency



# Card Icon 
# Solution provided by https://community.plotly.com/t/how-to-create-card-with-icon-on-the-right/51832/4

card_icon = {
	"color": "#005c8d",
	"textAlign": "center",
	"fontSize": 60,
	"margin": "auto",
}




card_head_style = {"background": "#273B80","color":"white"}
card_text_style = {"color":"#273B80","font":"bold"}



layout = html.Div(
	[
	dbc.Row(html.Img(src='/assets/topbar.png')),
	html.Hr(),
	dbc.Row(html.H6(id="last_update_humanaid",style={"color":"#273B80"}),),
	html.Hr(),
	html.H1("Humanitárna pomoc spracovaná v SK HUB",style={"color":"#273B80"}),
	dbc.Row(
		[
			dbc.Col(
				dbc.CardGroup(
						[
							dbc.Card(
								html.Div(DashIconify(icon="fa-solid:pallet"),style=card_icon),
								style={"maxWidth": 85,"color":"#005c8d","border": "none", "outline": "white"},
								),
							dbc.Card(
								dbc.CardBody(
									[
									html.H5("Množstvo",className="card-text border-0",style=card_text_style),
									html.H6(id="pallets",className="card-text")
									]   
									),style={"border": "none", "outline": "white"},
								),

						],
				),
			xs=3,
			),
			dbc.Col(
				dbc.CardGroup(
						[
							dbc.Card(
								html.Div(DashIconify(icon="healthicons:weight-negative"),style=card_icon),
								style={"maxWidth": 85,"color":"#646ffa","border": "none", "outline": "white"},
								),
							dbc.Card(
								dbc.CardBody(
									[
									html.H5("Hmotnosť",className="card-text border-0",style=card_text_style),
									html.H6(id="tons",className="card-text")
									]   
									),style={"border": "none", "outline": "white"},
								),

						],
				),
			xs=3,
			),

			dbc.Col(
				dbc.CardGroup(
						[
							dbc.Card(
								html.Div(DashIconify(icon="ri:money-euro-circle-fill"),style=card_icon),
								style={"maxWidth": 85,"color":"#1177a7","border": "none", "outline": "white"},
								),
							dbc.Card(
								dbc.CardBody(
									[
									html.H5("Deklarovaná cena",className="card-text border-0",style=card_text_style),
									html.H6(id="euros",className="card-text")
									]   
									),style={"border": "none", "outline": "white"},
								),

						],
				),
			xs=3,
			),

			dbc.Col(
				dbc.CardGroup(
						[
							dbc.Card(
								html.Div(DashIconify(icon="majesticons:map-simple-destination-line"),style=card_icon),
								style={"maxWidth": 85,"color":"#1177a7","border": "none", "outline": "white"},
								),
							dbc.Card(
								dbc.CardBody(
									[
									html.H5("Prijímateľ na UA",className="card-text border-0",style=card_text_style),
									html.P("Transcarpathian Regional Administration",className="card-text")
									]   
									),style={"border": "none", "outline": "white"},
								),

						],
				),
			xs=3,
			),

		],
	),
	dbc.Row(
		[
				# AUTOMATIC UPDATER
				dcc.Interval(
					id='interval-component',
					interval=10000 * 1000,  # in milliseconds
					n_intervals=0
				),
				dbc.Col(
					html.Div(
						dcc.Loading(id='loader_humanaid_graph',
							type='dot',
							color='#273B80', 	
							children=[
								dcc.Graph(id="humanaid_graph"),
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
	Output(component_id="last_update_humanaid", component_property="children"), 
	Output(component_id="pallets", component_property="children"), 
	Output(component_id="tons", component_property="children"), 
	Output(component_id="euros", component_property="children"), 
	Output(component_id="humanaid_graph", component_property="figure"),  
	Input(component_id="interval-component", component_property="n_intervals"),
	)

def confirm_update(value):

	# Define a color map for the main graph 

	humanaid_color_map = {
		"Počet dopravných prostriedkov (ks)": "#273B80",
		"Množstvo prepraveného tovaru (kg)": "#EE1C24",
	}

	# Data Treatment 

	df_human_aid = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=1964034340&single=true&output=csv')

	df_transit = df_human_aid.head(2)

	df_transit_melt = pd.melt(df_transit, id_vars=['Typ','Detail'],var_name='Dátum', value_name='Suma')

	df_last_update = df_transit_melt.tail(1).reset_index()

	# Create variable with the latest date
	last_update = str(df_last_update.at[0, 'Dátum'])
	last_update_text = "Aktualizované k dátumu: "
	last_update_return = last_update_text + last_update

	df_hub_variables = df_human_aid.loc[df_human_aid['Detail'].isin(['Deklarovaná cena (EURO)','Množstvo (počet paliet)','Hmotnosť (kg a t)'])]
	df_hub_melt = pd.melt(df_hub_variables, id_vars=['Typ','Detail'],var_name='Dátum', value_name='Suma')

	pallets_df = df_hub_melt.loc[df_hub_melt['Detail'] == 'Množstvo (počet paliet)']
	weight_df = df_hub_melt.loc[df_hub_melt['Detail'] == 'Hmotnosť (kg a t)']
	euros_df = df_hub_melt.loc[df_hub_melt['Detail'] == 'Deklarovaná cena (EURO)']

	total_pallets = pallets_df.Suma.sum()
	total_pallets_return = f'{total_pallets:.0f}'
	

	total_weight = weight_df.Suma.sum()
	total_weight = total_weight / 1000
	total_weight_string = f'{total_weight:.2f}'
	tons_symbol = "T"
	total_weight_return  = total_weight_string + " " + tons_symbol

	total_euros = euros_df.Suma.sum()
	total_euros_return = str(format_currency(total_euros, 'EUR', locale='sk_SK'))



	fig_human_aid = px.bar(df_transit_melt,x='Dátum',y='Suma',color='Detail',barmode='stack',template='plotly_white',labels={'Detail':'Premenná'},
             title='Humanitárna pomoc (pri tranzite do UA)',facet_col="Detail",facet_col_wrap=1,
             height=900,color_discrete_map=humanaid_color_map)

	fig_human_aid.update_yaxes(matches=None)
	fig_human_aid.update_xaxes(nticks=5)

	fig_human_aid.update_traces(hovertemplate="Datúm:  %{x}<br><br><b>Celkom: %{y}</b>")
	fig_human_aid.update_layout(
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
		) 
	fig_human_aid.update_layout(showlegend=False)  
	fig_human_aid.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
	#fig_human_aid.update_xaxes(rangeslider_visible=True)

	return last_update_return, total_pallets_return, total_weight_return, total_euros_return, fig_human_aid







