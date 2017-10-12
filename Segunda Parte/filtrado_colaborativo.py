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
        
    for key in datos:
        print(key)
    
    print('\n Los usuarios similares ♥ ♥ ♥ ' + usuario + ' son: \n')
    
    usuarios = usuarios_similares(datos, usuario, 3)
    
    print(usuarios)
    
    print('♦'*70)
    print('el score de similitud del usuario: ')
    print('♦'*70)
    
    all_movies = list()
    for item in usuarios: 
        if round(float(item[1]),2) > 0.0:
             print(item[0], round(float(item[1]),2))
             print(datos[item[0]])
             print(usuario)
             print(datos[usuario])
                
             value = { k : datos[item[0]][k] for k in set(datos[item[0]]) - set(datos[usuario]) }
             movies = list(value.keys())
             all_movies.append(movies)
                
             print('\n')
            
    flat_list = list()         
    for sublist in all_movies:
        for item in sublist:
            flat_list.append(item)
            
    newlist = list()
    for i in flat_list:
        if i not in newlist:
            newlist.append(i)
        
    print(newlist)             
             
