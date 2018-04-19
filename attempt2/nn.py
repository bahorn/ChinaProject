import json
import copy
import math
import numpy
import cProfile

import itertools

# Keras for the ML model
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout

def loadInFlavors(flavorFileName):
    flavorFile = open(flavorFileName, 'r')
    flavors = json.load(flavorFile)
    flavorVector = [[] for _ in range(len(flavors))]
    for flavor in flavors:
        flavorVector[flavor['id']] = flavor['scores']
    return flavorVector

# Layer that takes a vector of how much a user likes certain foods
def compressInput(likeVector, flavorVectors):
    compressed = [0 for _ in range(len(flavorVectors[0]))]
    n = len(likeVector)
    scaledValues = [0 for _ in range(n)]
    point = 0
    invN = 1.0/n
    while point < n:
        scale = likeVector[point]
        scaledValues[point] = [(i*scale)*invN for i in flavorVectors[point]]
        point += 1
    # join up
    for x in range(n):
        for y in range(len(scaledValues[x])):
            compressed[y] += scaledValues[x][y]
    return compressed

# Generates more test cases from a single input
def mutateTestCase(testcase, maxNTestcases=10):
    newTestCases = [testcase]
    activePos = []
    for n in range(len(testcase)):
        if n != 0:
            activePos.append(n)
    # Don't bother if nothing is in this testcase
    if len(activePos) == 0:
        return []
    else:
        # generate up to 5000 new examples by deactivating 5% of the active
        # neurons
        count = 0
        for combination in itertools.combinations(activePos,
                                        int(math.ceil(len(activePos)*0.05))):
            if count >= maxNTestcases:
                break
            newAttempt = copy.deepcopy(testcase)
            # deactivate
            for i in combination:
                newAttempt[i] = 0.0
            newTestCases.append(newAttempt)
            count += 1
    return newTestCases

# Get the data into a form we can use to train the Keras model
def preprocessData(dataFileName, flavorFileName):
    # load in data
    dataPointsX = []
    dataPointsY = []
    dataFile = open(dataFileName, 'r')

    flavorVector = loadInFlavors(flavorFileName)
    print('[!] Starting mutations')
    mutationCount = 0
    for item in json.load(dataFile):
        for testcase in mutateTestCase(item[0]):
            dataPointsX.append(compressInput(testcase, flavorVector))
            dataPointsY.append(item[1])
            if mutationCount%10 == 0:
                print('[!] Mutated '+str(mutationCount))
            mutationCount += 1
    return dataPointsX,dataPointsY

# the network
def likeNetworkTrain(
        epochs=100,
        batch_size=32,
        middleLayers=2,
        data='./data/data.json',
        flavors='./data/flavorValues.json'):
    print('[!] PreProcessing Data')
    dataPointsX, dataPointsY = preprocessData(data, flavors)
    nX = len(dataPointsX[0])
    nY = len(dataPointsY[0])
    dataX = numpy.array(dataPointsX)
    dataY = numpy.array(dataPointsY)
    print('[!] Creating Model')
    model = Sequential()
    model.add(Dense(nX, activation='relu', input_dim=nX))
    for layer in range(middleLayers):
        model.add(Dense(int(nY*1.1), activation='relu'))
    model.add(Dense(nY, activation='softmax'))
    model.compile(optimizer='adam',
              loss='binary_crossentropy',
              metrics=['accuracy'])
    print('[!] Training Model')
    model.fit(dataX, dataY, epochs=epochs, batch_size=batch_size)

# Query the pretrained network
def likeNetworkQuery(query, model='./model.dat',
                     flavorFileName='./data/flavorValues.json'):
    flavorVector = loadInFlavors(flavorFileName)
    testcase = compressInput(query, flavorVector)


if __name__ == "__main__":
    likeNetworkTrain()
    #print mutateTestCase([-1,-0.2,1,0.0,1,0.4,0.1,-0.4])
    #cProfile.run('preprocessData("./data/data.json", "./data/flavorValues.json")')
