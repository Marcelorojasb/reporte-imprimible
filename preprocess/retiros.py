from datetime import date
import pandas as pd
import numpy as np
import os

# ************* Directorio donde se guardarán los parquets: *************
parquet_dir='/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/5. Prog 2023.07'
#parquet_dir=r'G:\Unidades compartidas\5. Reportes\24. Prueba_PLP\2. PLP2023' # Windows


# **********************  Caso base  **********************
base = ''
base_path = '/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/5. Prog 2023.07/IPLP20230711_v7b'
#csv_path =r'G:\Unidades compartidas\5. Reportes\01. Pruebas PLP\3. Prog. 2022.09' # Windows
datafile=base_path +'/indhor.csv'
#datafile=base_path +r'\indhor.csv' # Win
indhor_df=pd.read_csv(datafile, encoding='latin-1')
datafile=base_path +'/plpbar.csv'
#datafile=base_path +r'\plpbar.csv' # Win
bar_df_base=pd.read_csv(datafile)


# **********************  Caso falla  **********************
falla = 'FCTA'
falla_path = '/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/5. Prog 2023.07/IPLP20230711_v7b_sin_CTA'
#falla_path=r'G:\Unidades compartidas\5. Reportes\01. Pruebas PLP\3. Prog. 2022.09' # Windows
datafile=falla_path+'/plpbar.csv'
#datafile=falla_path +r'\plpbar.csv' # Win
bar_df_falla=pd.read_csv(datafile)


plp_date = '2023.07'  #<------------- Ingresar fecha del plp acá
year = plpdate[0:4]
month = plpdate[5:7]


# **********************  Balances por propietario  **********************
propietario = 'ENGIE' # ENGIE (SE PUEDE CAMBIAR)
# Si el parquet del propietario no existe setear flag en 1
flag = 0
if flag:
    process_df = pd.read_parquet('/Users/marcelo/Downloads/NeoCity/Balance2022.parquet', engine='pyarrow') # Balance completo
    engie_df = process_df.loc[process_df['propietario']==propietario]
    parquet_file = os.path.join(parquet_dir, propietario + "_retiros.parquet")
    engie_df.to_parquet(parquet_file, engine='pyarrow')
# Parquet retiros engie
flag = 0
if flag:
    df_ret= pd.read_parquet(parquet_dir + '/engie_retiros.parquet', engine='pyarrow')
    clientes_df=df_ret.groupby(['Retiro','Tipo','REGION'], as_index=False)['Medida_kWh'].sum() 
    #clientes_df = clientes_df.loc[clientes_df['Tipo']!='T']
    parquet_file = os.path.join(parquet_dir, propietario + "_ret.parquet")
    clientes_df.to_parquet(parquet_file, engine='pyarrow')


# **********************  Valorizado  **********************
# Función auxiliar
def hora_mensual(bloque, anomes):
    ano = int(anomes[0:4])
    mes = int(anomes[4:6])
    bloque = int(bloque)

    # Calcular el día dentro del mes
    dia = (bloque - 1) // 24 + 1

    # Calcular la hora
    hora = (bloque - 1) % 24 + 1

    return ano, mes, dia, hora

process_df = df_ret
process_df = process_df.loc[process_df['Tipo']!='T'] 
añomesbar_df=process_df.groupby(['BarraPLP','Clave Año_Mes','Hora Mensual'], as_index=False)[['Medida_kWh']].sum()
añomesbar_df['Clave Año_Mes'] = '20' + añomesbar_df['Clave Año_Mes'].astype(str)
# Aplica la función a cada fila del DataFrame y expande los resultados en nuevas columnas
añomesbar_df[['Anno', 'Mes', 'Dia', 'Hora']] = añomesbar_df.apply(lambda row: pd.Series(hora_mensual(row['Hora Mensual'], row['Clave Año_Mes'])), axis=1)
añomesbar_df=añomesbar_df.drop(columns=['Clave Año_Mes','Hora Mensual']) # Eliminación columnas antiguas de fecha

df = añomesbar_df

# Función para calcular el valor numérico aumentado en 0.5% respecto al año anterior
def calcular_valor_año_anterior(valor_anterior):
    return valor_anterior * 1.005

# Rango de años desde 2023 hasta 2026
años_extender = range(2022, 2027)

# Extender los valores numéricos para cada etiqueta y año
df_ext = pd.DataFrame()
for etiqueta, sub_df_etiqueta in df.groupby('BarraPLP'):
    for año in años_extender:
        if año == 2022:
            # Si es el primer año de extensión, utilizamos los valores del año 2022
            sub_df_año = sub_df_etiqueta[sub_df_etiqueta['Anno'] == 2022].copy()
            sub_df_año['Anno'] = año
            df_ext = pd.concat([df_ext, sub_df_año])
        else:
            # Calculamos el valor para los años siguientes
            sub_df_año_anterior = df_ext[(df_ext['BarraPLP'] == etiqueta) & (df_ext['Anno'] == año - 1)].copy()
            sub_df_año = sub_df_etiqueta[sub_df_etiqueta['Anno'] == 2022].copy()
            sub_df_año['Anno'] = año
            sub_df_año['Medida_kWh'] = calcular_valor_año_anterior(sub_df_año_anterior['Medida_kWh'].values)
            df_ext = pd.concat([df_ext, sub_df_año])

# Restablecer los índices del DataFrame resultante
df_ext.reset_index(drop=True, inplace=True)
df_ext_filtrado = df_ext.query('(Anno >= 2024 & Anno <= 2025) | (Anno == 2023 & Mes >= 7 & Dia >= 1 & Hora >= 1) | (Anno == 2026 & Mes <= 3 & Dia <= 31 & Hora <= 24)')
df1=df_ext_filtrado.merge(indhor_df)

# CASO BASE
barras = df1['BarraPLP'].unique()
bar_df_base=bar_df_base.loc[bar_df_base['Hidro'].str.strip() == 'MEDIA']
bar_df_base=bar_df_base.loc[bar_df_base['BarNom'].str.strip().isin(barras)]
bar_df_base['BarNom'] = bar_df_base['BarNom'].str.strip()
df2 = df1.merge(bar_df_base, left_on = ['Bloque','BarraPLP'], right_on= ['Bloque','BarNom'])
df2['Valorizado'] = -df2['Medida_kWh'].values*df2['CMgBar']/1000
df2 = df2.groupby(['BarraPLP','Mes', 'Anno'], as_index=False)[['Valorizado', 'Medida_kWh']].sum() # Suma por mes de la multiplicación
df2['date'] = pd.to_datetime(dict(year=df2.Anno, month=df2.Mes, day=1)) # Fecha a datetime object
df2=df2.drop(columns=['Mes', 'Anno']) # Eliminación columnas antiguas de fecha
name = propietario + '_val' + year + month + '_'+ base + '.parquet'
parquet_file = os.path.join(parquet_dir, name)
df2.to_parquet(parquet_file, engine='pyarrow')

# CASO FALLA
barras = df1['BarraPLP'].unique()
bar_df_falla=bar_df_falla.loc[bar_df_falla['Hidro'].str.strip() == 'MEDIA']
bar_df_falla=bar_df_falla.loc[bar_df_falla['BarNom'].str.strip().isin(barras)]
bar_df_falla['BarNom'] = bar_df_falla['BarNom'].str.strip()

df2 = df1.merge(bar_df_falla, left_on = ['Bloque','BarraPLP'], right_on= ['Bloque','BarNom'])
df2['Valorizado'] = -df2['Medida_kWh'].values*df2['CMgBar']/1000
df2 = df2.groupby(['BarraPLP','Mes', 'Anno'], as_index=False)[['Valorizado', 'Medida_kWh']].sum() # Suma por mes de la multiplicación
df2['date'] = pd.to_datetime(dict(year=df2.Anno, month=df2.Mes, day=1)) # Fecha a datetime object
df2=df2.drop(columns=['Mes', 'Anno']) # Eliminación columnas antiguas de fecha
name = propietario + '_val' + year + month + '_'+ falla + '.parquet'
parquet_file = os.path.join(parquet_dir, name)
df2.to_parquet(parquet_file, engine='pyarrow')