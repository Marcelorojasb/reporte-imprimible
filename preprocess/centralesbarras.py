from datetime import date
import pandas as pd
import numpy as np
import os

# ************* Directorio donde se guardarán los parquets: *************
parquet_dir='/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/5. Prog 2023.07'
#parquet_dir=r'G:\Unidades compartidas\5. Reportes\24. Prueba_PLP\2. PLP2023' # Windows


casos = []
plp_date = '2023.07'  #<------------- Ingresar fecha del plp acá

# *****************  Caso base:  *****************
base_path = '/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/5. Prog 2023.07/IPLP20230711_v7b'
#csv_path =r'G:\Unidades compartidas\5. Reportes\01. Pruebas PLP\3. Prog. 2022.09' # Windows

datafile= base_path + '/plpcen.csv'
#datafile= base_path + r'\plpcen.csv' # Win
cen_df_base=pd.read_csv(datafile)

datafile=base_path +'/indhor.csv'
#datafile=base_path +r'\indhor.csv' # Win
indhor_df=pd.read_csv(datafile, encoding='latin-1')

datafile=base_path +'/plpbar.csv'
#datafile=base_path +r'\plpbar.csv' # Win
bar_df_base=pd.read_csv(datafile)

casos.append((cen_df_base, bar_df_base, ''))

aux_sim = cen_df_base['Hidro'].unique() # Se guardan todas las simulaciones


# *****************  Caso falla 1:  *****************
falla_path = '/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/5. Prog 2023.07/IPLP20230711_v7b_sin_CTA'
#falla_path=r'G:\Unidades compartidas\5. Reportes\01. Pruebas PLP\3. Prog. 2022.09' # Windows

datafile=falla_path+'/plpcen.csv'
#datafile= falla_path + r'\plpcen.csv' # Win
cen_df_falla=pd.read_csv(datafile)

datafile=falla_path+'/indhor.csv'
#datafile=falla_path + r'\indhor.csv' # Win
#indhor_df=pd.read_csv(datafile, encoding='latin-1')

datafile=falla_path+'/plpbar.csv'
#datafile=falla_path +r'\plpbar.csv' # Win
bar_df_falla=pd.read_csv(datafile)

casos.append((cen_df_falla, bar_df_falla, 'FCTA'))

#aux_sim = cen_df['Hidro'].unique() # Se guardan todas las simulaciones


# ****************  Se pueden incluir mas casos:  ****************




# **************** Se pueden incluir mas casos:  *****************
aux_num = cen_df_base['CenNum'].unique() # Se guardan todos los numero de centrales
cens = len(aux_num)
#centrales = pd.DataFrame(columns=['Hidro', 'CenPgen', 'CenEgen', 'CenCVar', 'iu', 'val', 'costo','CMgBar','date', 'cen_nom', 'cen_num', 'tipo', 'bar_num', 'bar_nom','plp_date'])
for cen_df, bar_df, caso in casos:
    centrales_data = []
    for id, i in enumerate(aux_num): # Se recorren las centrales por número
        # CENTRAL
        cen_df1 = cen_df.loc[cen_df['CenNum'] == i] # Se buscan datos de la central "i"
        df1=cen_df1.merge(indhor_df) # Merge para obtener datos por horario
        # Info. constante central:
        cen_nom = df1['CenNom'].unique()[0] # Se guarda el nombre de la central
        tipo = df1['CenTip'].unique()[0] # Se guarda el tipo de la central
        bar_num = df1['CenBar'].unique()[0] # Se guarda el número de la barra de la central
        bar_nom = df1['BarNom'].unique()[0] # Se guarda el nombre de la barra de la central
        # BARRA
        bar_df1 = bar_df.loc[bar_df['BarNom'] == bar_nom] # Se buscan datos de la barra de la central "i"
        bar_df1 = bar_df1.loc[bar_df1['Hidro'].isin(aux_sim)] # Se usan solo las simulaciones que están en el df de centrales
        bar_df2=bar_df1.merge(indhor_df) # Merge para obtener datos por horario
        # INGRESO UNITARIO
        df1['iu']=(bar_df2['CMgBar'].values*df1['CenPgen'].values) # Multiplicación componente a componente
        df1['CMgBar']=bar_df2['CMgBar'].values
        df1['costo']=(df1['CenCVar'].values*df1['CenPgen'].values) # Multiplicación componente a componente
        df1['val']=(bar_df2['CMgBar'].values*df1['CenPgen'].values)
        aux_df1=df1.groupby(['Mes', 'Anno','Hidro'], as_index=False)[['CenPgen', 'CenCVar', 'iu','CMgBar']].mean() # Promedio por mes
        aux_df2=df1.groupby(['Mes', 'Anno','Hidro'], as_index=False)[['CenPgen', 'iu', 'val','costo']].sum() # Suma por mes de la multiplicación
        aux_df1['iu']=aux_df2['iu']/aux_df2['CenPgen'] # Normalización ingreso unitario
        aux_df1['CenEgen']=aux_df2['CenPgen']
        aux_df1['val']=aux_df2['val']
        aux_df1['costo']=aux_df2['costo']
        aux_df1=aux_df1.fillna(0) # Las divisiones por cero se rellenan con cero
        # RESTABLECER CAMPOS
        aux_df1['date'] = pd.to_datetime(dict(year=aux_df1.Anno, month=aux_df1.Mes, day=1)) # Fecha a datetime object
        aux_df1=aux_df1.drop(columns=['Mes', 'Anno']) # Eliminación columnas antiguas de fecha
        aux_df1['cen_nom']=cen_nom # Nombre central
        aux_df1['cen_num']=i # Numero central
        aux_df1['tipo']=tipo # Tipo central
        aux_df1['bar_num']=bar_num # Numero barra
        aux_df1['bar_nom']=bar_nom # Nombre barra
        aux_df1['plp_date']=plp_date # Fecha del plp ingresada
        #centrales = centrales.append(aux_df1)
        centrales_data.append(aux_df1)
        print(f'Central {id+1} de {cens} del caso ' + caso)
    centrales = pd.concat(centrales_data, ignore_index=True)
    parquet_file = os.path.join(parquet_dir, "centrales" +caso+ ".parquet")
    centrales.to_parquet(parquet_file, engine='pyarrow')