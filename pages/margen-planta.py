import dash
import plotly.graph_objs as go
from datetime import date # Objetos 'date'
from dateutil.relativedelta import relativedelta
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots # Múltiples plots en gráficos
from PIL import Image
from utils import make_dash_table, make_Mplanta_table, make_dataCen_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/margen-planta')

# Overview data
emp_dict = pd.read_parquet(DATA_PATH.joinpath("cen_emp_dict.parquet"), engine='pyarrow')
casos_list = [[pd.read_parquet(DATA_PATH.joinpath("centrales.parquet"), engine='pyarrow'),''], 
              [pd.read_parquet(DATA_PATH.joinpath("centralesFCTA.parquet"), engine='pyarrow'),'ANDINA']]
auxCBcen_df = casos_list[0][0]

plpdate="2023.03"
start_date = date(
    year=int(plpdate[0:4]),
    month=int(plpdate[5:7]),
    day=1
)
end_date = date(
    year=int(plpdate[0:4])+1,
    month=int(plpdate[5:7]),
    day=1
)
end_dt = date(
    year=int(plpdate[0:4])+3,
    month=int(plpdate[5:7]),
    day=1
)

# store the dates between two dates in a list
dates = []
while start_date <= end_dt:
    # add current date to list by converting  it to iso format
    dates.append(start_date.isoformat())
    # increment start date by timedelta
    start_date += relativedelta(months=1)

#2.0
layout = html.Div(
        [
            # page 1
            html.Div(
                [
                    html.Div([
                        'Seleccione empresa',
                        dcc.Dropdown(id='Emp2', options=['CENTRAL TERMOELÉCTRICA ANDINA SPA','INVERSIONES HORNITOS SPA', 'ENGIE ENERGÍA CHILE S.A.', 'EÓLICA MONTE REDONDO SPA'], value=['CENTRAL TERMOELÉCTRICA ANDINA SPA','INVERSIONES HORNITOS SPA', 'ENGIE ENERGÍA CHILE S.A.', 'EÓLICA MONTE REDONDO SPA'], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione caso',
                        dcc.Dropdown(id='Caso2', options=['caso base', 'falla CTA Engie'], value=['caso base'], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione central',
                        dcc.Dropdown(id = 'Cen2', value='ANDINA'), # Selección de la central (por nombre)
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione simulación',
                        dcc.Dropdown(id='Sim2', options=auxCBcen_df['Hidro'].unique(), value=auxCBcen_df['Hidro'].unique()[0], clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione fecha de inicio',
                        dcc.Dropdown(id='init2', options=dates, value=dates[0], clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione fecha de termino',
                        dcc.Dropdown(id='end2', options=dates, value=dates[12], clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    # Row 3
                    html.Br([]),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5(" Resumen Margen Planta y Contrato"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Ingresos vs costos por central. La generación no varía al producirse fallas. \
                                        El costo marginal de la barra varía al producirse fallas.",
                                        style={"color": "#ffffff", "font-size": "13px"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    #html.Div([
                        #'Seleccione central',
                        #dcc.Dropdown(id = 'Cen' ,options=cen_df['cen_nom'].unique(), value=cen_df['cen_nom'].unique()[0], clearable=False), # Selección de la central (por nombre)
                    #]),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Datos Planta"], className="subtitle padded"
                                    ),
                                    html.Table(id='datos-planta-table2'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Ingresos/Costos",
                                        className="subtitle padded",
                                    ),
                                    html.Table(id='m-planta-table2'),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "20px"},
                    ),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Tabla ingresos/costos"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    La tabla de ingresos/costos, muestra  \
                                    El costo marginal de la barra varía al producirse fallas.",
                                        style={"color": "#ffffff", "font-size": "13px"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                ],
                className="letterpage",
            ),
            html.Div(
                [
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Ingresos planta", className="subtitle padded"),
                                    dcc.Graph(id="margen_planta2",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 6
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Costo variable", className="subtitle padded"),
                                    dcc.Graph(id="c_var2",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="letterpage",
            ),
        ],
        className="page",
    )


@callback(
    [Output(component_id='Cen2',component_property='options'),
     Output(component_id='m-planta-table2', component_property='children'),
    ],
    [Input(component_id='Emp2',component_property='value'),
     Input(component_id='Caso2',component_property='value'),
     Input(component_id='Sim2',component_property='value'),
     Input(component_id='init2',component_property='value'),
     Input(component_id='end2',component_property='value')
    ])
def update_dropdown(empresa, caso, Sim, init, end):
    options = emp_dict.loc[:,emp_dict.loc['Empresa',:].isin(empresa)].columns
    options = options.values
    options = options.tolist()
    cen_casos = []
    fallas = []
    casos = []
    for id, i in enumerate(caso): # Se recorren lo plp si hay más de 1
        cen_falla = casos_list[id][1]
        perdidas_df = auxCBcen_df.loc[auxCBcen_df['cen_nom'].str.strip() == cen_falla]
        perdidas_df = perdidas_df.loc[perdidas_df['date']<=end]
        perdidas_df = perdidas_df.loc[perdidas_df['date']>=init]
        perdidas_df = perdidas_df.loc[perdidas_df['Hidro'].str.strip() == Sim.strip()]
        cenDP_df = casos_list[id][0]
        cenDP_df = cenDP_df.loc[cenDP_df['date']<=end]
        cenDP_df = cenDP_df.loc[cenDP_df['date']>=init] 
        df1DP = cenDP_df.loc[(cenDP_df['cen_nom'].str.strip()).isin(options)] # Se filtra por nombre de la central
        df1DP = df1DP.loc[df1DP['Hidro'].str.strip() == Sim.strip()]
        df1DP = df1DP.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
        cen_casos.append(df1DP)
        fallas.append(perdidas_df)
        casos.append(i)
    table = make_Mplanta_table(cen_casos,fallas,casos)
    return options, table

@callback(
    [Output(component_id='margen_planta2', component_property='figure'),
     Output(component_id='c_var2', component_property='figure'),
     Output(component_id='datos-planta-table2', component_property='children')],
    [Input(component_id='Caso2',component_property='value'),
     Input(component_id='Cen2', component_property='value'), # Central seleccionada
     Input(component_id='Sim2',component_property='value'),
     Input(component_id='init2',component_property='value'),
     Input(component_id='end2',component_property='value')])
def update_planta(caso,Cen,Sim,init,end):
    # Margen planta
    color = ['#0172C0', '#FF4500', '#008000', '#8B008B', '#FF8C00', '#00FFFF', '#FF1493', '#32CD32', '#FFD700', '#1E90FF',
          '#FF69B4', '#7FFF00', '#FF4500', '#00BFFF', '#FF6347', '#00CED1', '#FF7F50', '#3CB371', '#FFA500', '#20B2AA',
          '#FF0000', '#40E0D0', '#FF8C69', '#6495ED', '#FF69B4', '#8B0000', '#87CEEB', '#FF4500', '#FF1493', '#FF00FF']
    start_date = init
    end_date = end
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    # Se crea el segundo gráfico (Costo variable):
    fig2 = make_subplots()
    for id, i in enumerate(caso): # Se recorren lo plp si hay más de 1
        cen_df = casos_list[id][0]
        df1 = cen_df.loc[cen_df['cen_nom'].str.strip() == Cen.strip()] # Se filtra por nombre de la central
        df1 = df1.loc[df1['Hidro'].str.strip() == Sim.strip()]
        df1 = df1.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
        # Ingreso unitario:
        fig1.add_trace(
            go.Scatter(x=df1['date'], y=df1['CMgBar'], name="Cmg barra "+ i + "[USD|MWh]",marker_color=color[id+8]),
            secondary_y=True,
        )
        fig1.add_trace(
            go.Bar(x=df1['date'], y=df1['CenPgen'], name="P generada " + i + " [MW]",marker_color=color[id]),
            secondary_y=False,
        )
        # Costo marginal de la barra (se muestra el de la primera fecha en la lista):
        fig1.add_trace(
            go.Scatter(x=df1['date'], y=df1['iu'], name="Ingreso unitario " + i + "[USD|MWh]",marker_color=color[id+14]),
            secondary_y=True,
        )
        fig2.add_trace(
            go.Bar(x=df1['date'], y=df1['CenCVar'], name="Costo variable " + i +  " [USD|MW]",marker_color=color[id])
        )
    # Se crea el primer gráfico (Generación/CMG/ingreso unitario): 
    # Gráfico de barra de potencia generada
    # Titulo del gráfico:
    #fig.update_layout(
    #title_text="Proyección potencia generada")
    # Título del eje x:
    fig1.update_xaxes(title_text="Fecha")
    # Título del eje y principal:
    fig1.update_yaxes(title_text="[MW]", secondary_y=False)
    # Título del eje y secundario:
    fig1.update_yaxes(title_text="[USD|MWh]", secondary_y=True)
    # Hover eje principal:
    fig1.update_traces(
    hovertemplate="<br>".join([
        "Fecha: %{x}",
        "%{y} "+ "MW",
    ]), secondary_y=False
    )
    # Hover del eje secundario:
    fig1.update_traces(
    hovertemplate="<br>".join([
        "Fecha: %{x}",
        "%{y} "+ "USD|MWh",
    ]), secondary_y=True
    )
    fig1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1),
        margin={
                    "r": 30,
                    "t": 30,
                    "b": 30,
                    "l": 30,
                },
        height=350,
        )
    # Se agrega el logo:
    #fig.add_layout_image(
    #dict(
        #source=pyLogo,
        #xref="paper", yref="paper",
        #x=1.23, y=1.05,
        #sizex=0.2, sizey=0.2,
        #xanchor="right", yanchor="bottom"
    #)
    #)
    # Se setea el zoom inicial:
    fig1.update_xaxes(type="date", range=[start_date, end_date])
    # Título del eje x:
    fig2.update_xaxes(title_text="Fecha")
    # Título del eje y:
    fig2.update_yaxes(title_text="[USD|MW]")
    # Hover:
    fig2.update_traces(
    hovertemplate="<br>".join([
        "Fecha: %{x}",
        "%{y} "+ "USD|MW",
    ]),
    )
    # Se agrega el logo:
    #fig2.add_layout_image(
    #dict(
        #source=pyLogo,
        #xref="paper", yref="paper",
        #x=pos, y=1.05,
        #sizex=0.2, sizey=0.2,
        #xanchor="right", yanchor="bottom"
    #)
    #)
    # Se setea el zoom inicial:
    fig2.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1),
    margin={
                "r": 30,
                "t": 30,
                "b": 30,
                "l": 30,
            },
    height=350,
    )
    fig2.update_xaxes(type="date", range=[start_date, end_date])
    table1 = make_dataCen_table(df1)
    return fig1, fig2, table1