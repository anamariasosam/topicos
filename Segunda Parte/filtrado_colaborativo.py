import argparse
import json
import numpy as np


from Similitud import score_pearson


# definimos la funcion para el paso de argumento de consola

def lector_argumentos():
    lector = argparse.ArgumentParser(description = 'Encontrar usuario similar al de entrada')
    lector.add_argument('--usuario', dest = 'user', required = True, help = 'El usuario de entrada')
    
    return lector


def usuarios_similares(datos, usuario, numero_usuarios):
    if usuario not in datos:
        raise TypeError('No puede encontrar el usuario' + usuario + 'en la base de datos')
        
    # calculamos los scores
    
    scores = np.array([[x, score_pearson(datos, usuario, x)] for x in datos if x != usuario])
    
    score_ordenado = np.argsort(scores[:,1])[::-1]
    
    
    # selecciona los primeros usuarios
    top = score_ordenado[:numero_usuarios]
    return scores[top]


if __name__ == '__main__':
    argumentos = lector_argumentos().parse_args()
    usuario = argumentos.user
    archivo = 'ratings.json'
    
    with open(archivo, 'r') as f:
        datos = json.loads(f.read())
        
    print('â€¢ '*27)
    print('Hola ' + usuario + ' te recomendamos las siguientes pelÃ­culas:')
    
    usuarios = usuarios_similares(datos, usuario, 3)
    
    all_movies = list()
    for item in usuarios: 
        if round(float(item[1]),2) > 0.0:
             values = { k : datos[item[0]][k] for k in set(datos[item[0]]) - set(datos[usuario]) }
             all_movies.append(values.keys())

            
    flat_list = list()         
    for sublist in all_movies:
        for item in sublist:
            if item not in flat_list:
                flat_list.append(item)
                
    for movie in flat_list:
        print(' â™¥ ' + movie) 

    print('â€¢ '*26)
             
