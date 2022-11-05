#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash_mantine_components as dmc

from dash_iconify import DashIconify
from dash import register_page

layout = dmc.Container(
    id="wrapper",
    children=[
        dmc.Container(
            pl=8,
            pr=8,
            style={"marginTop": 30, "marginBottom": 20},
            children=[
                dmc.Text(
                    "BAJA PORTALEGRE 500",
                    align="center",
                    style={"fontSize": 30}
                ),
                dmc.Text(
                    "Dashboard Operacional",
                    align="center"
                )
            ]
        ),
        dmc.Grid(
            gutter="xl",
            children=[
                dmc.Col(
                    children=[
                        dmc.Anchor(
                            children=[
                                dmc.Paper(
                                    withBorder=True,
                                    p="lg",
                                    children=[
                                        dmc.Group(
                                            direction="column",
                                            align="center",
                                            children=[
                                                dmc.ThemeIcon(
                                                    DashIconify(icon="carbon:dashboard", height=20),
                                                    size=40,
                                                    radius=40,
                                                    variant="light"
                                                ),
                                                dmc.Text(
                                                    "BAJA PORTALEGRE DASHBOARD",
                                                    weight=500,
                                                    style={"marginTop": 15, "marginBottom": 5}
                                                ),
                                                dmc.Text(
                                                    color="dimmed",
                                                    size="sm",
                                                    align="center",
                                                    style={"lineHeight": 1.6, "marginBottom": 10},
                                                    children=[
                                                        "Boilerplate Boilerplate BoilerPlate ",
                                                        "Boilerplate Boilerplate BoilerPlate ",
                                                        "Boilerplate Boilerplate BoilerPlate"
                                                    ]
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ],
                            href="/home"
                        )
                    ]
                )
            ]
        )
    ]
)

register_page(
    __name__,
    path="/",
    title="Home | Home",
    description="BAJA PORTALEGRE 2022 - VOSTPT",
    layout=layout
)