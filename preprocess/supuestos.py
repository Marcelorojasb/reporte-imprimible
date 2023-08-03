import os
import pandas as pd
import numpy as np
from datetime import date
from dateutil.relativedelta import relativedelta

# ************* Directorio donde se guardarán los parquets: *************
parquet_dir='/Users/marcelo/Downloads/NeoCity/Projects/dash/Parquet_notebooks/parquets'
#parquet_dir='/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/2. PLP2023'



# Caso Base
datafile='/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/2. PLP2023/OPLP20230325/plpcen.csv'
#datafile=r'G:\Unidades compartidas\5. Reportes\01. Pruebas PLP\3. Prog. 2022.09\plpcen.csv' # Windows
cen_df=pd.read_csv(datafile)


# Demanda
datafile='/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/2. PLP2023/OPLP20230325/IPLP20230325.xlsm'
dem_df=pd.read_excel(datafile, sheet_name='Consumo', skiprows=[0,1,2], usecols=[0,1,2,3,4,5,6,7,8])
years = dem_df['Año'].values
for id, i in enumerate(years):
    if np.isnan(i):
        years[id] = int(curr)
    else:
        curr = i
dem_df['Año'] = years
parquet_file = os.path.join(parquet_dir, "consumo" + ".parquet")
dem_df.to_parquet(parquet_file, engine='pyarrow')

# Combustibles
datafile='/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/2. PLP2023/OPLP20230325/IPLP20230325.xlsm'
comb_df=pd.read_excel(datafile, sheet_name='Combustibles SEN', skiprows=[0]+[i for i in range(583,727)]).astype(str)
parquet_file = os.path.join(parquet_dir, "combustible" + ".parquet")
comb_df.to_parquet(parquet_file, engine='pyarrow')

# Plan de obras
datafile='/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/2. PLP2023/OPLP20230325/plpcen.csv'
#datafile=r'G:\Unidades compartidas\5. Reportes\01. Pruebas PLP\3. Prog. 2022.09\plpcen.csv' # Windows
cen_df=pd.read_csv(datafile)
cen_df=cen_df.loc[cen_df['Hidro'].str.strip()=='MEDIA']
datafile='/Users/marcelo/Library/CloudStorage/GoogleDrive-marcelo.rojas@neocity.cl/Unidades compartidas/5. Reportes/24. Prueba_PLP/2. PLP2023/OPLP20230325/IPLP20230325.xlsm'
planObras_df=pd.read_excel(datafile, sheet_name='Plan de Obras(5)', skiprows=[0,1,2,3], usecols=[1,2,3])
aux = planObras_df['CENTRAL'].values
pmax = []
tipo = []
for i in aux:
    cen_df1 = cen_df.loc[cen_df['CenNom'].str.strip() == i] # Se buscan datos de la central "i"
    pmax.append(max(cen_df1['CenPMax'].values))
    tip = i[-2:]
    if tip == 'FV' or tip == 'EO':
        tipo.append(tip)
    else:
        tipo.append('otro')
planObras_df['pmax']=pmax
planObras_df['tipo']=tipo
planObras_df['INICIAL']=pd.to_datetime(planObras_df['INICIAL'])
planObras_df['FINAL']=pd.to_datetime(planObras_df['FINAL'])
parquet_file = os.path.join(parquet_dir, "planDeObras" + ".parquet")
planObras_df.to_parquet(parquet_file, engine='pyarrow')