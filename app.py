#!/usr/bin/env python
# -*- coding: utf-8 -*-


# Layout Credits: Based on https://github.com/mcpcpc/sigfi/tree/dev

# Coded by Jorge Gomes from VOST Portugal 

# October 2022 

from dash import dash
from dash import page_registry

from dash import Dash

from layout.default import layout


app = Dash(__name__, use_pages=True)
values =  page_registry.values()
app.layout = layout(values)
server = app.server

if __name__ == "__main__":
    app.run_server(host='0.0.0.0', debug=False)

