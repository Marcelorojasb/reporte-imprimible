import dash
from dash import dcc, html, Input, Output, callback

dash.register_page(__name__,path='/contacto')
layout = html.Div(
        [
            # page 6
            html.Div(
                [
                    # Row 1
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("News", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.P(
                                                "29/05/2023    First release"
                                            ),
                                        ],
                                        style={"color": "#7a7a7a", "font-size": "13px"},
                                    ),
                                ],
                                className="row",
                            ),
                            html.Div(
                                [
                                    html.H6("Información de contacto", className="subtitle padded"),
                                    html.Br([]),
                                    html.Div(
                                        [
                                            html.Li("Número: "),
                                            html.Li("Correo: "),
                                            html.Li("Visitenos en neocity.cl"),
                                        ],
                                        id="reviews-bullet-pts",
                                    ),
                                    html.Div(
                                        [
                                            html.P(
                                                "Somos especialistas de energía y tecnología con más de 20 años de experiencia"
                                            ),
                                        ],
                                        style={"color": "#7a7a7a", "font-size": "13px"},
                                    ),
                                ],
                                className="row",
                            ),
                        ],
                        className="row ",
                    )
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )
