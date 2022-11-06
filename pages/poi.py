# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal


# -----------------------------------------------------
#                 DESCRIPTION
# -----------------------------------------------------
# This script shows the interactive map


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
from dash import Dash, Input, Output, dcc, html, dash_table, callback
import dash_bootstrap_components as dbc
from dash_iconify import DashIconify

# -----------------------------------------------
#                 DATA TREATMENT
# -----------------------------------------------

# Import information to dataframe 

df_raw = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=1280528379&single=true&output=csv')

# -----------------------------------------------
#                 MAP CREATION
# -----------------------------------------------

# Create Map 

fig_map = px.scatter_mapbox(df_raw, lat="Latitude", lon="Longitude",
	color="Kategória / Category",
	center=dict(lon=19.6500, lat=48.8343),
	zoom=6,
	size_max=15,
	height=400
	)

# Stylize Map 
# Update hover_label background color, font-size, and font-family
fig_map.update_layout(
	hoverlabel=dict(
		bgcolor="#272b30",
		font_size=16,
		font_family="Open Sans, sans-serif")
	)

# Hide Color Scale. It usually appears next to the map. 
fig_map.update_layout(coloraxis_showscale=False)

# Choose Map Layout and margins 
fig_map.update_layout(mapbox_style = 'open-street-map',margin={"r":0,"t":0,"l":5,"b":0})

# Create Hooverlabel content 
hovername="INFO"

fig_map.update_traces(
	hovertext=hovername, 
	hovertemplate=f'<b>{hovername}<b>'
	)

# Define size of circles and opacity 
fig_map.update_traces(marker=dict(size=17,opacity=0.8))




# Legend Card Style 

card_icon_legend = {
		"color": "#273B80",
		"textAlign": "center",
		"fontSize": 30,
		"margin": "auto",
		}
card_icon_legend_weekend = {
		"color": "#273B80",
		"textAlign": "center",
		"fontSize": 30,
		"margin": "auto",
		}
card_icon_legend_bed_emergency = {
		"color": "red",
		"textAlign": "center",
		"fontSize": 30,
		"margin": "auto",
		}

# -----------------------------------------------
#                 APP LAYOUT
# -----------------------------------------------



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
					dcc.Graph(id='poi_graph',figure=fig_map,
						config= dict(
							displayModeBar = False),
						),
					], 
					),
				xs=12, sm=12, md=12, lg=12, xl=12,
				),
			],
			),
		# Address Card
		dbc.Row(
			[
			dbc.Col(
				html.Div(id='main_address'),
				xs=12, sm=12, md=12, lg=12, xl=12,
				),
			],
			),
		# Contact Email and Opening Hours
		dbc.Row(
			[
			dbc.Col(
				html.Div(id='main_telephone'),
				xs=12, sm=12, md=4, lg=3, xl=3,
				),
			dbc.Col(
				html.Div(id='main_email'),
				xs=12, sm=12, md=4, lg=3, xl=3,
				),
			dbc.Col(
					html.Div(id='main_hours'),
					xs=12, sm=12, md=4, lg=3, xl=3,
				),
			dbc.Col(
					html.Div(id='main_hours_weekend'),
					xs=12, sm=12, md=4, lg=3, xl=3,
				),
			],
		),
		# Services 
		dbc.Row(
			[
				dbc.Col(
					html.H1("Dostupné služby"),
				xs=12, sm=12, md=4, lg=3, xl=3,
				),
			],

		),

		dbc.Row(
			[
				dbc.Col(
				html.Div(id="services_passport"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_temp_refuge"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_medical"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_hotfood"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_coldfood"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_hotdrinks"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_bottlewater"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_wc"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_shower"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_beds_1_10"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_beds_1"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
			],
		),

		dbc.Row(
			[
				dbc.Col(
				html.Div(id="services_bed_relax"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_psychological"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_atm"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_exchange"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_mobile"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_labour"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_children"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_animation"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_changing"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_pet"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
				dbc.Col(
				html.Div(id="services_aid"),
				xs=1, sm=1, md=1, lg=1, xl=1,	
				),
			],
		),
		html.Hr(),
		html.Hr(),
		dbc.Row(dbc.Col(html.H1("Legenda"),),),
		dbc.Row(
			[
				dbc.Col(
					html.P(
						DashIconify(icon="ant-design:clock-circle-filled",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Otváracie hodiny"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="ant-design:clock-circle-outline",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Otváracie hodiny cez víkend"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="fontisto:passport",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Pasová kontrola"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),	
			],
		className="g-0",
		),

		dbc.Row(
			[
				dbc.Col(
					html.P(
						DashIconify(icon="ant-design:file-protect-outlined",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Registrácia ,,dočasné útočisko"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="fa-solid:hand-holding-medical",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Zdravotná služba"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="emojione-monotone:pot-of-food",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Strava teplá"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),	
			],
		className="g-0",
		),

		dbc.Row(
			[
				dbc.Col(
					html.P(
						DashIconify(icon="fa6-solid:bowl-food",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Strava studená"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="charm:coffee",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Teplé nápoje"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="fa6-solid:bottle-water",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Balená voda"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),	
			],
		className="g-0",
		),

		

		dbc.Row(
			[
				dbc.Col(
					html.P(
						DashIconify(icon="bi:badge-wc",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("WC/toaleta"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="fa-solid:shower",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Sprcha (umývadlo + teplá voda)"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="mdi:bed",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Lôžka - núdzové ubytovanie (1-10dní)"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),	
			],
		className="g-0",
		),

		dbc.Row(
			[
				dbc.Col(
					html.P(
						DashIconify(icon="mdi:bed",style=card_icon_legend_bed_emergency),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Lôžka - núdzové ubytovanie 1noc (24h)"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="ic:baseline-chair",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Oddychové lôžka (bez nocľahu)"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="ri:mental-health-fill",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Psychologická pomoc"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),	
			],
		className="g-0",
		),

		dbc.Row(
			[
				dbc.Col(
					html.P(
						DashIconify(icon="emojione-monotone:atm-sign",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Bankomat"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="ic:outline-currency-exchange",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Zmenáreň (euro - hrivna)"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="carbon:mobile-add",style=card_icon_legend_weekend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Služby mobilných operátorov"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),	
			],
		className="g-0",
		),

		dbc.Row(
			[
				dbc.Col(
					html.P(
						DashIconify(icon="mdi:office-building-cog",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("UPSVaR"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="map:playground",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Detský kútik"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="fa6-solid:hands-holding-child",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Služby pre deti - animátori"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),	
			],
		className="g-0",
		),

		dbc.Row(
			[
				dbc.Col(
					html.P(
						DashIconify(icon="mdi:mother-nurse",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Prebaľovací kútik"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="map:veterinary-care",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Priestor pre zvieratá (veterinárna služba)"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),
				dbc.Col(
					html.P(
						DashIconify(icon="fa-solid:hands-helping",style=card_icon_legend),
					),
				xs=1, sm=1, md=1, lg=1, xl=1,
				),
				dbc.Col(
					html.P("Humanitárna pomoc (drogéria, oblečeNIE, obuv)"),
				xs=1, sm=1, md=1, lg=1, xl=3,
				),	
			],
		className="g-0",
		),
	],
)

@callback(
	# First Row 
	Output(component_id="main_address", component_property="children"), 
	Output(component_id="main_telephone", component_property="children"),
	Output(component_id="main_email", component_property="children"), 
	Output(component_id="main_hours", component_property="children"), 
	Output(component_id="main_hours_weekend", component_property="children"), 
	# Second Row 
	Output(component_id="services_passport", component_property="children"), #
	Output(component_id="services_temp_refuge", component_property="children"),
	Output(component_id="services_medical", component_property="children"), 
	Output(component_id="services_hotfood", component_property="children"), 
	Output(component_id="services_coldfood", component_property="children"), 
	Output(component_id="services_hotdrinks", component_property="children"), 
	Output(component_id="services_bottlewater", component_property="children"), 
	Output(component_id="services_wc", component_property="children"),
	Output(component_id="services_shower", component_property="children"), 
	Output(component_id="services_beds_1_10", component_property="children"), 
	Output(component_id="services_beds_1", component_property="children"), 
	# Third  Row 
	Output(component_id="services_bed_relax", component_property="children"), 
	Output(component_id="services_psychological", component_property="children"), 
	Output(component_id="services_atm", component_property="children"), 
	Output(component_id="services_exchange", component_property="children"), 
	Output(component_id="services_mobile", component_property="children"), 
	Output(component_id="services_labour", component_property="children"), 
	Output(component_id="services_children", component_property="children"), 
	Output(component_id="services_animation", component_property="children"), 
	Output(component_id="services_changing", component_property="children"), 
	Output(component_id="services_pet", component_property="children"), 
	Output(component_id="services_aid", component_property="children"), 
	Input(component_id='poi_graph',component_property='hoverData'),
	prevent_initial_call=True
	)


def create_cards(data):
	if not None:

		actual_lat = data['points'][0]['lat']
		actual_lon = data['points'][0]['lon']
		
		df_map = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=1280528379&single=true&output=csv')
		
		current_point = df_map.loc[(df_map['Latitude'] == actual_lat) & (df_map['Longitude'] == actual_lon)]
		name = current_point['Meno / Name'].values[0]
		address = current_point['Adresa / Address'].values[0]
		county = current_point['Kraj / Country'].values[0]
		hours_week = current_point['Otváracie hodiny'].values[0]
		hours_weekend = current_point['Otváracie hodiny cez víkend'].values[0]
		contact_phone = current_point['Telefonický kontakt / Phone number'].values[0]
		contact_email = current_point['E-mail'].values[0]
		# Services
		passport_control = current_point['Pasová kontrola'].values[0]
		temporary_shelter = current_point['Registrácia ,,dočasné útočiskoˮ'].values[0]
		medical_service = current_point['Zdravotná služba'].values[0]
		hotfood_service = current_point['Strava teplá'].values[0]
		coldfood_service = current_point['Strava studená'].values[0]
		hotdrinks_service = current_point['Teplé nápoje'].values[0]
		bottlewater_service = current_point['Balená voda'].values[0]
		wc_service = current_point['WC/toaleta'].values[0]
		shower_service = current_point['Sprcha (umývadlo + teplá voda)'].values[0]
		beds_1_to_10_service = current_point['Lôžka - núdzové ubytovanie (1-10dní)'].values[0]
		beds_1_service = current_point['Lôžka - núdzové ubytovanie 1noc (24h)'].values[0]
		beds_relax_service = current_point['Oddychové lôžka (bez nocľahu)'].values[0]              
		psychological_service = current_point['Psychologická pomoc'].values[0]                           
		atm_service = current_point['Bankomat'].values[0]                                   
		exchange_service = current_point['Zmenáreň (euro - hrivna)'].values[0]                        
		mobile_service = current_point['Služby mobilných operátorov'].values[0]                   
		labour_service = current_point['UPSVaR'].values[0]                                          
		children_service = current_point['Detský kútik'].values[0]                                  
		animation_service = current_point['Služby pre deti - animátori'].values[0]                    
		changing_service = current_point['Prebaľovací kútik'].values[0]                           
		pet_service = current_point['Priestor pre zvieratá (veterinárna služba)'].values[0]      
		aid_service = current_point['Humanitárna pomoc (drogéria, oblečeNIE, obuv)'].values[0]

		# Services Card Icon Style Conditions

		if passport_control == "ÁNO":
			card_icon_passport = {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_passport = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}

		if temporary_shelter == "ÁNO":
				card_icon_shelter= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_shelter = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}

		if medical_service == "ÁNO":
				card_icon_medical = {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_medical = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}

		if hotfood_service == "ÁNO":
				card_icon_hotfood = {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_hotfood = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if coldfood_service == "ÁNO":
				card_icon_coldfood = {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_coldfood = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if hotdrinks_service == "ÁNO":
				card_icon_hotdrinks = {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_hotdrinks = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if bottlewater_service == "ÁNO":
				card_icon_bottlewater = {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_bottlewater = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if wc_service == "ÁNO":
				card_icon_wc= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_wc = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if shower_service == "ÁNO":
				card_icon_shower= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_shower = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if beds_1_to_10_service == "ÁNO":
				card_icon_beds_1_10= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_beds_1_10 = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}

		if beds_1_service == "ÁNO":
				card_icon_beds_1= {
				"color": "red",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_beds_1 = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}

		if beds_relax_service == "ÁNO":
				card_icon_beds_relax= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_beds_relax = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}

		if psychological_service == "ÁNO":
				card_icon_psychological= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_psychological = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}

		if atm_service == "ÁNO":
				card_icon_atm= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_atm = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}

		if exchange_service == "ÁNO":
				card_icon_exchange= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_exchange = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if mobile_service == "ÁNO":
				card_icon_mobile= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_mobile = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if labour_service == "ÁNO":
				card_icon_labour= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_labour = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if children_service == "ÁNO":
				card_icon_children= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_children = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if animation_service == "ÁNO":
				card_icon_animation= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_animation = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if changing_service == "ÁNO":
				card_icon_changing= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_changing = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if pet_service == "ÁNO":
				card_icon_pet= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_pet = {
			"color": "#f5f6fc",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}
		if aid_service == "ÁNO":
				card_icon_aid= {
				"color": "#273B80",
				"textAlign": "center",
				"fontSize": 60,
				"margin": "auto",
			}
		else: 
			card_icon_aid = {
			"color": "#273B80",
			"textAlign": "center",
			"fontSize": 60,
			"margin": "auto",
		}

		# Card Icon 
		# Solution provided by https://community.plotly.com/t/how-to-create-card-with-icon-on-the-right/51832/4

		card_icon = {
		"color": "#273B80",
		"textAlign": "center",
		"fontSize": 30,
		"margin": "auto",
		}

		card_icon_weekend = {
		"color": "#6772F7",
		"textAlign": "center",
		"fontSize": 30,
		"margin": "auto",
		}

		card_head_style = {"background": "#273B80","color":"white"}
		card_text_style = {"color":"#273B80","font":"bold"}

		address_card =  dbc.Row(
			[
			dbc.Col(
				[
				dbc.Row(html.Div()),
				dbc.Row(),
				dbc.CardGroup(
					[
					dbc.Card(
						html.Div(DashIconify(icon="entypo:address"),style=card_icon),
						style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
						),
					dbc.Card(
						dbc.CardBody(
							[
							html.H5(name,className="card-text border-0",style=card_text_style),
							html.P(address,className="card-text")
							]   
							),style={"border": "none", "outline": "white"},
						),

					],
					)
				],
				xs=12, 
				),
			],className="g-0",
			),

		telephone_card =  dbc.Row(
			[
			dbc.Col(
				[
				dbc.Row(html.Div()),
				dbc.Row(),
				dbc.CardGroup(
					[
					dbc.Card(
						html.Div(DashIconify(icon="bxs:phone-call"),style=card_icon),
						style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
						),
					dbc.Card(
						dbc.CardBody(
							[
							html.H5(contact_phone,className="card-text border-0",style=card_text_style),

							]   
							),style={"border": "none", "outline": "white"},
						),

					],
					)
				],
				xs=12, 
				),
			],className="g-0",
			),

		email_card =  dbc.Row(
			[
			dbc.Col(
				[
				dbc.Row(html.Div()),
				dbc.Row(),
				dbc.CardGroup(
					[
					dbc.Card(
						html.Div(DashIconify(icon="clarity:email-solid"),style=card_icon),
						style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
						),
					dbc.Card(
						dbc.CardBody(
							[
							html.H5(contact_email,className="card-text border-0",style=card_text_style),
							]   
						),
						style={"border": "none", "outline": "white"},
					),

					],
				),
				],
				xs=12, 
				),
			],className="g-0",
			),

		opening_card =  dbc.Row(
			[
			dbc.Col(
				[
				dbc.Row(html.Div()),
				dbc.Row(),
				dbc.CardGroup(
					[
					dbc.Card(
						html.Div(DashIconify(icon="ant-design:clock-circle-filled"),style=card_icon),
						style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
						),
					dbc.Card(
						dbc.CardBody(
							[
							html.H5(hours_week,className="card-text border-0",style=card_text_style),
							]   
						),
						style={"border": "none", "outline": "white"},
					),

					],
				),
				],
				xs=12, 
				),
			],className="g-0",
			),
		

		opening_weekend_card =  dbc.Row(
			[
			dbc.Col(
				[
				dbc.Row(html.Div()),
				dbc.Row(),
				dbc.CardGroup(
					[
					dbc.Card(
						html.Div(DashIconify(icon="ant-design:clock-circle-outline"),style=card_icon_weekend),
						style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
						),
					dbc.Card(
						dbc.CardBody(
							[
							html.H5(hours_weekend,className="card-text border-0",style=card_text_style),
							]   
						),
						style={"border": "none", "outline": "white"},
					),

					],
				),
				],
				xs=12, 
				),
			],className="g-0",
			),

		service_passport = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="fontisto:passport"),style=card_icon_passport),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),

		service_refuge = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="ant-design:file-protect-outlined"),style=card_icon_shelter),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_medical = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="fa-solid:hand-holding-medical"),style=card_icon_medical),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),

		service_hotfood = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="emojione-monotone:pot-of-food"),style=card_icon_hotfood),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),

		service_coldfood = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="fa6-solid:bowl-food"),style=card_icon_coldfood),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),

		service_hotdrinks = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="charm:coffee"),style=card_icon_hotdrinks),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),

		service_bottlewater = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="fa6-solid:bottle-water"),style=card_icon_bottlewater),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),

		service_wc = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="bi:badge-wc"),style=card_icon_wc),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_shower = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="fa-solid:shower"),style=card_icon_shower),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),

		service_bed_1_10 = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="mdi:bed"),style=card_icon_beds_1_10),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),

		service_bed_1 = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="mdi:bed"),style=card_icon_beds_1),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),

		service_bed_relax = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="ic:baseline-chair"),style=card_icon_beds_relax),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_psychological = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="ri:mental-health-fill"),style=card_icon_psychological),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_atm = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="emojione-monotone:atm-sign"),style=card_icon_atm),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_exchange = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="ic:outline-currency-exchange"),style=card_icon_exchange),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_mobile = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="carbon:mobile-add"),style=card_icon_mobile),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_labour = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="mdi:office-building-cog"),style=card_icon_labour),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_children = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="map:playground"),style=card_icon_children),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_animation = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="fa6-solid:hands-holding-child"),style=card_icon_animation),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_changing = dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="mdi:mother-nurse"),style=card_icon_changing),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_pet= dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="map:veterinary-care"),style=card_icon_pet),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),
		service_aid= dbc.Row(
			[
			dbc.Col(
				dbc.Card(
					html.Div(DashIconify(icon="fa-solid:hands-helping"),style=card_icon_aid),
					style={"maxWidth": 85,"color":"#273B80","border": "none", "outline": "white"},
					), 
				xs=12,
			),
			], className="g-0",
		),


		all_cards  = [
						address_card,
						telephone_card,
						email_card,
						opening_card,
						opening_weekend_card, 
						service_passport,
						service_refuge,
						service_medical,
						service_hotfood,
						service_coldfood, 
						service_hotdrinks,
						service_bottlewater, 
						service_wc,
						service_shower,
						service_bed_1_10,
						service_bed_1,
						service_bed_relax,
						service_psychological,
						service_atm,
						service_exchange,
						service_mobile,
						service_labour,
						service_children,
						service_animation,
						service_changing,
						service_pet,
						service_aid

						]



		# Return Cards 
		return all_cards
	else:
		return "No hover"




