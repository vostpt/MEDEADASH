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


df = pd.read_csv(
		'https://docs.google.com/spreadsheets/d/e/2PACX-1vTSnUP4UWex1vuhJ_cyMk81bSyD7ez1CKUcNd_NBKky'
		'-Wbz3tnYeTpVGddpv7f4qMc4dCrgmgTiIyXr/pub?gid=0&single=true&output=csv')
df_dropdown = pd.melt(df, id_vars=['center', 'total_capacity'], var_name='date', value_name='occupancy')


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
											dbc.Col(id='table',xs=12, sm=12, md=12, lg=12, xl=12),
									], 
									),
				xs=12, sm=12, md=12, lg=12, xl=12,
				),
				],
		),
		dbc.Row(
                [
                dbc.Col(html.H4("CENTRUM VÝBERU:"),xs=12, sm=12, md=3, lg=3, xl=3,),
                dbc.Col(
                    dcc.Dropdown(
                        id='dropdown_area',
                        options=[{'label': i, 'value': i} for i in df_dropdown.center.unique()],
                        value='ZT Humenné', className="dropdown"
                    ),xs=12, sm=12, md=3, lg=3, xl=3,
                ),
            ],
            ),
            dcc.Graph(id="bar_graph_table")
	],
)

@callback(
	
	Output(component_id="table",component_property="children"), 

	Input(component_id="interval-component", component_property="n_intervals"),
)

# WHAT HAPPENS WHEN CALL BACK IS TRIGGERED
def confirm_update(value):

	# -----------------------------------------------
	#               DATA TREATMENT
	# -----------------------------------------------

	df_raw = pd.read_csv(
		'https://docs.google.com/spreadsheets/d/e/2PACX-1vTSnUP4UWex1vuhJ_cyMk81bSyD7ez1CKUcNd_NBKky'
		'-Wbz3tnYeTpVGddpv7f4qMc4dCrgmgTiIyXr/pub?gid=0&single=true&output=csv')
	df_map_tab = pd.melt(df_raw, id_vars=['center', 'total_capacity'], var_name='date', value_name='occupancy')
	df_latest_map_tab = df_map_tab.tail(11)
	df_latest_map = df_latest_map_tab.tail(11)

	df_map = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vTSnUP4UWex1vuhJ_cyMk81bSyD7ez1CKUcNd_NBKky-Wbz3tnYeTpVGddpv7f4qMc4dCrgmgTiIyXr/pub?gid=65156759&single=true&output=csv')

	map_dataframe = pd.merge(df_latest_map, df_map, on ='center', how ='inner')

	

	df_table_up=map_dataframe.filter(['center','total_capacity','occupancy'])
	df_table_up['percentage']=round((map_dataframe['occupancy']/map_dataframe['total_capacity'])*100,2)

	# Create new column with emojis based on percentage
	df_table_up['opstatus'] = df_table_up['percentage'].apply(lambda x:
		'🔴' if x > 90 else (
			'🟠' if x > 70 else (
				'🟡' if x > 49 else (
					'🟢' if x == 0 else  (
						'🟢' if x > 0 else ''
						)))))

	newtable_up = dash_table.DataTable(

		data=df_table_up.to_dict('records'),                                        
		columns=[                                                                   
				{'name':'Center', 'id':'center'},                                    
				{'name':'Total Beds', 'id':'total_capacity','type':'numeric'},      
				{'name':'Occupied', 'id':'occupancy','type':'numeric'},        		
				{'name':'Status', 'id':'opstatus'},                                

				],
		fixed_rows={'headers': True},                                               
		style_table={'height': 350},                                               

		style_cell_conditional=[                                                    
			{'if': {'column_id': 'center'},                                           
			'width': '1%','textAlign': 'left'},
			 {'if': {'column_id': 'total_capacity'},                                
			 'width': '5%'},
			{'if': {'column_id': 'occupancy'},                                
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
		page_size=11,                                                               
		)

	return newtable_up

@callback(
    Output(component_id="bar_graph_table", component_property="figure"),
    Input(component_id="dropdown_area", component_property="value")
)

# WHAT HAPPENS WHEN CALL BACK IS TRIGGERED
def dropdown_update(value):
	df = pd.read_csv(
		'https://docs.google.com/spreadsheets/d/e/2PACX-1vTSnUP4UWex1vuhJ_cyMk81bSyD7ez1CKUcNd_NBKky'
		'-Wbz3tnYeTpVGddpv7f4qMc4dCrgmgTiIyXr/pub?gid=0&single=true&output=csv')

	df_melt = pd.melt(df, id_vars=['center', 'total_capacity'], var_name='date', value_name='occupancy')

	df_bar = df_melt[df_melt['center']==value]

	fig_bar = px.bar(df_bar,x='date',y='occupancy',template='plotly_white')

	fig_bar.update_xaxes(tickangle=0, tickfont=dict(color='black', size=7))
	fig_bar.update_yaxes(tickangle=90, tickfont=dict(color='black', size=7))
	fig_bar.update_xaxes(nticks=5)
	fig_bar.update_traces(hovertemplate="Datúm:  %{x} <br><b>Celkom: %{y}</b>")
	fig_bar.update_traces(marker_color='rgb(39,59,128)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.8)

	fig_bar.update_layout(
        hoverlabel=dict(
        bgcolor="#273B80",
        font_size=16,
        font_family="sans-serif"
    	)
    )   

	return fig_bar 
