#! /usr/bin/python
import random
import math
import operator


def maxVal(A, inicio, fim):  # Max nlogn sem a classe
    if fim - inicio <= 1:
        return max(A[inicio], A[fim])
    else:
        meio = (inicio + fim) / 2
        a = maxVal(A, inicio, meio)
        b = maxVal(A, meio + 1, fim)
        return max(a, b)


def minVal(A, inicio, fim):  # Min nlogn sem a classe
    if fim - inicio <= 1:
        return min(A[inicio], A[fim])
    else:
        meio = (inicio + fim) / 2
        a = minVal(A, inicio, meio)
        b = minVal(A, meio + 1, fim)
        return min(a, b)


def loadDataset(elementoV, lista):
    i = 0
    u = []
    for elemen in elementoV:  # 1000 pos
        u = elemen.split(" ")  # quebra as linhas onde tem espaco
        aux = []
        for x in u:  # 133 pos
            if i == 132:  # classe
                aux.append(x.strip(" "))
            if i != 132:
                aux.append(float(x.strip(" ")))
            i += 1
        i = 0
        lista.append(aux)


def euclideanDistance(instancia1, instancia2, tam):
    distancia = 0
    for x in range(tam):
        distancia += pow((instancia1[x] - instancia2[x]), 2)
    return math.sqrt(distancia)


def getNeighbors(treinoSet, testeInstancia, k):
    distancias = []
    tam = len(testeInstancia) - 1
    for x in range(len(treinoSet)):
        dist = euclideanDistance(testeInstancia, treinoSet[x], tam)
        distancias.append((treinoSet[x], dist))
    distancias.sort(key=operator.itemgetter(1))
    vizinhos = []
    for x in range(k):
        vizinhos.append(distancias[x][0])
    return vizinhos


def getResponse(vizinhos):
    votosClasses = {}
    for x in range(len(vizinhos)):
        resposta = vizinhos[x][-1]
        if resposta in votosClasses:
            votosClasses[resposta] += 1
        else:
            votosClasses[resposta] = 1
    votosClassificados = sorted(votosClasses.iteritems(), key=operator.itemgetter(1), reverse=True)
    return votosClassificados[0][0]


def getAccuracy(testeSet, predicoes):
    correto = 0
    for x in range(len(testeSet)):
        if testeSet[x][-1] == predicoes[x]:
            correto += 1
    return (correto / float(len(testeSet))) * 100.0


def minMaxNorm(vetor):  # Normaliza o vetor usando Min-Max
    cont = 0
    for elem in vetor:
        minmax = []
        maximo = maxVal(elem, 0, (len(elem) - 2))
        minimo = minVal(elem, 0, (len(elem) - 2))
        for norm in range(len(elem) - 1):
            minmax.append(
                (elem[norm] - minimo) / float(maximo - minimo)
            )
        minmax.append(elem[len(elem)-1])
        vetor[cont] = minmax
        cont += 1


def vermatrixconfusao(matriz_c):
    cont = 0


    for i in matriz_c:
        print repr(i) + "-> "+repr(cont)
        cont += 1

def main(i):
    arq = open("testing.data", 'r')
    arq2 = open("training.data", 'r')

    elementosTeste = arq.readlines()
    elementosTreino = arq2.readlines()

    # prepare data
    trainingSet = []
    testSet = []
    loadDataset(elementosTeste, testSet)
    loadDataset(elementosTreino, trainingSet)

    if i==1:
        print "Train set: " + repr(len(trainingSet))
        print "Test set: " + repr(len(testSet))
        print "Arquivos de Entrada: testing.data & training.data"

    matrix = []
    for k in range(10):
        matrix.append([0] * 10)

    #print 'Test[0] set: '+repr(len(testSet[0]))

    #normalize data
    minMaxNorm(testSet)
    minMaxNorm(trainingSet)
    #print 'Test[0] set norm: ' + repr(len(testSet[0]))

    # generate predictions
    predictions = []
    k = i

    #print k
    print('\n K = ' + str(k))

    #calcula para k-vizinhos
    for x in range(len(testSet)):
        neighbors = getNeighbors(trainingSet, testSet[x], k)
        result = getResponse(neighbors)
        predictions.append(result)
        #print('> predicted=' + repr(result) + ', actual=' + repr(testSet[x][-1]))
        aux = testSet[x][-1]
        matrix[int(aux)][int(result)] += 1

    vermatrixconfusao(matrix)
    accuracy = getAccuracy(testSet, predictions)
    print('Accuracy: ' + repr(accuracy) + '%\n')


if __name__ == "__main__":
    k = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19]
    for i in k:
        main(i)
