# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal


# -----------------------------------------------------
#                 DESCRIPTION
# -----------------------------------------------------
# This script deals with the Working in SK data


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


# DATA FOR DROPDOWN
df_working = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=1784927526&single=true&output=csv')
df_filtered = df_working.drop(['Okres', 'Kraj','Aktualizované dňa'], axis = 1)



layout = html.Div(
	[
	dbc.Row(html.Img(src='/assets/topbar.png')),
	html.Hr(),
	dbc.Row(html.H6(id="last_update_working",style={"color":"#273B80"}),),
	html.Hr(),
	html.H1("Pracujúci na Slovensku",style={"color":"#273B80"}),
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
								html.H5(id="counter-kos_wk",
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
								html.H5(id="counter-tre_wk",
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
								html.H5(id="counter-trn_wk",
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
								html.H5(id="counter-ban_wk",
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
								html.H5(id="counter-bra_wk",
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
								html.H5(id="counter-nit_wk",
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
								html.H5(id="counter-pre_wk",
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
								html.H5(id="counter-zil_wk",
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
                dbc.Col(html.H4("Veková skupina:"),xs=12, sm=12, md=3, lg=3, xl=3,),
                dbc.Col(
                    dcc.Dropdown(
                        id='dropdown_agegroup',
                        options=[{'label': col, 'value': col} for col in df_filtered.columns],
                        value='Celkový súčet', className="dropdown"
                    ),xs=12, sm=12, md=3, lg=3, xl=3,
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
									dcc.Graph(id="working_graph"),
								],

							),
						),
			),	

		],
	),
	],
)


@callback(
	Output(component_id="last_update_working", component_property="children"),  
	Output(component_id="counter-kos_wk", component_property="children"),
	Output(component_id="counter-tre_wk", component_property="children"),  
	Output(component_id="counter-trn_wk", component_property="children"),  
	Output(component_id="counter-ban_wk", component_property="children"),  
	Output(component_id="counter-bra_wk", component_property="children"),  
	Output(component_id="counter-nit_wk", component_property="children"),  
	Output(component_id="counter-pre_wk", component_property="children"),  
	Output(component_id="counter-zil_wk", component_property="children"),    
	 
	 
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

	#df_dynamic = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=454383671&single=true&output=csv')

	#df_dynamic['dynamic_date'] =  pd.to_datetime(df_dynamic['Dátum pobytu na SR'],format="%d.%m.%Y",dayfirst=True)

	df_working = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=1784927526&single=true&output=csv')

	#df_region = df_dynamic.groupby(['dynamic_date','Kraj'])['Vek'].count().to_frame().reset_index()

	df_working_last_update = df_working.tail(1).reset_index()

	df_working_melt = pd.melt(df_working,id_vars=['Kraj','Okres','Aktualizované dňa'],var_name='Age Group',value_name='Total')

	# Create variable with the latest date
	last_update = df_working_last_update.at[0, 'Aktualizované dňa']
	last_update_text = "Aktualizované k dátumu: "
	last_update_return = last_update_text + str(last_update)

	df_counter = df_working

	counter_bra = df_counter.loc[df_counter['Kraj'] == 'Bratislavský kraj']['Celkový súčet'].sum()
	counter_kos = df_counter.loc[df_counter['Kraj'] == 'Košický kraj']['Celkový súčet'].sum()
	counter_trn = df_counter.loc[df_counter['Kraj'] == 'Trnavský kraj']['Celkový súčet'].sum()
	counter_zil = df_counter.loc[df_counter['Kraj'] == 'Žilinský kraj']['Celkový súčet'].sum()
	counter_tre = df_counter.loc[df_counter['Kraj'] == 'Trenčiansky kraj']['Celkový súčet'].sum()
	counter_nit = df_counter.loc[df_counter['Kraj'] == 'Nitriansky kraj']['Celkový súčet'].sum()
	counter_pre = df_counter.loc[df_counter['Kraj'] == 'Prešovský kraj']['Celkový súčet'].sum()
	counter_ban = df_counter.loc[df_counter['Kraj'] == 'Banskobystrický kraj']['Celkový súčet'].sum()

	return last_update_return, counter_kos, counter_tre, counter_trn, counter_ban, counter_bra, counter_nit, counter_pre, counter_zil

@callback(
	Output(component_id="working_graph", component_property="figure"), 
	Input(component_id="dropdown_agegroup", component_property="value")

)
def dropdown_agegroup(value):

	with open('assets/districts_epsg_4326.geojson') as response:
		districts = json.load(response)



	df_dropdown = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=1784927526&single=true&output=csv')
	df2 = df_dropdown[['Okres', value]].copy()

	print("VALUE",value)

	#df_dropdown_melt = pd.melt(df_dropdown,id_vars=['Kraj','Okres','Aktualizované dňa'],var_name='Age Group',value_name='Total')
	#df_dropdown_value  = df_dropdown_melt[df_dropdown_melt['Age Group']==value]
  	# Plot Graphs

	fig_animation = px.choropleth_mapbox(df2, geojson=districts,locations='Okres',featureidkey='properties.NM3',color=value,
		color_continuous_scale="Reds",
		center=dict(lon=20.0068, lat=48.8264),
		zoom=7,
		opacity=0.6,
		height=900,
		custom_data=['Okres',value],
		labels={'Total':'Suma'},
		hover_name='Okres', 
        hover_data = [value])
                          

	fig_animation.update_layout(mapbox_style = 'open-street-map',margin={"r":15,"t":25,"l":15,"b":0})
	fig_animation.update_layout(coloraxis_showscale=False)
	fig_animation.update_traces(hovertemplate="<b>%{customdata[0]}</b><br><b>Celkom: %{customdata[1]}</b>")

	fig_animation.update_layout(
		hoverlabel=dict(
			bgcolor="#273B80",
			font_size=16,
			font_family="sans-serif"
			)
	)

	fig_animation.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
	
	
	return fig_animation







