# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal


# -----------------------------------------------------
#                 DESCRIPTION
# -----------------------------------------------------
# This script deals with the resources 


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

# -----------------------------------------------
#                  STYLING
# -----------------------------------------------

# Create Specific Color Map for this section
resources_color_map={"HaZZ" : "#005c8d",
		"RHCP" : "#646ffa",
		"PZ SR" : "#1177a7",
		"Finančná správa" : "#588bff",
		"Ozbrojené sily SR - Celé územie od 07.04.2022" : "#565182",
		"DHZO" : "#60b2ff",
		"Okresný úrad" : "#534798",
		"Migračný úrad" : "#94b5ea",
		"Duchovná služba" : "#6a58ae",
		"Centrum právnej pomoci" : "#588cbb",
		"Zahraničné zložky" : "#8974d4",
		"MH SR" : "#355287",
		"SKR MV SR" : "#a6a4ff",
		"MK SR" : "#4b4c8f",
		"MDaV SR" : "#4a9bff",
		"MPaRV SR" : "#7a74a8",
		"Centrum podpory" : "#0074d6",
		"MPSVaR SR" : "#7d6eab",
		"Externý - Accenture" : "#0288d3",
		"Migračný úrad MV SR" : "#a38ee2",
		"Červený kríž" : "#EF1C24",
		"Dobrovoľníci" : "#EF1C24"}

# Data for DropDown 
df_resources_drop = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=951867680&single=true&output=csv')

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
		dbc.Row(html.H1("Počet štátnych zamestnancov")),
		dbc.Col(html.H6(id="last_update_resources",style={"color":"#273B80"}), xs=12, sm=10, md=6, lg=6, xl=3),
		dbc.Row(
			[
				
				dbc.Col(
						dcc.Loading(id='loader_resources',
							type='dot',
							color='#273B80', 	
							children=[
								dcc.Graph(id='resources_total_pie'),
							], 
						),
				xs=12, sm=12, md=12, lg=6, xl=6,
				),
				dbc.Col(
						dcc.Loading(id='loader_resources_focus',
							type='dot',
							color='#273B80', 	
							children=[
								dcc.Graph(id='resources_focus_pie'),
							], 
						),
				xs=12, sm=12, md=12, lg=6, xl=6,
				),
			],
		),
		dbc.Row(html.H4("Zdroje v priebehu času"),),
		dbc.Row(
                [
	                
	                dbc.Col(
	                    dcc.Dropdown(
	                        id='dropdown_resources',
	                        options=[{'label': i, 'value': i} for i in df_resources_drop['Počet štátnych zamestnancov'].unique()],
	                        value=['HaZZ','RHCP'], className="dropdown",
	                        multi=True
	                    ),
	                xs=12, sm=12, md=6, lg=6, xl=6,
	                ),
            	],
        ),
        dbc.Row(
        	[
        		dbc.Col(
        			dcc.Graph(id="resources_drop"),
        		xs=12, sm=12, md=12, lg=12, xl=12,
        		),
        	],
        ),
		
	],className="g-0"
)


@callback(
	Output(component_id="last_update_resources", component_property="children"),  
	Output(component_id="resources_total_pie",component_property="figure"),
	Output(component_id="resources_focus_pie",component_property="figure"),
 
	Input(component_id="interval-component", component_property="n_intervals"),
	)

# WHAT HAPPENS WHEN CALL BACK IS TRIGGERED
def confirm_update(value):

	# -----------------------------------------------
	#               DATA TREATMENT
	# -----------------------------------------------

	# Import Data - Resources

	df_state = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=951867680&single=true&output=csv')
	
	# Fill N/A with zero values 
	df_state = df_state.fillna(0)

	# Wide to Long 
	df_state_melt = pd.melt(df_state,id_vars='Počet štátnych zamestnancov')
	# Create Dataframe with Employment Officers
	df_state_melt_no_ps = df_state_melt[df_state_melt['Počet štátnych zamestnancov'] != "MPSVaR SR"]
	# Create Dataframes for Pie Charts
	df_state_pie = df_state_melt.tail(22)
	df_state_no_ps_pie = df_state_melt_no_ps.tail(21)

	

	df_last_update = df_state_pie.tail(1).reset_index()

	
	# Create variable with the latest date
	last_update = str(df_last_update.at[0, 'variable'])
	
	last_update_text = "Aktualizované k dátumu: "
	last_update_return = last_update_text + last_update

	

	# Resources Total Pie Last Update

	state_total_pie = px.pie(df_state_pie,names='Počet štátnych zamestnancov',values='value',hole=0.4, custom_data=['Počet štátnych zamestnancov'],
							color='Počet štátnych zamestnancov',color_discrete_map=resources_color_map,title="<b>Všetky zdroje</b>")
	state_total_pie.update_traces(textposition='inside')
	state_total_pie.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
	state_total_pie.update_traces(hovertemplate="<b>%{customdata[0]}")
	state_total_pie.update_layout(
	        hoverlabel=dict(
	        #bgcolor="#273B80",
	        font_size=16,
	        font_family="sans-serif"
	    	)
	    )   
	state_total_pie.update_traces(textinfo='text+value+percent')
	state_total_pie.update_layout(showlegend=False)
	
	# Resources Total Pie Last Update

	state_focus_pie = px.pie(df_state_no_ps_pie,names='Počet štátnych zamestnancov',values='value',hole=0.4, custom_data=['Počet štátnych zamestnancov'],
							color='Počet štátnych zamestnancov',color_discrete_map=resources_color_map,title="<b>Všetky zdroje okrem MPSVaR SR</b>")
	state_focus_pie.update_traces(textposition='inside')
	state_focus_pie.update_layout(uniformtext_minsize=10, uniformtext_mode='hide')
	state_focus_pie.update_traces(hovertemplate="<b>%{customdata[0]}")
	state_focus_pie.update_layout(
	        hoverlabel=dict(
	        font_size=16,
	        font_family="sans-serif"
	    	)
	    )   
	state_focus_pie.update_traces(textinfo='text+value+percent')
	state_focus_pie.update_layout(showlegend=False)

	return  last_update_return, state_total_pie, state_focus_pie

@callback(
    Output(component_id="resources_drop", component_property="figure"),
    Input(component_id="dropdown_resources", component_property="value")
)

def dropdownupdate(value):
	# -----------------------------------------------
	#               DATA TREATMENT
	# -----------------------------------------------

	# Create Specific Color Map for this section
	resources_color_map={"HaZZ" : "#005c8d",
		"RHCP" : "#646ffa",
		"PZ SR" : "#1177a7",
		"Finančná správa" : "#588bff",
		"Ozbrojené sily SR - Celé územie od 07.04.2022" : "#565182",
		"DHZO" : "#60b2ff",
		"Okresný úrad" : "#534798",
		"Migračný úrad" : "#94b5ea",
		"Duchovná služba" : "#6a58ae",
		"Centrum právnej pomoci" : "#588cbb",
		"Zahraničné zložky" : "#8974d4",
		"MH SR" : "#355287",
		"SKR MV SR" : "#a6a4ff",
		"MK SR" : "#4b4c8f",
		"MDaV SR" : "#4a9bff",
		"MPaRV SR" : "#7a74a8",
		"Centrum podpory" : "#0074d6",
		"MPSVaR SR" : "#7d6eab",
		"Externý - Accenture" : "#0288d3",
		"Migračný úrad MV SR" : "#a38ee2",
		"Červený kríž" : "#EF1C24",
		"Dobrovoľníci" : "#EF1C24"
	}

	# Import Data - Resources

	df_state = pd.read_csv('https://docs.google.com/spreadsheets/d/e/2PACX-1vSPMQhe0RziV-GvpZis8_8cN2TOPE6s2pSQ_1qpBiMORgVGeOI_UccexX3tOAZf_hipnekydIsQvWN3/pub?gid=951867680&single=true&output=csv')
	
	# Fill N/A with zero values 
	df_state = df_state.fillna(0)

	# Wide to Long 
	df_state_melt = pd.melt(df_state,id_vars='Počet štátnych zamestnancov',var_name='Dátum',value_name='Verejní zamestnanci alebo dobrovoľníci')

	df_dropdown_graph = df_state_melt[df_state_melt['Počet štátnych zamestnancov'].isin(value)]

	dropdown_graph = px.bar(df_dropdown_graph,x='Dátum',y='Verejní zamestnanci alebo dobrovoľníci',color='Počet štátnych zamestnancov',template='plotly_white',
							color_discrete_map=resources_color_map, barmode='group')

	dropdown_graph.update_xaxes(tickangle=0, tickfont=dict(color='black', size=7))
	dropdown_graph.update_yaxes(tickangle=90, tickfont=dict(color='black', size=7))
	dropdown_graph.update_xaxes(nticks=5)
	dropdown_graph.update_traces(hovertemplate="Datúm:  %{x} <br><b>Celkom: %{y}</b>")
	#dropdown_graph.update_traces(marker_color='rgb(39,59,128)', marker_line_color='rgb(8,48,107)',
    #              marker_line_width=1.5, opacity=0.8)

	dropdown_graph.update_layout(
        hoverlabel=dict(
        bgcolor="#273B80",
        font_size=16,
        font_family="sans-serif"
    	)
    ) 

	dropdown_graph.update_layout(showlegend=False)

	dropdown_graph.update_xaxes(rangeslider_visible=True)


	return dropdown_graph








