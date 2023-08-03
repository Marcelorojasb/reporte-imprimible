import dash
import plotly.graph_objs as go
import plotly.express as px
from datetime import date # Objetos 'date'
from dateutil.relativedelta import relativedelta
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots # Múltiples plots en gráficos
from PIL import Image

import pandas as pd
import pathlib
# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/supuestos')

emp_dict = pd.read_parquet(DATA_PATH.joinpath("cen_emp_dict.parquet"), engine='pyarrow')
dem_df = pd.read_parquet(DATA_PATH.joinpath("consumo.parquet"), engine='pyarrow')
comb_df = pd.read_parquet(DATA_PATH.joinpath("combustible.parquet"), engine='pyarrow')
planObras_df = pd.read_parquet(DATA_PATH.joinpath("planDeObras.parquet"), engine='pyarrow')

layout = html.Div(
        [
            # page 1
            html.Div(
                [
                    html.Div([
                        'Seleccione empresa',
                        dcc.Dropdown(id='empresa', options=['CENTRAL TERMOELÉCTRICA ANDINA SPA','INVERSIONES HORNITOS SPA', 'ENGIE ENERGÍA CHILE S.A.', 'EÓLICA MONTE REDONDO SPA'], value=['CENTRAL TERMOELÉCTRICA ANDINA SPA','INVERSIONES HORNITOS SPA', 'ENGIE ENERGÍA CHILE S.A.', 'EÓLICA MONTE REDONDO SPA'], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Supuestos"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Los gráficos de esta sección corresponden a costos de combustible con mayor detalle \
                                    y la demanda por mes.",
                                        style={"color": "#ffffff", "font-size": "13px"},
                                        className="row",
                                    ),
                                ],
                                className="product",
                            )
                        ],
                        className="row",
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Combustibles plena carga", className="subtitle padded"),
                                    dcc.Graph(id="comb",)
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
                                    html.H6("Demanda", className="subtitle padded"),
                                    dcc.Graph(id="dem",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="letterpage",
            ),
            # page 1
            html.Div(
                [
                    # Row 
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Plan de obras", className="subtitle padded"),
                                    dcc.Graph(id="pdo",)
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
    [Output(component_id='comb', component_property='figure'),
     Output(component_id='dem',component_property='figure'),
     Output(component_id='pdo', component_property='figure'),
    ],
    Input(component_id='empresa',component_property='value'))
def update_dropdown(empresa):
    month = [4,8,12,1,2,7,6,3,5,11,10,9]
    options = emp_dict.loc[:,emp_dict.loc['Empresa',:].isin(empresa)].columns
    cen_df = comb_df.loc[(comb_df['Nombre'].str.strip()).isin(options)]
    cen_df["Plena Carga"] = pd.to_numeric(cen_df["Plena Carga"])
    X = cen_df.groupby(['Tipo', 'Unidad medida'], as_index=False)['Plena Carga'].mean()
    col = X['Tipo'].values
    text = X['Unidad medida'].values
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#aec7e8']
    fig1 = px.bar(
        x=col,
        y=X['Plena Carga'].values,color=[i for i in col],text=[i for i in text],
        color_discrete_sequence=colors
    )
    fig1.update_layout(xaxis={'visible': True, 'showticklabels': True})
    fig1.update_layout(yaxis={'visible': True, 'showticklabels': True})
    fig1.update_layout(xaxis_title=None)
    fig1.update_layout(yaxis_title=None)
    # No mostrar leyenda:
    fig1.update_layout(showlegend=False)
    # Edición del hover:
    fig1.update_traces(
        hovertemplate="<br>".join([
            "%{x}" + ': '+ "%{y} %{text}",
        ])
    )
    # Texto en las barras (90°):
    fig1.update_traces(textangle=90)
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
    dem1_df = dem_df.loc[dem_df['Año']==2024]
    dateA = dem1_df['Año'].unique()[0]
    dem1_df = dem1_df.groupby(['Mes'], as_index=False)['GWh','GWh.1','GWh.2'].sum()
    dem1_df['total'] = dem1_df['GWh'] + dem1_df['GWh.1'] + dem1_df['GWh.2']
    dem1_df['numM'] = month
    dem1_df = dem1_df.sort_values(by=['numM']) # Se ordenan los datos por fecha para los gráficos de linea
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
            go.Bar(x=dem1_df['Mes'], y=dem1_df['total'], name="Consumo por mes [GWh]",marker_color='rgb(1,114, 192)'),
            secondary_y=False,
        )
    fig2.update_xaxes(title_text="Fecha")
    # Título del eje y:
    fig2.update_yaxes(title_text="[GWh]")
    # Hover:
    fig2.update_traces(
    hovertemplate="<br>".join([
        "Fecha: %{x}"+ f"{dateA}",
        "%{y} "+ "GWh",
    ]),
    )
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
    start_date = date(
    year=2023,
    month=3,
    day=15
    )
    end_dt = date(
        year=2025,
        month=1,
        day=15
    )
    dates = []
    while start_date <= end_dt:
        # add current date to list by converting  it to iso format
        dates.append(start_date.isoformat())
        # increment start date by timedelta
        start_date += relativedelta(months=1)
    fv = []
    eo = []
    otro = []
    for i in range(len(dates)):
        start = dates[i]
        val_df = planObras_df.loc[planObras_df['FINAL']>=start]
        val_df = val_df.groupby(['tipo'], as_index=True)['pmax'].sum()
        fv.append(val_df['FV'])
        eo.append(val_df['EO'])
        otro.append(val_df['otro'])
    fig3 = make_subplots()
    fig3.add_trace(
                go.Bar(x=dates, y=fv, name="FV",marker_color='rgb(255, 154, 27)')
            )
    fig3.add_trace(
                go.Bar(x=dates, y=eo, name="EO",marker_color='rgb(1,114, 192)')
            )
    fig3.add_trace(
                go.Bar(x=dates, y=otro, name="otro",marker_color='rgb(170, 170, 170)')
            )
    fig3.update_xaxes(title_text="Fecha")
    # Título del eje y:
    fig3.update_yaxes(title_text="[MW]")
    # Hover:
    fig3.update_traces(
    hovertemplate="<br>".join([
        "Fecha: %{x}"+ f"{dateA}",
        "%{y} "+ "[MW]",
    ]),
    )
    fig3.update_layout(legend=dict(
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
    start_date = date(
    year=2023,
    month=12,
    day=15
    )
    end_dt = date(
        year=2025,
        month=1,
        day=15
    )
    fig3.update_xaxes(type="date", range=[start_date, end_dt])
    fig3.update_yaxes(range=[0, 2000])
    return fig1, fig2, fig3