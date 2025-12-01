"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd

def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.

      
    """
    encabezados_raw,lineas_raw=subir_y_limpieza()
    
    nombres_columnas=generar_encabezados(encabezados_raw)
    clusters_ordenados=organizar_clusters(lineas_raw)
    base_datos=base_data(clusters_ordenados)

    df_final=limpieza_data(base_datos,nombres_columnas)
    return df_final

def subir_y_limpieza():    
    lineas=[]
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as f:
        i=0
        for line in f:
            line=line.lower()
            if i==0 or i==1:
#Al analizar el texto los encabezados si vienen bien separados, es
#decir que vienen separados por un doble espacio entre ellos
                line=encabezado(line)
            else:
                line=linea(line)
            if len(line) != 0:
                lineas.append(line)
            i+=1
    encabezados=lineas[:2]
    lineas=lineas[3:]
    return encabezados,lineas

def encabezado(line):
    #Eliminar los espacios antes y despues de cada línea
    line=line.strip()
    #Separar por espacios
    line=line.split("  ")
    #Elimino las elemento vacios para cada una de las lineas
    line=[x for x in line if x!=""]
    #Dentro de cada linea elimina los espacios en los elementos 
    # posteriormente nos puede servir para pegar las frases y vuelve 
    # el texto en minuscula
    line=[x.strip() for x in line]
    return line

def linea(line):
    #Eliminar los espacios antes y despues de cada línea
    line=line.strip()
    #Separar por espacios
    line=line.split(" ")
    #Elimino las elemento vacios para cada una de las lineas
    line=[x for x in line if x!=""]
    #Dentro de cada linea elimina los espacios en los elementos 
    # posteriormente nos puede servir para pegar las frases y vuelve 
    # el texto en minuscula
    line=[x.strip() for x in line]
    return line

def es_entero(x):
    try:
        int(x)
        return True
    except ValueError:
        return False
    
def organizar_clusters(lineas):    
    nueva_lista=[]
    linea=[]
    for i in lineas:
#Si el primer elemento de la lista es un número quiere decir que iniciamos
# un nuevo cluster
        if es_entero(i[0]):
#Si la linea existe lo pega
            if linea:
                nueva_lista.append(linea.copy())
            linea=[]
#Inicia pegando los clusters y su primera "Linea"
            linea.extend(i)
        else:
#Continua actualizando los clusters
            linea.extend(i) 
#Pega el ultimo cluster y limpia la linea para evitar que se pegue al inicio
    if linea:
        nueva_lista.append(linea)
        linea=[]
# Primero organizo las tres primeras columnas convirtiendolos en números 
# y columnas
    nueva_lista=[[int(item[0])]+[int(item[1])]+[float(item[2].replace(",","."))]+[x for x in item[4:]] for item in nueva_lista]
# Para organizar los items si llega a ser necesario porque no venían en orden los   
# clusters aunque eso es poco probable     
    nueva_lista.sort()
    return nueva_lista

def generar_encabezados(encabezados_raw):
#De la base de datos ya limpia, selecciono las dos filas donde 
# estan los nombres de cada columna, y la organizo
    encabezados=encabezados_raw.copy()
    encabezados[0][1]=encabezados[0][1]+" "+encabezados[1][0]
    encabezados[0][2]=encabezados[0][2]+" "+encabezados[1][1]
# Elimino la fila 2 que ya no sirve para nada, para luego entregar 
# los nombres de los encabezados eliminando los espacios por 
    encabezados=encabezados[0]
    encabezados=[x.replace(" ","_") for x in encabezados]
    return encabezados

def base_data(nb):    
    lista_completa=nb.copy()
    final=[]
# PARA CADA CLUSTER CREA las frases correspondientes a la 4ta columna
    for i in lista_completa:
        frase=""
        parte_1=i[:3]
# Pega los elementos según como toque y 
# deja siempre un espacio al final y por eso 
# antes de revisar para eliminar el punto final se hace un strip
        for d in i[3:]:
            frase+=d + " "
        frase=frase.strip()
# Elimina el punto final en las frases que lo contienen 
        if frase[-1]==".":
            frase=frase[0:-1]
#Pega la frase al cluster y luego el cluster a la lista que 
# contiene las filas de la base de datos
        parte_1.append(frase)
        final.append(parte_1)
    return final

def limpieza_data(datos,nombre_columnas):
    datos=pd.DataFrame(datos)
#Cambio el nombre de las columnas por los encabezados
    datos.columns=nombre_columnas
    return datos
