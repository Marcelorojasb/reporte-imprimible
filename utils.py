import dash
from dash import dcc, html

def Header(app):
    return html.Div([get_header(app), html.Br([]), get_menu()], className='no-print')


def get_header(app):
    header = html.Div(
        [
            html.Div(
                [
                    html.A(
                        html.Img(
                            src=app.get_asset_url("Marca/marca_sin_bajada.png"),
                            className="logo",
                        ),
                        href="/",
                    ),
                ],
                className="row",
            ),
            html.Div(
                [
                    html.H5("       Demo reporte: Simulación de fallas"),
                ],
                className="twelve columns main-title",
                style={"padding-left": "0"},
            ),
        ],
        className="row",
    )
    return header


def get_menu():
    menu = html.Div(
        [
            dcc.Link(
                "Resumen",
                href="/",
                className="tab first",
            ),
            dcc.Link(
                "Margen Planta",
                href="/margen-planta",
                className="tab",
            ),
            dcc.Link(
                "Margen Contrato",
                href="/margen-contrato",
                className="tab",
            ),
            dcc.Link(
                "Tablas", href="/tablas", className="tab"
            ),
            dcc.Link(
                "Supuestos",
                href="/supuestos",
                className="tab",
            ),
            dcc.Link(
                "Contacto",
                href="/contacto",
                className="tab",
            ),
        ],
        className="row all-tabs",
    )
    return menu


def make_dash_table(df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    html_row = []
    for index in df.columns:
        html_row.append(html.Td(index,style={'font-size': '12px'}))
    table.append(html.Tr(html_row))
    for index, row in df.iterrows():
        html_row = []
        for i in range(len(row)):
            html_row.append(html.Td([row[i]]))
        table.append(html.Tr(html_row))
    return table


def make_Mplanta_table(cen_list,fallas,casos):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    for id, caso in enumerate(casos):
        cen_df = cen_list[id]
        ingresos_n = cen_df['val'].values
        costos_n = cen_df['costo'].values
        mp = f'{round((sum(ingresos_n) - sum(costos_n)),2):,}'
        ingresos = f'{round(sum(ingresos_n),2):,}'
        costos = f'{round(sum(costos_n),2):,}'
        row_i = [html.Td(f"Ingresos {casos[id]}" + '   [USD]',style={'font-size': '12px'}), html.Td(ingresos,style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
        row_c = [html.Td(f"Costos {casos[id]}" + '   [USD]',style={'font-size': '12px'}), html.Td(costos,style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
        row_m = [html.Td(f"Margen planta {casos[id]}" + '   [USD]',style={'font-size': '12px'}), html.Td(mp,style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
        table.append(html.Tr(row_i))
        table.append(html.Tr(row_c))
        table.append(html.Tr(row_m))
        if id == 0:
            mpcb = (round(sum(ingresos_n),2) - round(sum(costos_n),2))
        else:
            perdida = f'{(mpcb - (round(sum(ingresos_n),2) - round(sum(costos_n),2))):,}'
            row_p = [html.Td(f"Pérdida (caso base - falla) {casos[id]}" + '   [USD]',style={'font-size': '12px'}), html.Td(perdida,style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
            table.append(html.Tr(row_p))
    return table


def make_dataCen_table(cen_df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    cen_nom = cen_df['cen_nom'].unique()[0]
    cen_num = cen_df['cen_num'].unique()[0]
    tipo = cen_df['tipo'].unique()[0]
    bar_nom = cen_df['bar_nom'].unique()[0]
    plp_date = cen_df['plp_date'].unique()[0]
    row_cnom = [html.Td("Central",style={'font-size': '12px'}), html.Td(cen_nom,style={'font-size': '12px'})]
    row_cnum = [html.Td("Número",style={'font-size': '12px'}), html.Td(cen_num,style={'font-size': '12px'})]
    row_tipo = [html.Td("Tipo",style={'font-size': '12px'}), html.Td(tipo,style={'font-size': '12px'})]
    row_bnom = [html.Td("Barra",style={'font-size': '12px'}), html.Td(bar_nom,style={'font-size': '12px'})]
    row_date = [html.Td("Fecha datos",style={'font-size': '12px'}), html.Td(plp_date[5:7]+'/'+ plp_date[0:4],style={'font-size': '12px'})]
    return [html.Tr(row_cnom), html.Tr(row_cnum), html.Tr(row_tipo), html.Tr(row_bnom), html.Tr(row_date)]

def make_dataRet_table(max, val_acum, emp):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    row_e = [html.Td("Empresa",style={'font-size': '12px'}), html.Td(emp,style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
    row_c = [html.Td("Cliente mayor retiro",style={'font-size': '12px'}), html.Td(max[0],style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
    row_a = [html.Td("Mayor retiro" + ' [kWh]',style={'font-size': '12px'}), html.Td(f'{round(max[1],2):,}', style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
    table = [html.Tr(row_e), html.Tr(row_c), html.Tr(row_a)]
    for id, i in enumerate(val_acum):
        if id == 0:
            cb = round(i[0],2)
            row = [html.Td("Total retiros " + i[1] + ' [USD]',style={'font-size': '12px'}), html.Td(f'{round(i[0],2):,}', style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
            table.append(html.Tr(row))
        else:
            perdida = cb - round(i[0],2)
            row = [html.Td("Total retiros " + i[1] + ' [USD]',style={'font-size': '12px'}), html.Td(f'{round(i[0],2):,}', style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
            row_p = [html.Td("Perdida " + i[1] + ' [USD]',style={'font-size': '12px'}), html.Td(f'{round(perdida,2):,}', style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
            table.append(html.Tr(row))
            table.append(html.Tr(row_p))
    return table

def make_dataRes_table2(cen_list, casos, val_acum, emp):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    cenCB_df = cen_list[0]
    ingresosCB = cenCB_df['val'].values
    costosCB = cenCB_df['costo'].values
    cb = round(sum(ingresosCB)-sum(costosCB),2)
    table = []
    for id, caso in enumerate(casos):
        cen_df = cen_list[id]
        ingresos = cen_df['val'].values
        costos = cen_df['costo'].values
        mp = f'{round(sum(ingresos)-sum(costos),2):,}'
        diff = f'{round(sum(ingresos)-sum(costos),2)-cb:,}'
        row_i = [html.Td(f"Margen planta {casos[id]}" + '   [USD]',style={'font-size': '12px'}), html.Td(mp,style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
        row_p = [html.Td(f"Pérdida {casos[id]} respecto caso base" + '   [USD]',style={'font-size': '12px'}), html.Td(diff,style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
        table.append(html.Tr(row_i))
        table.append(html.Tr(row_p))
    for id, i in enumerate(val_acum):
        row = [html.Td("Total retiros " + i[1] + ' [USD]',style={'font-size': '12px'}), html.Td(f'{round(i[0],2):,}', style={'text-align':'right', 'padding': '10px', "font-size": "12px"})]
        table.append(html.Tr(row))
    return table

def make_dataRes_table(cen_list, casos, val_acum, emp):
    table = []
    row_1 = [html.Td("Glosa",style={'font-size': '12px'}), html.Td("Caso Base",style={"font-size": "12px"}), html.Td("Caso falla",style={"font-size": "12px"}), html.Td("Diferencia",style={"font-size": "12px"})]
    table.append(html.Tr(row_1))
    row_mp = [html.Td("Margen planta" + ' [USD]',style={'font-size': '12px'})]
    for id, caso in enumerate(casos):
        cen_df = cen_list[id]
        ingresos_n = cen_df['val'].values
        costos_n = cen_df['costo'].values
        mp = f'{round((round(sum(ingresos_n),2) - round(sum(costos_n),2)),2):,}'
        row_m = html.Td(mp,style={"font-size": "12px"})
        row_mp.append(row_m)
        if id == 0:
            mpcb = (round(sum(ingresos_n),2) - round(sum(costos_n),2))
        else:
            perdida = f'{round((- mpcb + (round(sum(ingresos_n),2) - round(sum(costos_n),2))),2):,}'
            row_p = html.Td(perdida,style={"font-size": "12px"})
            row_mp.append(row_p)
    table.append(html.Tr(row_mp))
    row_ret = [html.Td("Margen contrato" + ' [USD]',style={'font-size': '12px'})]
    for id, i in enumerate(val_acum):
        if id == 0:
            cb = round(i[0],2)
            row = html.Td(f'{round(i[0],2):,}', style={"font-size": "12px"})
            row_ret.append(row)
        else:
            perdida = cb - round(i[0],2)
            row = html.Td(f'{round(i[0],2):,}', style={"font-size": "12px"})
            row_p = html.Td(f'{round(perdida,2):,}', style={"font-size": "12px"})
            row_ret.append(row)
            row_ret.append(row_p)
    table.append(html.Tr(row_ret))
    return table

def planilla_resumen(list_df):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []
    flag = 1
    for df in list_df:
        html_row = [html.Td('',style={'font-size': '10px'})]
        if flag:
            flag = 0
            for index in df.columns:
                html_row.append(html.Td(index,style={'font-size': '11px'}))
            table.append(html.Tr(html_row))
        name = df.index.name
        table.append(html.Tr([html.Td(name,style={'font-size': '11px'})]))
        for index, row in df.iterrows():
            html_row = [html.Td(index, style={'font-size': '10px'})]
            for i in range(len(row)):
                html_row.append(html.Td([f'{round(row[i],2):,}']))
            table.append(html.Tr(html_row))
        if name == 'GENERACIÓN ESPERADA [MWh]':
            total_gen = df.sum(axis = 0, skipna = True)
            html_row = [html.Td('TOTAL GENERACIÓN', style={'font-size': '10px'})]
            for i in total_gen:
                html_row.append(html.Td([f'{round(i,2):,}']))
            table.append(html.Tr(html_row))
        if name == 'INGRESOS ESPERADOS (PxQ) [USD]':
            total_ing = df.sum(axis = 0, skipna = True)
            html_row = [html.Td('TOTAL INGRESOS', style={'font-size': '10px'})]
            for i in total_ing:
                html_row.append(html.Td([f'{round(i,2):,}']))
            table.append(html.Tr(html_row))
        if name == 'COSTOS ESPERADOS [USD]':
            total_cos = df.sum(axis = 0, skipna = True)
            html_row = [html.Td('TOTAL COSTOS', style={'font-size': '10px'})]    
            for i in total_cos:
                html_row.append(html.Td([f'{round(i,2):,}']))   
            table.append(html.Tr(html_row)) 
    table.append(html.Tr([html.Td('MARGEN PLANTA [USD]',style={'font-size': '11px'})]))
    html_row = [html.Td('INGRESOS - COSTOS', style={'font-size': '10px'})]
    for idx, i in enumerate(total_ing):
        html_row.append(html.Td([f'{round((total_ing[idx]-total_cos[idx]),2):,}']))
    table.append(html.Tr(html_row)) 
    return table