import dash
import plotly.graph_objs as go
from datetime import date # Objetos 'date'
from dateutil.relativedelta import relativedelta
from dash import dcc, html, Input, Output, callback
from plotly.subplots import make_subplots # Múltiples plots en gráficos
from PIL import Image
from utils import make_Mplanta_table, make_dataCen_table, make_dataRet_table,  make_dataRes_table

import pandas as pd
import pathlib

# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/')

# Overview data
#df_fund_facts = pd.read_csv(DATA_PATH.joinpath("df_fund_facts.csv"))
#df_price_perf = pd.read_csv(DATA_PATH.joinpath("df_price_perf.csv"))
emp_dict = pd.read_parquet(DATA_PATH.joinpath("cen_emp_dict.parquet"), engine='pyarrow')
casos_list = [[pd.read_parquet(DATA_PATH.joinpath("centrales.parquet"), engine='pyarrow'),''], 
              [pd.read_parquet(DATA_PATH.joinpath("centralesFCTA.parquet"), engine='pyarrow'),'ANDINA']]
casos_listb = [[pd.read_parquet(DATA_PATH.joinpath("ENGIE_val202307.parquet"), engine='pyarrow'),''], 
              [pd.read_parquet(DATA_PATH.joinpath("ENGIE_val202307_FCTA.parquet"), engine='pyarrow'),'FCTA']]
ret = {'Engie': pd.read_parquet(DATA_PATH.joinpath("ENGIE_ret.parquet"), engine='pyarrow')}
auxCBcen_df = casos_list[0][0]
plpdate="2023.07"
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
                        dcc.Dropdown(id='Emp1', options=['CENTRAL TERMOELÉCTRICA ANDINA SPA','INVERSIONES HORNITOS SPA', 'ENGIE ENERGÍA CHILE S.A.', 'EÓLICA MONTE REDONDO SPA'], value=['CENTRAL TERMOELÉCTRICA ANDINA SPA','INVERSIONES HORNITOS SPA', 'ENGIE ENERGÍA CHILE S.A.', 'EÓLICA MONTE REDONDO SPA'], clearable=False, multi=True),
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione caso',
                        dcc.Dropdown(id='Caso1', options=['caso base', 'falla CTA Engie'], value=['caso base'], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Div([
                        'Seleccione central',
                        dcc.Dropdown(id = 'Cen1', value='ANDINA'), # Selección de la central (por nombre)
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Div([
                        'Seleccione simulación',
                        dcc.Dropdown(id='Sim1', options=auxCBcen_df['Hidro'].unique(), value=auxCBcen_df['Hidro'].unique()[0], clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Div([
                        'Seleccione fecha de inicio',
                        dcc.Dropdown(id='init1', options=dates, value=dates[0], clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Div([
                        'Seleccione fecha de termino',
                        dcc.Dropdown(id='end1', options=dates, value=dates[12], clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    # Row 3
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
                                    html.Table(id='datos-planta-table1'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6(
                                        "Ingresos/Costos",
                                        className="subtitle padded",
                                    ),
                                    html.Table(id='m-planta-table1'),
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "10px"},
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
                    # Row 5
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6("Ingresos planta", className="subtitle padded"),
                                    dcc.Graph(id="margen_planta1",)
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row",
                    ),
                ],
                className="letterpage",
            ),
            html.Div(
                [
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Br([], className='no-print'),
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
                    html.Div([
                        'Seleccione grupo',
                        dcc.Dropdown(id='gp1', options=['Engie'], value='Engie', clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    html.Div([
                        'Seleccione barra (gráfico retiros por barra)',
                        dcc.Dropdown(id='Bar1', options=casos_listb[0][0]['BarraPLP'].unique(), value='EntreRios220', clearable=False), # Selección de la simulación
                    ], className='no-print'),
                    # Row 4
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Datos Retiros"], className="subtitle padded"
                                    ),
                                    html.Table(id='datos-retiros-table1'),
                                ],
                                className="six columns",
                            ),
                            html.Div(
                                [
                                    html.H6("Distribución de clientes", className="subtitle padded"),
                                    dcc.Graph(id="clientes1",)
                                ],
                                className="six columns",
                            ),
                        ],
                        className="row",
                        style={"margin-bottom": "10px"},
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H5("Resumen"),
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
                            ),                     
                        ],
                        className="row",
                    ),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.H6(
                                        ["Tabla resumen"], className="subtitle padded"
                                    ),
                                    html.Table(id='resumen-table1'),
                                ],
                                className="twelve columns",
                            ),  
                        ],
                        className="row ",
                    )
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
                                    html.H6("Valorizado por barra", className="subtitle padded"),
                                    dcc.Graph(id="val-bar1",)
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
                                    html.H6("Gráfico resumen", className="subtitle padded"),
                                    dcc.Graph(id="res-fig1",)
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
    [Output(component_id='Cen1',component_property='options'),
     Output(component_id='m-planta-table1', component_property='children'),
    ],
    [Input(component_id='Emp1',component_property='value'),
     Input(component_id='Caso1',component_property='value'),
     Input(component_id='Sim1',component_property='value'),
     Input(component_id='init1',component_property='value'),
     Input(component_id='end1',component_property='value')
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
    [Output(component_id='margen_planta1', component_property='figure'),
     Output(component_id='datos-planta-table1', component_property='children')],
    [Input(component_id='Caso1',component_property='value'),
     Input(component_id='Cen1', component_property='value'), # Central seleccionada
     Input(component_id='Sim1',component_property='value'),
     Input(component_id='init1',component_property='value'),
     Input(component_id='end1',component_property='value')])
def update_planta(caso,Cen,Sim,init,end):
    # Margen planta
    start_date = init
    end_date = end
    color = ['#0172C0', '#FF4500', '#008000', '#8B008B', '#FF8C00', '#00FFFF', '#FF1493', '#32CD32', '#FFD700', '#1E90FF',
          '#FF69B4', '#7FFF00', '#FF4500', '#00BFFF', '#FF6347', '#00CED1', '#FF7F50', '#3CB371', '#FFA500', '#20B2AA',
          '#FF0000', '#40E0D0', '#FF8C69', '#6495ED', '#FF69B4', '#8B0000', '#87CEEB', '#FF4500', '#FF1493', '#FF00FF']
    fig1 = make_subplots(specs=[[{"secondary_y": True}]])
    for id, i in enumerate(caso): # Se recorren lo plp si hay más de 1
        cen_df = casos_list[id][0]
        df1 = cen_df.loc[cen_df['cen_nom'].str.strip() == Cen.strip()] # Se filtra por nombre de la central
        df1 = df1.loc[df1['Hidro'].str.strip() == Sim.strip()]
        df1 = df1.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
        # Costo marginal de la barra (se muestra el de la primera fecha en la lista):
        fig1.add_trace(
            go.Scatter(x=df1['date'], y=df1['CMgBar'], name="Cmg barra "+ i + "[USD|MWh]",marker_color=color[id+8]),
            secondary_y=True,
        )
        fig1.add_trace(
            go.Bar(x=df1['date'], y=df1['CenPgen'], name="P generada " + i + " [MW]",marker_color=color[id]),
            secondary_y=False,
        )
        # Ingreso unitario:
        fig1.add_trace(
            go.Scatter(x=df1['date'], y=df1['iu'], name="Ingreso unitario " + i + "[USD|MWh]",marker_color=color[id+14]),
            secondary_y=True,
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
    # Se setea el zoom inicial:
    fig1.update_xaxes(type="date", range=[start_date, end_date])
    # Título del eje x:
    table1 = make_dataCen_table(df1)
    return fig1, table1


@callback(
    [Output(component_id='clientes1', component_property='figure'),
     Output(component_id='datos-retiros-table1', component_property='children')],
    [Input(component_id='gp1',component_property='value'),
     Input(component_id='Caso1', component_property='value')])
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
    fig1.update_xaxes(type="date", range=[start_date, end_date])
    val_acum = []
    for id, i in enumerate(casos):
        process_df = casos_listb[id][0]
        añomes_df=process_df.groupby(['date'], as_index=False)[['Valorizado']].sum()
        añomes_df['date'] = pd.to_datetime(añomes_df['date'])
        val_acum.append((sum(añomes_df['Valorizado'].values),i))
    table = make_dataRet_table(max_client, val_acum, emp)
    return fig1, table

@callback(
    Output(component_id='val-bar1', component_property='figure'),
    [Input(component_id='gp1',component_property='value'),
     Input(component_id='Caso1', component_property='value'),
     Input(component_id='Bar1',component_property='value'),
     Input(component_id='init1',component_property='value'),
     Input(component_id='end1',component_property='value'),])
def update_bar(emp,casos,bar,init,end):
    start_date = init
    end_date = end
    color = ['#0172C0', '#FF4500', '#008000', '#8B008B', '#FF8C00', '#00FFFF', '#FF1493', '#32CD32', '#FFD700', '#1E90FF',
          '#FF69B4', '#7FFF00', '#FF4500', '#00BFFF', '#FF6347', '#00CED1', '#FF7F50', '#3CB371', '#FFA500', '#20B2AA',
          '#FF0000', '#40E0D0', '#FF8C69', '#6495ED', '#FF69B4', '#8B0000', '#87CEEB', '#FF4500', '#FF1493', '#FF00FF']
    # Gráfico año mes
    fig4 = make_subplots(specs=[[{"secondary_y": True}]])
    for id, i in enumerate(casos):
        # Gráfico año mes barra
        process_df = casos_listb[id][0]
        añomesbar_df=process_df.groupby(['BarraPLP','date'], as_index=False)[['Valorizado']].sum()
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
    fig4.update_xaxes(type="date", range=[start_date, end_date])
    return fig4

@callback(
    [Output(component_id='resumen-table1', component_property='children'),
     Output(component_id='res-fig1', component_property='figure')],
    [Input(component_id='Emp1',component_property='value'),
     Input(component_id='Sim1',component_property='value'),
     Input(component_id='init1',component_property='value'),
     Input(component_id='end1',component_property='value'),
     Input(component_id='gp1',component_property='value'),
     Input(component_id='Caso1', component_property='value')])
def update_resumen(empresa, Sim, init, end, emp, caso):
    color = ['#0172C0', '#FF4500', '#008000', '#8B008B', '#FF8C00', '#00FFFF', '#FF1493', '#32CD32', '#FFD700', '#1E90FF',
          '#FF69B4', '#7FFF00', '#FF4500', '#00BFFF', '#FF6347', '#00CED1', '#FF7F50', '#3CB371', '#FFA500', '#20B2AA',
          '#FF0000', '#40E0D0', '#FF8C69', '#6495ED', '#FF69B4', '#8B0000', '#87CEEB', '#FF4500', '#FF1493', '#FF00FF']
    options = emp_dict.loc[:,emp_dict.loc['Empresa',:].isin(empresa)].columns
    options = options.values
    options = options.tolist()   
    cen_casos = []
    casos = []
    lineas1 = []
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])   
    for id, i in enumerate(caso): # Se recorren lo plp si hay más de 1
        cenDP_df = casos_list[id][0]
        cenDP_df = cenDP_df.loc[cenDP_df['date']<=end]
        cenDP_df = cenDP_df.loc[cenDP_df['date']>=init] 
        df1DP = cenDP_df.loc[(cenDP_df['cen_nom'].str.strip()).isin(options)] # Se filtra por nombre de la central
        df1DP = df1DP.loc[df1DP['Hidro'].str.strip() == Sim.strip()]
        df1DP = df1DP.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
        # df1DP: Sumar sobre todas la fechas para obtener el anual
        añomes_df=df1DP.groupby(['date'], as_index=False)[['val']].sum()
        X = añomes_df['date'].values
        Y = añomes_df['val'].values
        fig3.add_trace(
            go.Bar(x=X, y=Y, name="Margen planta" + ' ' + i +  " [USD]",marker_color=color[id]),
            secondary_y=False,)
        lineas1.append((X,Y))
        cen_casos.append(df1DP)
        casos.append(i)
    val_acum = []
    lineas2 = []
    for id, i in enumerate(caso):
        process_df = casos_listb[id][0]
        añomes_df=process_df.groupby(['date'], as_index=False)[['Valorizado']].sum()
        añomes_df = añomes_df.loc[añomes_df['date'] <= end]
        añomes_df = añomes_df.loc[añomes_df['date'] >= init]
        añomes_df = añomes_df.sort_values(by=['date']) # Se ordenan los datos por fecha para los gráficos de linea
        val_acum.append((sum(añomes_df['Valorizado'].values),i))
        X = añomes_df['date'].values
        Y = añomes_df['Valorizado'].values
        fig3.add_trace(
            go.Bar(x=X, y=Y, name="Margen contrato" + ' ' + i +  " [USD]",marker_color=color[id+15]),
            secondary_y=False,)
        lineas2.append((X,Y))
    for id, i in enumerate(casos):
        X = lineas1[id][0]
        Y = lineas1[id][1] + lineas2[id][1]
        fig3.add_trace(
            go.Scatter(x=X, y=Y, name="Suma "+ i + " [USD]",marker_color=color[id+8]),
            secondary_y=True,
        )
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
    table = make_dataRes_table(cen_casos,casos, val_acum, emp)
    return table, fig3