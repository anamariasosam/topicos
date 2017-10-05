# -*- coding: UTF-8 -*-

import argparse #leer argumentos de la consola
import json # leer archivos json
import numpy as np


# funcion para leer argumentos

def lector_argumentos():
    lector = argparse.ArgumentParser(description = 'Cálculo del score de similitud')
    lector.add_argument('--elele1', dest = 'elele1', required = True, help = 'El elele1 es el primer usuario')
    lector.add_argument('--elele2', dest = 'elele2', required = True, help = 'El elele2 es el segundo usuario')
    lector.add_argument('--elele-score', dest = 'elele_score', required = True, choices = ['Euclidiano', 'Pearson'], help = 'El elele-score es la medida de similitud')
    
    return lector


def score_euclidiano(datos, elele1, elele2):
    # comprobamos que los usuario estén en la base de datos 
    if elele1 not in datos: 
        raise TypeError('No puedo encontrar a ese elele 1 en la base de datos')
    if elele2 not in datos: 
        raise TypeError('No puedo encontrar a ese elele 2 en la base de datos')
        
    peliculas_comunes = {} 
    
    for item in datos[elele1]:
        if item in datos[elele2]:
            peliculas_comunes[item] = 1
    
    if len(peliculas_comunes) == 0:
        return 0
    
    # calculamos el score euclidiano si tenemos peliculas en comun 
    
    cuadrado_diferencias = []
    
    for item in datos[elele1]:
        if item in datos[elele2]:
            euclidiano = np.square(datos[elele1][item] - datos[elele2][item])
            cuadrado_diferencias.append(euclidiano)
    score = 1 / (1 + np.sqrt(np.sum(cuadrado_diferencias)))
    
    return score


def score_pearson(datos, elele1, elele2):
    # comprobamos que los usuario estén en la base de datos 
    if elele1 not in datos: 
        raise TypeError('No puedo encontrar a ese elele 1 en la base de datos')
    if elele2 not in datos: 
        raise TypeError('No puedo encontrar a ese elele 2 en la base de datos')
        
    peliculas_comunes = {} 
    
    for item in datos[elele1]:
        if item in datos[elele2]:
            peliculas_comunes[item] = 1
    
    if len(peliculas_comunes) == 0:
        return 0
    
    # calculamos la suma de los rating de todas las peliculas en comun
    suma_usuario1 = np.sum([datos[elele1][item] for item in peliculas_comunes])
    suma_usuario2 = np.sum([datos[elele2][item] for item in peliculas_comunes])

    # Calculamos la suma de los cuadrados
    cuadrados_usuario1 = np.sum([np.square(datos[elele1][item]) for item in peliculas_comunes])
    cuadrados_usuario2 = np.sum([np.square(datos[elele2][item]) for item in peliculas_comunes])
    
    suma_productos = np.sum([datos[elele1][item]*datos[elele2][item] for item in peliculas_comunes])
    
    # indices de Pearson
    Sxy = suma_productos - (suma_usuario1*suma_usuario2 / len(peliculas_comunes))
    Sxx = cuadrados_usuario1 - (np.square(suma_usuario1) / len(peliculas_comunes))
    Syy = cuadrados_usuario2 - (np.square(suma_usuario2) / len(peliculas_comunes))
    
    # si no hay desviacion el score es cero
    
    if Sxx*Syy == 0:
        return 0
    
    # retornamos el score de Pearson
    return Sxy/np.sqrt(Sxx*Syy)

# EL MAIN

if __name__ == '__main__':
    argumentos = lector_argumentos().parse_args()
    elele1 = argumentos.elele1
    elele2 = argumentos.elele2
    tipo_score = argumentos.elele_score
    
    
    # cargamos los datos
    
    archivo = 'ratings.json'
    
    with open(archivo, 'r') as f:
        datos = json.loads(f.read())
        
    for key in datos:
        print(key)
        
    # calculamos la similitud
    if tipo_score == 'Euclidiano':
        print('\n El score Euclidiano es: ')
        print(score_euclidiano(datos, elele1, elele2))
    else: 
        print('\n El score Pearson es: ')
        print(score_pearson(datos, elele1, elele2))