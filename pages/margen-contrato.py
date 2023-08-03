import dash
import plotly.graph_objs as go
from datetime import date # Objetos 'date'
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots # Múltiples plots en gráficos
from PIL import Image
from utils import make_dataRet_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/margen-contrato')


# Overview data
casos_list = [[pd.read_parquet(DATA_PATH.joinpath("ENGIE_val202307.parquet"), engine='pyarrow'),''], 
              [pd.read_parquet(DATA_PATH.joinpath("ENGIE_val202307_FCTA.parquet"), engine='pyarrow'),'FCTA']]
emp_dict = pd.read_parquet(DATA_PATH.joinpath("cen_emp_dict.parquet"), engine='pyarrow')
ret = {'Engie': pd.read_parquet(DATA_PATH.joinpath("ENGIE_ret.parquet"), engine='pyarrow')}

plpdate="2023.07"
start_date = date(
    year=int(plpdate[0:4]),
    month=int(plpdate[5:7]),
    day=1
)
end_date = date(
    year=int(plpdate[0:4])+2,
    month=int(plpdate[5:7]),
    day=1
)

#2.0
layout = html.Div(
        [
            # page 1
            html.Div(
                [
                    html.Div([
                        'Seleccione empresa',
                        dcc.Dropdown(id='Emp3', options=['Engie'], value='Engie', clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione caso',
                        dcc.Dropdown(id='Caso3', options=['Caso base', 'Caso falla FCTA'], value=['Caso base'], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione barra (gráfico retiros por barra)',
                        dcc.Dropdown(id='Bar', options=casos_list[0][0]['BarraPLP'].unique(), value='EntreRios220', clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    # Row 3
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Margen contrato"),
                                    html.Br([]),
                                    html.P(
                                        "\
                                    Ingresos/Costos (o tarifas) a partir de los retiros del grupo o empresa (casos base o falla), \
                                    considerar fallas genera cambios en los costos marginales y por tanto también en los ingresos, \
                                    costos y tarifas.\
                                    En la tabla 'Datos retiro', puede observar el mayor retiro de la empresa seleccionada y el total \
                                    recaudado por retiros (valorizado total) en cada caso (caso predeterminado caso base).",
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
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Datos Retiros"], className="subtitle padded"
                                    ),
                                    html.Table(id='datos-retiros-table'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6("Distribución de clientes", className="subtitle padded"),
                                    dcc.Graph(id="clientes",)
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "20px"},
                    ),
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Valorizado por barra", className="subtitle padded"),
                                    dcc.Graph(id="val-bar",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                ],
                className="letterpage",
            ),
            html.Div(
                [
                    # Row 6
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Valorizado total por mes", className="subtitle padded"),
                                    dcc.Graph(id="mgc",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),

                    # Row 7
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Retiros por mes", className="subtitle padded"),
                                    dcc.Graph(id="ret-mes",)
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
    [Output(component_id='clientes', component_property='figure'),
     Output(component_id='mgc', component_property='figure'),
     Output(component_id='datos-retiros-table', component_property='children')],
    [Input(component_id='Emp3',component_property='value'),
     Input(component_id='Caso3', component_property='value')])
def update_contrato(emp,casos):
    clientes_df = ret[emp]
    labels = clientes_df['Retiro'].values
    labels = labels.tolist()
    values = abs(clientes_df['Medida_kWh'].values)
    values = values.tolist()
    max_id = values.index(max(values))
    max_client = (labels[max_id],values[max_id])
    color = ['#0172C0', '#FF4500', '#008000', '#8B008B', '#FF8C00', '#00FFFF', '#FF1493', '#32CD32', '#FFD700', '#1E90FF',
          '#FF69B4', '#7FFF00', '#FF4500', '#00BFFF', '#FF6347', '#00CED1', '#FF7F50', '#3CB371', '#FFA500', '#20B2AA',
          '#FF0000', '#40E0D0', '#FF8C69', '#6495ED', '#FF69B4', '#8B0000', '#87CEEB', '#FF4500', '#FF1493', '#FF00FF']
    colors = color + color + color + color + color + color + color + color + color
    mina = ['MINA', 'MIN', 'MINERA', 'FAENA', 'FINNING', 'CHUQUICAMATA', 'CAP','NORANDA']
    agricola = ['AGRICOLA', 'AGRO','AGRÍCOLA']
    tipos = [mina,agricola]
    clientes = clientes_df['Retiro'].values
    tipo = clientes_df['Tipo'].values
    labels = ['Minero', 'Agricola','Comercial u otro','Regulado']
    values = [0,0,0,0]
    for id, i in enumerate(abs(clientes_df['Medida_kWh'].values)):
        flag = 1
        if tipo[id] == 'R':
            values[3] = values[3] + i
        else:
            for idx, x in enumerate(tipos):
                for y in x:
                    if y in clientes[id]:
                        values[idx] = values[idx] + i
                        flag = 0
                        break
            if flag:
                values[2] = values[2] + i
    fig1 = go.Figure(data=[go.Pie(labels=labels, values=values)])
    fig1.update_traces(textposition='inside')
    fig1.update_traces(marker=dict(colors=colors))
    fig1.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
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
    fig1.update(layout_showlegend=False)
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    val_acum = []
    for id, i in enumerate(casos):
        process_df = casos_list[id][0]
        añomes_df=process_df.groupby(['date'], as_index=False)[['Valorizado']].sum()
        añomes_df['date'] = pd.to_datetime(añomes_df['date'])
        añomes_df = añomes_df.loc[añomes_df['date'].dt.date >= start_date]
        añomes_df = añomes_df.loc[añomes_df['date'].dt.date <= end_date]
        fig3.add_trace(
            go.Bar(x=añomes_df['date'].values, y=añomes_df['Valorizado'].values, name="Valorizado total" + emp + ' ' + i +  " [USD]",marker_color=color[id]),
            secondary_y=False,)
        val_acum.append((sum(añomes_df['Valorizado'].values),i))
    fig3.update_xaxes(title_text="Fecha")
    # Título del eje y principal:
    fig3.update_yaxes(title_text="[USD]", secondary_y=False)
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
    table = make_dataRet_table(max_client, val_acum, emp)
    return fig1, fig3, table

@callback(
    [Output(component_id='val-bar', component_property='figure'),
     Output(component_id='ret-mes', component_property='figure')],
    [Input(component_id='Emp3',component_property='value'),
     Input(component_id='Caso3', component_property='value'),
     Input(component_id='Bar',component_property='value')])
def update_bar(emp,casos,bar):
    color = ['#0172C0', '#FF4500', '#008000', '#8B008B', '#FF8C00', '#00FFFF', '#FF1493', '#32CD32', '#FFD700', '#1E90FF',
          '#FF69B4', '#7FFF00', '#FF4500', '#00BFFF', '#FF6347', '#00CED1', '#FF7F50', '#3CB371', '#FFA500', '#20B2AA',
          '#FF0000', '#40E0D0', '#FF8C69', '#6495ED', '#FF69B4', '#8B0000', '#87CEEB', '#FF4500', '#FF1493', '#FF00FF']
    process_df = casos_list[0][0]
    añomes_df=process_df.groupby(['date'], as_index=False)[['Medida_kWh']].sum() 
    añomes_df['date'] = pd.to_datetime(añomes_df['date'])
    añomes_df = añomes_df.loc[añomes_df['date'].dt.date >= start_date]
    añomes_df = añomes_df.loc[añomes_df['date'].dt.date <= end_date]
    # Gráfico año mes
    fig2 = make_subplots(specs=[[{"secondary_y": True}]])
    fig2.add_trace(
        go.Bar(x=añomes_df['date'], y=-añomes_df['Medida_kWh'].values, name="Retiros por mes " + emp +  " [kWh]",marker_color=color[0]),
        secondary_y=False,)
    fig2.update_xaxes(title_text="Fecha")
    # Título del eje y principal:
    fig2.update_yaxes(title_text="[kWh]", secondary_y=False)
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
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    for id, i in enumerate(casos):
        # Gráfico año mes barra
        process_df = casos_list[id][0]
        añomesbar_df=process_df.groupby(['BarraPLP','date'], as_index=False)[['Valorizado']].sum()
        añomesbar_df['date'] = pd.to_datetime(añomesbar_df['date'])
        añomesbar_df = añomesbar_df.loc[añomesbar_df['date'].dt.date >= start_date]
        añomesbar_df = añomesbar_df.loc[añomesbar_df['date'].dt.date <= end_date]
        barfig_df = añomesbar_df.loc[añomesbar_df['BarraPLP'].str.strip()==bar.strip()]
        fig4.add_trace(
            go.Bar(x=barfig_df['date'], y=barfig_df['Valorizado'], name="Valorizado " + i +  " [USD]",marker_color=color[id]),
            secondary_y=False,)
    fig4.update_xaxes(title_text="Fecha")
    # Título del eje y principal:
    fig4.update_yaxes(title_text="[USD]", secondary_y=False)
    fig4.update_layout(legend=dict(
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
    return fig4, fig2
        