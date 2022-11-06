# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal


# -----------------------------------------------------
#                 DESCRIPTION
# -----------------------------------------------------
# This script deals with the Refugees Register section


# -----------------------------------------------
#                  LIBRARIES
# -----------------------------------------------


# Import Core Libraries 
import pandas as pd
import numpy as np
import plotly.express as px
import json
import datetime as dt 
from datetime import date, datetime, time

# Import Dash and Dash Bootstrap Components
import dash
import dash_daq as daq
from dash import Input, Output, dcc, html, dash_table, callback
import dash_bootstrap_components as dbc

from dash_iconify import DashIconify



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
	dbc.Row(html.H6(id="last_update_registered",style={"color":"#273B80"}),),
	html.Hr(),
	html.H1("Distribúcia utečencov na území Slovenska",style={"color":"#273B80"}),
	html.Hr(),
	dbc.Row(
		[
			dbc.Col(
				dbc.Card(
					[
						dbc.CardImg(src="/assets/Kosicky_vlajka.svg", top=True,style={"height":100,"width":150}),
						dbc.CardBody(
							[
								html.H4("Košický", className="card-title"),
								html.H5(id="counter-kos",
									className="card-text border-0",
								),  
							]
						),
    				],
    			style={"color":"#273B80","border": "none", "outline": "white"},
				),
				xs=3,
			),

			dbc.Col(
				dbc.Card(
					[
						dbc.CardImg(src="/assets/Trenciansky_vlajka.svg", top=True,style={"height":100,"width":150}),
						dbc.CardBody(
							[
								html.H4("Trenčiansky", className="card-title"),
								html.H5(id="counter-tre",
									className="card-text border-0",
								),  
							]
						),
    				],
    			style={"color":"#273B80","border": "none", "outline": "white"},
				),
				xs=3,
			),
			dbc.Col(
				dbc.Card(
					[
						dbc.CardImg(src="/assets/Trnavsky_vlajka.svg", top=True,style={"height":100,"width":150}),
						dbc.CardBody(
							[
								html.H4("Trnavský", className="card-title"),
								html.H5(id="counter-trn",
									className="card-text border-0",
								),  
							]
						),
    				],
    			style={"color":"#273B80","border": "none", "outline": "white"},
				),
				xs=3,
			),
			dbc.Col(
				dbc.Card(
					[
						dbc.CardImg(src="/assets/Banskobystricky_vlajka.svg", top=True,style={"height":100,"width":150}),
						dbc.CardBody(
							[
								html.H4("Banskobystrický", className="card-title"),
								html.H5(id="counter-ban",
									className="card-text border-0",
								),  
							]
						),
    				],
    			style={"color":"#273B80","border": "none", "outline": "white"},
				),
				xs=3,
			),

		],

	),
	

	dbc.Row(
		[
			dbc.Col(
				dbc.Card(
					[
						dbc.CardImg(src="/assets/Bratislavsky_vlajka.svg", top=True,style={"height":100,"width":150}),
						dbc.CardBody(
							[
								html.H4("Bratislavský", className="card-title"),
								html.H5(id="counter-bra",
									className="card-text border-0",
								),  
							]
						),
    				],
    			style={"color":"#273B80","border": "none", "outline": "white"},
				),
				xs=3,
			),

			dbc.Col(
				dbc.Card(
					[
						dbc.CardImg(src="/assets/Nitriansky_vlajka.svg", top=True,style={"height":100,"width":150}),
						dbc.CardBody(
							[
								html.H4("Nitriansky", className="card-title"),
								html.H5(id="counter-nit",
									className="card-text border-0",
								),  
							]
						),
    				],
    			style={"color":"#273B80","border": "none", "outline": "white"},
				),
				xs=3,
			),
			dbc.Col(
				dbc.Card(
					[
						dbc.CardImg(src="/assets/Presovsky_vlajka.svg", top=True,style={"height":100,"width":150}),
						dbc.CardBody(
							[
								html.H4("Prešovský", className="card-title"),
								html.H5(id="counter-pre",
									className="card-text border-0",
								),  
							]
						),
    				],
    			style={"color":"#273B80","border": "none", "outline": "white"},
				),
				xs=3,
			),
			dbc.Col(
				dbc.Card(
					[
						dbc.CardImg(src="/assets/Zilinsky_vlajka.svg", top=True,style={"height":100,"width":150}),
						dbc.CardBody(
							[
								html.H4("Žilinský", className="card-title"),
								html.H5(id="counter-zil",
									className="card-text border-0",
								),  
							]
						),
    				],
    			style={"color":"#273B80","border": "none", "outline": "white"},
				),
				xs=3,
			),

		],

	),
	html.Hr(),
	html.Hr(),
	dbc.Row(
		[
		dbc.Col(
					html.Div(
						dcc.Loading(id='loader_register_graph',
							type='dot',
							color='#273B80', 	
							children=[
								dcc.Graph(id="animated_graph"),
							],

						),
					),
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
						dcc.Loading(id='loader_register_graph',
							type='dot',
							color='#273B80', 	
							children=[
								dcc.Graph(id="register_graph"),
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
	Output(component_id="last_update_registered", component_property="children"),  
	Output(component_id="counter-kos", component_property="children"),
	Output(component_id="counter-tre", component_property="children"),  
	Output(component_id="counter-trn", component_property="children"),  
	Output(component_id="counter-ban", component_property="children"),  
	Output(component_id="counter-bra", component_property="children"),  
	Output(component_id="counter-nit", component_property="children"),  
	Output(component_id="counter-pre", component_property="children"),  
	Output(component_id="counter-zil", component_property="children"),    
	Output(component_id="animated_graph", component_property="figure"),  
	Output(component_id="register_graph", component_property="figure"),  
	Input(component_id="interval-component", component_property="n_intervals"),
	)

def confirm_update(value):

	# Define a color map for the main graph 

	register_color_map = {
		"Košický":"#CF281B", 
		"Trenčiansky":"#CF281B", 
		"Trnavský":"#CF281B", 
		"Banskobystrický":"#CF281B",
       "Bratislavský":"#0366AD", 
       "Nitriansky":"#FF0102", 
       "Prešovský":"#CF281B", 
       "Žilinský":"#07963D",
	}

	# Data Treatment 

	df_dynamic = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=454383671&single=true&output=csv')

	df_dynamic['dynamic_date'] =  pd.to_datetime(df_dynamic['Dátum pobytu na SR'],format="%d.%m.%Y",dayfirst=True)

	df_region = df_dynamic.groupby(['dynamic_date','Kraj'])['Vek'].count().to_frame().reset_index()

	df_register_last_update = df_dynamic.tail(1).reset_index()

	# Create variable with the latest date
	last_update = df_register_last_update.at[0, 'Dátum pobytu na SR']
	last_update_text = "Aktualizované k dátumu: "
	last_update_return = last_update_text + str(last_update)

	df_counter = df_dynamic.loc[df_dynamic['Dátum pobytu na SR']== last_update]

	counter_bra = df_counter.loc[df_counter['Kraj'] == 'Bratislavský'].Vek.count()
	counter_kos = df_counter.loc[df_counter['Kraj'] == 'Košický'].Vek.count()
	counter_trn = df_counter.loc[df_counter['Kraj'] == 'Trnavský'].Vek.count()
	counter_zil = df_counter.loc[df_counter['Kraj'] == 'Žilinský'].Vek.count()
	counter_tre = df_counter.loc[df_counter['Kraj'] == 'Trenčiansky'].Vek.count()
	counter_nit = df_counter.loc[df_counter['Kraj'] == 'Nitriansky'].Vek.count()
	counter_pre = df_counter.loc[df_counter['Kraj'] == 'Prešovský'].Vek.count()
	counter_ban = df_counter.loc[df_counter['Kraj'] == 'Banskobystrický'].Vek.count()

	with open('assets/districts_epsg_4326.geojson') as response:
  		districts = json.load(response)

  	# Plot Graphs

	fig_animation = px.choropleth_mapbox(df_dynamic, geojson=districts,locations='Okres',featureidkey='properties.NM3',color='Vek',
		color_continuous_scale="Blues",
		center=dict(lon=20.0068, lat=48.8264),
		zoom=7,
		opacity=0.6,
		height=900,
		custom_data=['Okres','Vek'],
		labels={'Vek':'Suma'},
		animation_frame='Dátum pobytu na SR',
		hover_name='Okres', 
        hover_data = ['Dátum pobytu na SR', 'Vek'])
                          

	fig_animation.update_layout(mapbox_style = 'open-street-map',margin={"r":15,"t":0,"l":15,"b":0})
	fig_animation.update_layout(coloraxis_showscale=False)

	fig_animation.update_layout(
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
	)

	fig_animation.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
	
	


	region_graph = px.bar(df_region,x='dynamic_date',y='Vek',color='Kraj',template='plotly_white',facet_col='Kraj',
		facet_col_wrap=4,height=900,
		labels={'dynamic_date':'Dátum pobytu na SR','Vek':'Suma'}
		)
	region_graph.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))

	region_graph.update_layout(
		height=900,
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
		)  

	

	return last_update_return, counter_kos, counter_tre, counter_trn, counter_ban, counter_bra, counter_nit, counter_pre, counter_zil, fig_animation, region_graph







