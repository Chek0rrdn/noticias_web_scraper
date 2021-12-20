
# Scraper para sitios de Noticias

  

## Introducción

  

El siguiente proyecto sirve para descargar noticias de artículos de una manera automática de diferentes páginas de noticas vía URL.

  

## Instalación

  

>  **Note**: Para ejecutar con éxito el programa, se tiene que ejecutar el siguiente comando para instalar las dependencias necesarias de Python que se encuentran en el archivo de requirements.txt:

  
  

```sh
pip3 install -r requirements.txt
```

## Uso del Scraper
Para utilizar el programa utilice la siguiente sintaxis:
```sh
python3 main.py <sitio_de_noticias>
```
 **Note**: en caso de no asaber cuales son los sitios de noticias disponibles, utilice el siguiente comandoe, el cual le proporcionara los sitios validos.
```sh
python3 main.py -h
```

## Uso de la receta para la limpieza de los Datos
Una vez se utiliza el scraper, éste genera archivos de extension .csv el cual los guarda en una carpeta de nombre **Files**. Estos son los archivcos que por su naturaleza vienen de una forma sucia, y deben ser limpiados.
Para utilizar la Receta y limpiar los datos utilice ella siguiente sintaxis:
 ```sh
python3 newspaper_receipe.py <ruta_del_archivo>
```
 **Note**: en caso de no asaber cuales son los archivos, utilice el siguiente comandoe, el cual le proporcionara los archivos.
```sh
python3 newspaper_receipe.py -h
```