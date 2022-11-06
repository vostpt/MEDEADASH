# -*- coding: utf-8 -*-
# Original Code by Jorge Gomes for VOST Portugal

# -----------------------------------------------
#                  LIBRARIES
# -----------------------------------------------


# Import Dash and Dash Bootstrap Components
import dash
from dash import Input, Output, dcc, html, dash_table
import dash_bootstrap_components as dbc


about_layout = html.Div(
	dbc.Row(
		[
				dbc.Row(
					html.Img(src='/assets/topbar.png'),
				),
				dbc.Row(html.Hr(),),
				dbc.Row(html.Hr(),),
				dbc.Row(html.Hr(),),
				dbc.Row(
					[
						dbc.Col(
							html.H1("O TEJTO PLATFORME"),
						xl=4,
						),
						dbc.Col(
							children=[
								  
								html.P("Táto platforma je vyvinutá, hosťovaná a udržiavaná organizáciou VOST Portugal - Associação de Voluntários Digitais em Situações de Emergência (VOSTPT)"
										"v spolupráci s Ministerstvom investícií, regionálneho rozvoja a informatizácie Slovenskej republiky (ďalej ako MIRRI SR)." 
											"Odborný personál podpory virtuálnych operácií je právnym zástupcom VOST Europe, európskej federácie VOST v Európe."
											"Platforma je postavená výlučne na technológiách otvorených zdrojov a knižníc."
											),
							],
						xl=4,
						),
						dbc.Col(
							children=[
								    
								html.P("Túto platformu VOST Portugal sprístupňuje bezodplatne pre potreby vlády Slovenskej republiky" 
											"s cieľom podporiť riadenie migračného toku osôb z Ukrajiny vyvolaného agresiou Ruskej federácie voči Ukrajine."
											"Kódy použité v tejto platforme nie je možné použiť pre komerčné účely alebo ich využiť vo vývoji iného komerčného produktu."
											"Pri verejnej komunikácii platformy je potrebné uviesť označenie jej autora VOSTPT, a to v nasledujúcej forme „CONFIRM,"
											"nástroj na riadenie masového pohybu osôb, vyvinutý spoločnosťou VOST Portugal"

									),
								
								html.H4("Za presnosť, aktualizáciu a úplnosť údajov zobrazovaných na tejto platforme,"
											"ako aj akékoľvek požiadavky na dopracovanie nových prehľadov či funkcionalít zodpovedá výlučne MIRRI SR."
											"Ako zdrojové dáta sú využívané dáta udržiavané a distribuované MV SR (BA STAB, Odbor analýzy rizík a koordinácie ÚHCP P PZ)."
									),
							],
						xl=4,
						),
					],
				),
		],
	),
	
),
