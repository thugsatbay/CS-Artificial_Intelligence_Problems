#!usr/bin/env python2
import math
import numpy as np
import time
from operator import itemgetter



def knnmodel(filename, model_file):
    fmodel = open(model_file, 'w')
    with open(filename, 'rb') as train_file:
        for line in train_file:
            data = line.split(' ')
            fmodel.write(' '.join(data[1:]))
    fmodel.close()


# This method calculates the Cosine distance between two feature vectors
def cosineDist(modelVec, testVec):
    m_array = np.asarray(map(int,modelVec))
    t_array = np.asarray(map(int,testVec))
    return np.dot(m_array,t_array)/ (np.linalg.norm(m_array)*np.linalg.norm(t_array))


# This method calculates the Euclidean Distance / Norm-2 between two feature vectors
def norm2Distance(modelVec, testVec):
    #return np.linalg.norm(np.asarray(map(int,modelVec))-np.asarray(map(int,testVec)))
    return int(np.linalg.norm(modelVec-testVec))


def findDominantNeighbor(model, test_image_instance, k=5):

    n_distance = []
    for pos, model_image in enumerate(model):
        dist_fm_mimage = norm2Distance(model_image[1:], test_image_instance[1:])
        n_distance.append((model_image, dist_fm_mimage))

    n_distance = sorted(n_distance, key=lambda x : x[1])

    k_neighbours = [n_distance[i][0] for i in xrange(k)]
    neighbor_count = {}
    for item in k_neighbours:
        if item[0] in neighbor_count:
            neighbor_count[item[0]] += 1
        else:
            neighbor_count[item[0]] = 1

    return max(neighbor_count.items(), key=lambda x: x[1])[0]


def knntest(test_file, model_file):

    accuracy = 0.0
    correct = 0
    totalTestImages = 0
    model = []
    with open(model_file, 'rb') as mfile:
        for line in mfile:
            image_data = line.replace('\n', '').split(' ')
            model.append(np.asarray(map(int,image_data)))

    test = []
    with open(test_file, 'rb') as tfile:
        for line in tfile:
            test.append(line.replace('\n', '').split(' '))
    output = open('output.txt','w')
    for test_image in test:
        totalTestImages += 1
        knn_orient = findDominantNeighbor(model, \
        np.asarray(map(int,test_image[1:])),int(math.sqrt(len(model))))
        output.write(test_image[0]+' '+str(knn_orient)+'\n')
        if knn_orient == int(test_image[1]):
            correct += 1
    accuracy = float(correct) / float(totalTestImages)
    print 'Accuracy:    ', accuracy*100, '%'
