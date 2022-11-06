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

color_graph_map={
"Ukrajina":"#F7CE00",
"Ostatní štátni príslušníci tretích krajín":"#8C92AC",
"EÚ+":"#013193"
}

intro_text = """The forest fire of “La Montagnette”, that occurred in July 2022, is used to simulate the use of the CONFIRM solution, by VOST Portugal, 
				and its application to share information, and for social media management. 
				The fire started with a defective brake of a wagon, from a freight train, that lead to
 				multiple fires alongside the railroad. The result was 1600 ha burnt and 1000 firefighters engaged, at the peak of the fire.
 				The firefighters fought to protect an historical monument, the Abbaye du Frigolet. that was successfully protected from the fire. 
 				Several people had to be evacuated. In this exercise / Proof of Concept you will witness not only the aggregation capabilities of CONFIRM,
 				but also how VOST Portugal automates the information that should go to the public, via social media - or any other means, during a major incident, 
 				and how CONFIRM can be useful to map the capacity of evacuation areas. 
 				"""

layout = html.Div(
	[
		dbc.Row(html.Img(src='/assets/topbar.png')),
		html.Hr(),
		dbc.Row(
			[
				# AUTOMATIC UPDATER
				dcc.Interval(
					id='interval-component',
					interval=10000 * 1000,  # in milliseconds
					n_intervals=0
				),

			],
		),
		dbc.Row(
			[
				dbc.Col(
					[
					dbc.Card(
						[
						dbc.CardHeader("MEDEA Proof Of Concept", style=card_head_style),
						dbc.CardBody(
							[
								html.H4(intro_text,style=card_text_style),
							],

							),
						],
						),
					],
				xs=12, sm=12, md=12, lg=12, xl=12
				),
			],
		),
		dbc.Row(
			[
				dbc.Col(
					html.Img(src='/assets/photo-1658166113.jpeg'),
				xs=12, sm=12, md=12, lg=12, xl=12	
				),

			]

		)
	],
)
		
	








