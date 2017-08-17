from sklearn import datasets
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split
import numpy as np
from numpy import linalg as LA

# Importar data de sklearn
iris = datasets.load_iris()
X = iris.data[:,[2,3]]
y = iris.target

# Separar los datos de entranamiento y los de test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


# Tecnica de remoción
def remocion_train(X) :
    X = X - X.mean(axis=0)
    X = X/X.std(axis=0)

    return X

def remocion_test(X_test) :
    media = X_train.mean(axis=0)
    desviacion = X_train.std(axis=0)

    X_test = X_test - media
    X_test = X_test/desviacion

    return X_test

# Tecnica de Binarizacion
def binarizacion(X,gamma) :
    filas = np.shape(X)[0]
    columnas = np.shape(X)[1]

    for i in range(filas) :
        for j in range(columnas) :
            X[i][j] = 1 if X[i][j] >= gamma else 0

    return X

# Tecnica de Escalamiento
def escalamiento(X) :
    X = X - X.min(axis=0)
    X = X/(X.max(axis=0) - X.min(axis=0))

    return X

# normalizacion l1
def normalizacion_uno(X) :
    norm = LA.norm(X, ord=1, axis=1)

    filas = np.shape(X)[0]
    columnas = np.shape(X)[1]

    for i in range(filas) :
        X[i][:] =  X[i][:] / norm[i]
    return X

# normalizacion l2
def normalizacion_dos(X) :
    norm = LA.norm(X, ord=2, axis=1)

    filas = np.shape(X)[0]
    columnas = np.shape(X)[1]

    for i in range(filas) :
        for j in range(columnas) :
            X[i][j] =  X[i][j] / norm[i]
    return X


def resultados_clasficador(x_train_norm, x_test_norm) :
    valores_de_c =[ 20.0, 40.0, 60.0, 80.0, 100.0, 1000.0, 10000.0, 100000.0, 1000000.0, 10000000.0]

    for c in valores_de_c :
        clasificador = LogisticRegression(C=c, random_state=0)
        clasificador.fit(x_train_norm, y_train)
        y_pred = clasificador.predict(x_test_norm)

        iguales = (y_test == y_pred).sum()
        print('C = %d - muestras iguales %d/%d' %(c, iguales, len(y_pred)))

print("Técnicas\n1 - Remoción\n2 - Binarización\n3 - Escalamiento\n4 - Normalizacion L1\n5 - Normalizacion L2")
tecnica = int(input('Que técnica desea realizar? '))

if tecnica == 1:
    print('\n- Remoción - \n')
    x_train_norm = remocion_train(X_train)
    x_test_norm = remocion_test(X_test)
elif tecnica == 2:
    print('\n- Binarización - \n')
    gamma = ( X_train.min() + X_train.max())/2
    x_train_norm =  binarizacion(X_train, gamma)
    x_test_norm =  binarizacion(X_test, gamma)
elif tecnica == 3:
    print('\n- Escalamiento - \n')
    x_train_norm = escalamiento(X_train)
    x_test_norm = escalamiento(X_test)
elif tecnica == 4:
    print('\n- Normalizacion L1 - \n')
    x_train_norm = normalizacion_uno(X_train)
    x_test_norm = normalizacion_uno(X_test)
elif tecnica == 5:
    print('\n- Normalizacion L2 - \n')
    x_train_norm = normalizacion_dos(X_train)
    x_test_norm = normalizacion_dos(X_test)

resultados_clasficador(x_train_norm, x_test_norm)
