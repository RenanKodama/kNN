#! /usr/bin/python
import random
import math
import operator


def maxVal(A, init, end):  # Max nlogn sem a classe
    if end - init <= 1:
        return max(A[init], A[end])
    else:
        m = (init + end) / 2
        v1 = maxVal(A, init, m)
        v2 = maxVal(A, m + 1, end)
        return max(v1, v2)


def minVal(A, init, end):  # Min nlogn sem a classe
    if end - init <= 1:
        return min(A[init], A[end])
    else:
        m = (init + end) / 2
        v1 = minVal(A, init, m)
        v2 = minVal(A, m + 1, end)
        return min(v1, v2)


def loadDataset(vetorElemen, lista):
    i = 0
    aux = []
    for elemen in vetorElemen:  # 1000 pos
        aux = elemen.split(" ")  # quebra as linhas onde tem espaco
        aux2 = []
        for x in aux:  # 133 pos
            if i == 132:  # classe
                aux2.append(x.strip(" "))
            if i != 132:
                aux2.append(float(x.strip(" ")))
            i += 1
        i = 0
        lista.append(aux2)


def euclideanDistance(instance1, instance2, length):
    distance = 0
    for x in range(length):
        distance += pow((instance1[x] - instance2[x]), 2)
    return math.sqrt(distance)


def getNeighbors(trainingSet, testInstance, k):
    distances = []
    length = len(testInstance) - 1
    for x in range(len(trainingSet)):
        dist = euclideanDistance(testInstance, trainingSet[x], length)
        distances.append((trainingSet[x], dist))
    distances.sort(key=operator.itemgetter(1))
    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])
    return neighbors


def getResponse(neighbors):
    classVotes = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classVotes:
            classVotes[response] += 1
        else:
            classVotes[response] = 1
    sortedVotes = sorted(classVotes.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedVotes[0][0]


def getAccuracy(testSet, predictions):
    correct = 0
    for x in range(len(testSet)):
        if testSet[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(testSet))) * 100.0


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
