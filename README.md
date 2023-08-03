# Reporte demo imprimible

Esta versión corresponde a la versión de deployment, es decir, no posee activado el debugger y se inicia el servicio mediante imágenes de Docker ya sea de forma local o web usando Gcloud.

## Getting Started

Para crear el entorno virtual (fuera del directorio de trabajo) y activarlo.

```
virtualenv venv

# Windows
venv\Scripts\activate
# Or Linux
source venv/bin/activate

```

Clonar el repositorio de git e instalar las librerías con pip

```

gh repo clone Marcelorojasb/reporte-imprimible
pip install -r requirements.txt


```

### Ejecutar la aplicación de manera local
Para ejecutar la aplicación, se debe tener instalado docker. Luego, para crear y ejecutar la imagen:

```

docker-compose build
docker-compose up -d

```
### Ejecutar la aplicación en Gcloud
Primero autenticarse e ingresar a la carpeta de trabajo en Gcloud reporte-piloto-dev con:

```

Gcloud init

```
Subir la imagen (se guardara en el contenedor de registros en la carpeta dash):
```

gcloud builds submit --tag gcr.io/reporte-piloto-dev/dash

```

## Sobre la app

Este demo contiene solo la simulación del caso base (sin fallas) y una simulación de falla (falla central Andina). La arquitectura de la aplicación está pensada para escalarla a más simulaciones o actualizaciones de datos de forma sencilla.

Para agregar los datos se deben realizar básicamente 2 pasos una vez se tengan los csv resultantes de la simulación del modelo plp. 

- Preprocesar los csv: En la carpeta [preprocess](/preprocess) se encuentran 3 archivos de python (La actualización de margen planta y contrato se puede realizar sin actualizar los supuestos, esto es, solo con los archivos centralesbarras.py y retiros.py). En aquellos archivos, se debe seleccionar la carpeta en donde se encuentran los csv. Luego, se deben ejecutar los 3 archivos (o 2 en caso de no usar el archivo supuestos.py). Como resultado, se obtendrán 8 parquets (5 en caso de no actualizar supuestos) que serán guardados en la carpeta de destino seleccioanada en cada uno de los archivos de python. Esos parquets deben ser agregados a la carpeta [data](/data) (o reemplazar los archivos existentes en caso de solo querer actualizar)
- Agregar archivos en el código: En los archivos margen-contrato.py, margen-planta.py, resumen.py y tablas.py de la carpeta [pages](/pages), cambiar los nombres del los parquets en caso de que se hayan cambiado o agregar los parquets adicionales (nueva falla).

## Built With

- [Dash](https://dash.plot.ly/) - Main server and interactive components
- [Plotly Python](https://plot.ly/python/) - Used to create the interactive plots

