import dash
from dash import dcc, html, Input, Output, State, callback, ctx
from utils import make_dash_table, planilla_resumen
from datetime import date # Objetos 'date'
import pandas as pd
import numpy as np
import pathlib


# get relative data folder
PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../data").resolve()
#2.0
dash.register_page(__name__,path='/tablas')




# Overview data
df_mp = pd.read_parquet(DATA_PATH.joinpath("centrales.parquet"), engine='pyarrow')
df_mpf = pd.read_parquet(DATA_PATH.joinpath("centralesFCTA.parquet"), engine='pyarrow')
emp_dict=pd.read_parquet(DATA_PATH.joinpath("cen_emp_dict.parquet"), engine='pyarrow')
val = pd.read_parquet(DATA_PATH.joinpath("ENGIE_val202307.parquet"), engine='pyarrow')
val_FCTA = pd.read_parquet(DATA_PATH.joinpath("ENGIE_val202307_FCTA.parquet"), engine='pyarrow')

plpdate="2023.07"
init = date(
    year=int(plpdate[0:4]),
    month=int(plpdate[5:7]),
    day=1
)
end = date(
    year=int(plpdate[0:4])+2,
    month=int(plpdate[5:7]),
    day=1
)


layout = html.Div(
        [
            # page 5
            html.Div(
                [
                    html.Div([
                        'Seleccione empresa',
                        dcc.Dropdown(id='empresas', options=['CENTRAL TERMOELÉCTRICA ANDINA SPA','INVERSIONES HORNITOS SPA', 'ENGIE ENERGÍA CHILE S.A.', 'EÓLICA MONTE REDONDO SPA'], value=['CENTRAL TERMOELÉCTRICA ANDINA SPA','INVERSIONES HORNITOS SPA', 'ENGIE ENERGÍA CHILE S.A.', 'EÓLICA MONTE REDONDO SPA'], clearable=False, multi=True), # Selección de la simulación
                    ], className='no-print'),
                    html.Br([]),
                    html.Div([
                        'Seleccione central',
                        dcc.Dropdown(id = 'centrales', clearable=False, multi=True), # Selección de la central (por nombre)
                    ], className='no-print'),
                    html.Br([], className='no-print'),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["Plantilla de resumen caso base"],
                                        className="subtitle padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                id='table1',
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    # Row 2
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Br([]),
                                    html.H6(
                                        ["Plantilla de resumen siniestro FCTA"],
                                        className="subtitle padded",
                                    ),
                                    html.Div(
                                        [
                                            html.Table(
                                                id = 'table2',
                                                className="tiny-header",
                                            )
                                        ],
                                        style={"overflow-x": "auto"},
                                    ),
                                ],
                                className="twelve columns",
                            )
                        ],
                        className="row ",
                    ),
                    html.Div(
                        [
                            html.Button("Descargar Excel", id="btn_csv"),
                            dcc.Download(id="download-dataframe-csv"),
                        ]
                    ),
                ],
                className="sub_page",
            ),
        ],
        className="page",
    )

@callback(
    [Output(component_id='centrales',component_property='options'),
     Output(component_id='centrales',component_property='value')],
    Input(component_id='empresas',component_property='value'))
def update_dropdown(empresa):
    options = emp_dict.loc[:,emp_dict.loc['Empresa',:].isin(empresa)].columns
    options = options.values
    options = options.tolist()
    return options, options

@callback(
    [Output(component_id='table1',component_property='children'),
     Output(component_id='table2',component_property='children'),],
    Input(component_id='centrales',component_property='value'))
def update_table(options):
    expected = df_mp.groupby(['date', 'cen_nom', 'cen_num'], as_index=False)['CenCVar', 'CenEgen', 'iu', 'val', 'costo', 'CMgBar'].mean()
    expected = expected.loc[expected['date']<=np.datetime64(end)]
    expected = expected.loc[expected['date']>=np.datetime64(init)]
    # CASO BASE:
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    for planta in options:
        expected_plant = expected.loc[expected['cen_nom'].str.strip()==planta]
        expected_plant.sort_values(by=['date'])
        expected_plant['date'] = expected_plant['date'].dt.strftime('%d/%m/%Y')
        data1.append(expected_plant['CenEgen'].values)
        data2.append(expected_plant['CMgBar'].values)
        data3.append(expected_plant['iu'].values)
        data4.append(expected_plant['CenCVar'].values)
        data5.append(expected_plant['val'].values)
        data6.append(expected_plant['costo'].values)
    table_df1 = pd.DataFrame(data1,index=options, columns=expected_plant['date'].values)
    table_df1.index.name = 'GENERACIÓN ESPERADA [MWh]'
    table_df2 = pd.DataFrame(data2,index=options, columns=expected_plant['date'].values)
    table_df2.index.name = 'COSTO MARGINAL PROMEDIO [USD/MWh]'
    table_df3 = pd.DataFrame(data3,index=options, columns=expected_plant['date'].values)
    table_df3.index.name = 'INGRESO UNITARIO [USD/MWh]'
    table_df4 = pd.DataFrame(data4,index=options, columns=expected_plant['date'].values)
    table_df4.index.name = 'COSTO COMBUSTIBLE PROMEDIO [USD/MWh]'
    table_df5 = pd.DataFrame(data5,index=options, columns=expected_plant['date'].values)
    table_df5.index.name = 'INGRESOS ESPERADOS (PxQ) [USD]'
    table_df6 = pd.DataFrame(data6,index=options, columns=expected_plant['date'].values)
    table_df6.index.name = 'COSTOS ESPERADOS [USD]'
    table1 = planilla_resumen([table_df1,table_df2,table_df3,table_df4,table_df5,table_df6])
    # CASO SINIESTRO:
    expected = df_mpf.groupby(['date', 'cen_nom', 'cen_num'], as_index=False)['CenCVar', 'CenEgen', 'iu', 'val', 'costo', 'CMgBar'].mean()
    expected = expected.loc[expected['date']<=np.datetime64(end)]
    expected = expected.loc[expected['date']>=np.datetime64(init)]
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    for planta in options:
        expected_plant = expected.loc[expected['cen_nom'].str.strip()==planta]
        expected_plant.sort_values(by=['date'])
        expected_plant['date'] = expected_plant['date'].dt.strftime('%d/%m/%Y')
        data1.append(expected_plant['CenEgen'].values)
        data2.append(expected_plant['CMgBar'].values)
        data3.append(expected_plant['iu'].values)
        data4.append(expected_plant['CenCVar'].values)
        data5.append(expected_plant['val'].values)
        data6.append(expected_plant['costo'].values)
    table_df1 = pd.DataFrame(data1,index=options, columns=expected_plant['date'].values)
    table_df1.index.name = 'GENERACIÓN ESPERADA [MWh]'
    table_df2 = pd.DataFrame(data2,index=options, columns=expected_plant['date'].values)
    table_df2.index.name = 'COSTO MARGINAL PROMEDIO [USD/MWh]'
    table_df3 = pd.DataFrame(data3,index=options, columns=expected_plant['date'].values)
    table_df3.index.name = 'INGRESO UNITARIO [USD/MWh]'
    table_df4 = pd.DataFrame(data4,index=options, columns=expected_plant['date'].values)
    table_df4.index.name = 'COSTO COMBUSTIBLE PROMEDIO [USD/MWh]'
    table_df5 = pd.DataFrame(data5,index=options, columns=expected_plant['date'].values)
    table_df5.index.name = 'INGRESOS ESPERADOS (PxQ) [USD]'
    table_df6 = pd.DataFrame(data6,index=options, columns=expected_plant['date'].values)
    table_df6.index.name = 'COSTOS ESPERADOS [USD]'
    table2 = planilla_resumen([table_df1,table_df2,table_df3,table_df4,table_df5,table_df6])
    return table1, table2

@callback(
    Output("download-dataframe-csv", "data"),
    [Input("btn_csv", "n_clicks"),
     State(component_id='centrales',component_property='value')],
    prevent_initial_call=True,
)
def func(n_clicks, options, val = val, val_FCTA = val_FCTA):
    rows = len(options) + 1
    # Se genera planilla
    expected = df_mp.groupby(['date', 'cen_nom', 'cen_num'], as_index=False)[['CenCVar', 'CenEgen', 'iu', 'val', 'costo', 'CMgBar']].mean()
    expected = expected.loc[expected['date']<=np.datetime64(end)]
    expected = expected.loc[expected['date']>=np.datetime64(init)]
    # CASO BASE:
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    for planta in options:
        expected_plant = expected.loc[expected['cen_nom'].str.strip()==planta]
        expected_plant.sort_values(by=['date'])
        expected_plant['date'] = expected_plant['date'].dt.strftime('%d/%m/%Y')
        data1.append(expected_plant['CenEgen'].values)
        data2.append(expected_plant['CMgBar'].values)
        data3.append(expected_plant['iu'].values)
        data4.append(expected_plant['CenCVar'].values)
        data5.append(expected_plant['val'].values)
        data6.append(expected_plant['costo'].values)
    table_df1 = pd.DataFrame(data1,index=options, columns=expected_plant['date'].values)
    total_df = pd.DataFrame(table_df1.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL GENERACION'], columns=expected_plant['date'].values)
    table_df1=table_df1.append(total_df)
    table_df1.index.name = 'GENERACIÓN ESPERADA [MWh]'
    table_df2 = pd.DataFrame(data2,index=options, columns=expected_plant['date'].values)
    table_df2.index.name = 'COSTO MARGINAL PROMEDIO [USD/MWh]'
    table_df3 = pd.DataFrame(data3,index=options, columns=expected_plant['date'].values)
    table_df3.index.name = 'INGRESO UNITARIO [USD/MWh]'
    table_df4 = pd.DataFrame(data4,index=options, columns=expected_plant['date'].values)
    table_df4.index.name = 'COSTO COMBUSTIBLE PROMEDIO [USD/MWh]'
    table_df5 = pd.DataFrame(data5,index=options, columns=expected_plant['date'].values)
    totali_df = pd.DataFrame(table_df5.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL INGRESOS'], columns=expected_plant['date'].values)
    table_df5=table_df5.append(totali_df)
    table_df5.index.name = 'INGRESOS ESPERADOS (PxQ) [USD]'
    table_df6 = pd.DataFrame(data6,index=options, columns=expected_plant['date'].values)
    totalc_df = pd.DataFrame(table_df6.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL COSTOS'], columns=expected_plant['date'].values)
    table_df6=table_df6.append(totalc_df)
    table_df6.index.name = 'COSTOS ESPERADOS [USD]'
    table_df7 = pd.DataFrame(totali_df.sum(axis = 0, skipna = True).values.reshape(1,25) - totalc_df.sum(axis = 0, skipna = True).values.reshape(1,25),index=['INGRESOS - COSTOS'], columns=expected_plant['date'].values)
    table_df7.index.name = 'MARGEN PLANTA [USD]'
    caso_base = [table_df1,table_df2,table_df3,table_df4,table_df5,table_df6,table_df7]
    # CASO SINIESTRO:
    expected = df_mpf.groupby(['date', 'cen_nom', 'cen_num'], as_index=False)['CenCVar', 'CenEgen', 'iu', 'val', 'costo', 'CMgBar'].mean()
    expected = expected.loc[expected['date']<=np.datetime64(end)]
    expected = expected.loc[expected['date']>=np.datetime64(init)]
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    data5 = []
    data6 = []
    for planta in options:
        expected_plant = expected.loc[expected['cen_nom'].str.strip()==planta]
        expected_plant.sort_values(by=['date'])
        expected_plant['date'] = expected_plant['date'].dt.strftime('%d/%m/%Y')
        data1.append(expected_plant['CenEgen'].values)
        data2.append(expected_plant['CMgBar'].values)
        data3.append(expected_plant['iu'].values)
        data4.append(expected_plant['CenCVar'].values)
        data5.append(expected_plant['val'].values)
        data6.append(expected_plant['costo'].values)
    table_df1 = pd.DataFrame(data1,index=options, columns=expected_plant['date'].values)
    total_df = pd.DataFrame(table_df1.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL GENERACION'], columns=expected_plant['date'].values)
    table_df1=table_df1.append(total_df)
    table_df1.index.name = 'GENERACIÓN ESPERADA [MWh]'
    table_df2 = pd.DataFrame(data2,index=options, columns=expected_plant['date'].values)
    table_df2.index.name = 'COSTO MARGINAL PROMEDIO [USD/MWh]'
    table_df3 = pd.DataFrame(data3,index=options, columns=expected_plant['date'].values)
    table_df3.index.name = 'INGRESO UNITARIO [USD/MWh]'
    table_df4 = pd.DataFrame(data4,index=options, columns=expected_plant['date'].values)
    table_df4.index.name = 'COSTO COMBUSTIBLE PROMEDIO [USD/MWh]'
    table_df5 = pd.DataFrame(data5,index=options, columns=expected_plant['date'].values)
    totali_df = pd.DataFrame(table_df5.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL INGRESOS'], columns=expected_plant['date'].values)
    table_df5=table_df5.append(totali_df)
    table_df5.index.name = 'INGRESOS ESPERADOS (PxQ) [USD]'
    table_df6 = pd.DataFrame(data6,index=options, columns=expected_plant['date'].values)
    totalc_df = pd.DataFrame(table_df6.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL COSTOS'], columns=expected_plant['date'].values)
    table_df6=table_df6.append(totalc_df)
    table_df6.index.name = 'COSTOS ESPERADOS [USD]'
    table_df7 = pd.DataFrame(totali_df.sum(axis = 0, skipna = True).values.reshape(1,25) - totalc_df.sum(axis = 0, skipna = True).values.reshape(1,25),index=['INGRESOS - COSTOS'], columns=expected_plant['date'].values)
    table_df7.index.name = 'MARGEN PLANTA [USD]'
    caso_falla = [table_df1,table_df2,table_df3,table_df4,table_df5,table_df6,table_df7]

    # RETIROS POR MES CASO BASE
    data1 = []
    data2 = []
    barras = val['BarraPLP'].unique()
    val = val.loc[val['date']<=np.datetime64(end)]
    val = val.loc[val['date']>=np.datetime64(init)]
    for barra in barras:
        val_barra = val.loc[val['BarraPLP']==barra]
        val_barra = val_barra.sort_values(by=['date'])
        val_barra['date'] = val_barra['date'].dt.strftime('%d/%m/%Y')
        data1.append(-val_barra['Medida_kWh'].values)
        data2.append(val_barra['Valorizado'].values)
    table_df1 = pd.DataFrame(data1,index=barras, columns=val_barra['date'].values)
    total_df = pd.DataFrame(table_df1.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL RETIROS'], columns=val_barra['date'].values)
    table_df1=table_df1.append(total_df)
    table_df1.index.name = 'RETIROS POR MES [kWh]'
    table_df2 = pd.DataFrame(data2,index=barras, columns=val_barra['date'].values)
    total_df = pd.DataFrame(table_df2.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL VALORIZADO'], columns=val_barra['date'].values)
    table_df2=table_df2.append(total_df)
    table_df2.index.name = 'VALORIZADO POR MES [USD]'

    # RETIROS POR MES CASO FALLA
    data1 = []
    data2 = []
    val_FCTA = val_FCTA.loc[val_FCTA['date']<=np.datetime64(end)]
    val_FCTA = val_FCTA.loc[val_FCTA['date']>=np.datetime64(init)]
    for barra in barras:
        val_barra = val_FCTA.loc[val_FCTA['BarraPLP']==barra]
        val_barra = val_barra.sort_values(by=['date'])
        val_barra['date'] = val_barra['date'].dt.strftime('%d/%m/%Y')
        data1.append(-val_barra['Medida_kWh'].values)
        data2.append(val_barra['Valorizado'].values)
    table_df3 = pd.DataFrame(data1,index=barras, columns=val_barra['date'].values)
    total_df = pd.DataFrame(table_df3.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL RETIROS'], columns=val_barra['date'].values)
    table_df3=table_df3.append(total_df)
    table_df3.index.name = 'RETIROS POR MES [kWh]'
    table_df4 = pd.DataFrame(data2,index=barras, columns=val_barra['date'].values)
    total_df = pd.DataFrame(table_df4.sum(axis = 0, skipna = True).values.reshape(1,25),index=['TOTAL RETIROS'], columns=val_barra['date'].values)
    table_df4=table_df4.append(total_df)
    table_df4.index.name = 'VALORIZADO POR MES [USD]'

    # WRITE CSV
    writer = pd.ExcelWriter('plantilla_resumen.xlsx', engine="xlsxwriter")

    initrow = 0
    for idx, df in enumerate(caso_base):
            if idx == 0:
                copytoexcel = df
                copytoexcel.to_excel(writer, sheet_name='Caso Base', startrow=idx*rows+initrow)
                initrow = initrow+2
            else:
                copytoexcel = df
                copytoexcel.to_excel(writer, sheet_name='Caso Base',header=['','','','','','','','','','','','','','','','','','','','','','','','',''], startrow=idx*rows+initrow)
                initrow = initrow+2
    table_df1.to_excel(writer, sheet_name='Caso Base', startrow=idx*rows+initrow+1)
    table_df2.to_excel(writer, sheet_name='Caso Base',header=['','','','','','','','','','','','','','','','','','','','','','','','',''], startrow=idx*rows+initrow+18)

    initrow = 0
    for idx, df in enumerate(caso_falla):
            if idx == 0:
                copytoexcel = df
                copytoexcel.to_excel(writer, sheet_name='Caso siniestro FCTA', startrow=idx*rows+initrow)
                initrow = initrow+2
            else:
                copytoexcel = df
                copytoexcel.to_excel(writer, sheet_name='Caso siniestro FCTA',header=['','','','','','','','','','','','','','','','','','','','','','','','',''], startrow=idx*rows+initrow)
                initrow = initrow+2
    table_df3.to_excel(writer, sheet_name='Caso siniestro FCTA', startrow=idx*rows+initrow+1)
    table_df4.to_excel(writer, sheet_name='Caso siniestro FCTA',header=['','','','','','','','','','','','','','','','','','','','','','','','',''], startrow=idx*rows+initrow+18)
    workbook  = writer.book
    worksheet = writer.sheets['Caso Base']
    format1 = workbook.add_format({'num_format': '#,##0.00'})
    worksheet.set_column('B:Z', 18, format1)
    worksheet = writer.sheets['Caso siniestro FCTA']
    worksheet.set_column('B:Z', 18, format1)
    writer.save()
    return dcc.send_file('plantilla_resumen.xlsx')