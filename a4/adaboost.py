from random import random, randint
from sys import argv, maxint
import time
import numpy as np
import math
import copy
import pickle


def read_files(file_name):
    files = {}
    with open(file_name, 'r') as f:
        for line in f:
            data = line.replace("\n", "").split()
            img = np.array(data[2:], dtype=np.float16)
            orientation = int(data[1])
            files[(data[0], orientation)] = {"orientation": orientation, "image": img}
    return files

def getBestAttribute(boost, imageOrient, data):
	for sample in data:
		for pixel in boost:
			if (data[sample]["image"][pixel[0]] > data[sample]["image"][pixel[1]] and data[sample]["orientation"] == imageOrient) \
                or (data[sample]["image"][pixel[0]] < data[sample]["image"][pixel[1]] and data[sample]["orientation"] != imageOrient):
				boost[pixel] += data[sample]["weight"]
	return max([(boost[pixel], pixel) for pixel in boost], key= lambda x: x[0])

def initializeWeight(train, totalCount):
	for sample in train:
		train[sample]["weight"] = 1.0/totalCount

def normalize(normalizeValue, data):
	for sample in data:
		data[sample]["weight"] = data[sample]["weight"]/normalizeValue

def modifyWeight(modifier, pixel, imageOrient, data):
	newWeight = 0.0
	for sample in data:
		if (data[sample]["image"][pixel[0]] > data[sample]["image"][pixel[1]] and data[sample]["orientation"] == imageOrient) \
            or (data[sample]["image"][pixel[0]] < data[sample]["image"][pixel[1]] and data[sample]["orientation"] != imageOrient):
			data[sample]["weight"] *= modifier
		newWeight += data[sample]["weight"]
	return newWeight

def AdaBoostTraining(dataFileName, modelFileName):
    train_data = read_files(dataFileName)

    stump_count = 64
    count_Train = len(train_data)

    adaboost = {}
    orientation = [0, 90, 180, 270]
    pixelx, pixely = None, None
    for stump in xrange(stump_count):
        while True:
            pixelx = randint(0,191)
            pixely = randint(0,191)
            if abs(pixelx - pixely) < 8:
                continue
            if (pixelx, pixely) not in adaboost:
                break
        adaboost[(pixelx, pixely)] = 0

    # Adaboost ensembler for each decision
    all_orientation_stump = {}
    for orient in orientation:
        print "Calculating stumps for Orientation,", str(orient), "..."
        bestAttribute = []
        initializeWeight(train_data, count_Train)

        newAdaBoost = copy.deepcopy(adaboost)
        for stump in xrange(stump_count):

            # value, pixel, beta
            bestAttribute.append(getBestAttribute(newAdaBoost, orient, train_data))

            # redundant statement will always be one?
            totalWeight = sum([train_data[sample]["weight"] for sample in train_data])

            # Prevent division by 0
            error = min(0.99, (totalWeight - bestAttribute[stump][0]) / float(totalWeight))

            beta = (error)/(1.0 - error)

            # Stores the weights of the decision stump based on error
            bestAttribute[stump] += ((1.0 + math.log(1.0/beta)),)

            normalizeWeight = modifyWeight(beta, bestAttribute[stump][1], orient, train_data)

            normalize(normalizeWeight, train_data)

            # Delete pixel stump
            del newAdaBoost[bestAttribute[stump][1]]

            for key in newAdaBoost:
                newAdaBoost[key] = 0

        all_orientation_stump[orient] = bestAttribute[:]
    with open(modelFileName, 'wb') as handle:
        pickle.dump(all_orientation_stump, handle)

    accuracy(train_data, all_orientation_stump)

def AdaBoostTesting(dataFileName, modelFileName):
    test_data = read_files(dataFileName)

    with open(modelFileName, 'rb') as handle:
        all_orientation_stump = pickle.load(handle)
    print "Previous Saved Model Loaded Successfully ..."
    # Essembler for each orientation is executed on test data, the one with the best value is classified
    accuracy(test_data, all_orientation_stump, testing=True)

def accuracy(data, all_orientation_stump, testing=False):
    response = []
    count_correct = 0.0
    for sample in data:
        finalDecision = {}
        for orient in all_orientation_stump:
            decisionValue = 0.0
            for orient_decision_stump in all_orientation_stump[orient]:
                pixel = orient_decision_stump[1]
                decisionValue += orient_decision_stump[2] * (1.0 if (data[sample]["image"][pixel[0]] > data[sample]["image"][pixel[1]]) else -1.0)
            finalDecision[orient] = decisionValue
        decisionOrient = max(finalDecision.items(), key = lambda x: x[1])
        if testing:
            response.append((sample[0], str(int(decisionOrient[0]) * 90 )))
        if int(data[sample]["orientation"]) == int(decisionOrient[0]):
            count_correct += 1

    print "Accuracy: " + str( (count_correct * 100.0) / len(data) )
    if testing:
        with open('output.txt', 'w') as f:
            for each_response in response:
                f.write(" ".join(each_response)+'\n')
