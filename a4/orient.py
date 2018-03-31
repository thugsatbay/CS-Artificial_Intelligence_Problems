#!/usr/bin/env python
# =====================================================
# Assignment 4
# =====================================================
# Application of Machine Learning Algorithms
# Classify Images based on the orientation of Images
# Orientation Class: 0,90,180,270 Degrees
#
# ML Models:
#           K Nearest Neighbours (nearest)
#           AdaBoost (adaboost)
#           Neural Nets (nnet)
#           Best (best: Convolutional Neural Network???)
#
# Team members:
# Dhaval Niphade
# Gurleen Dhody
# Rashmi Bidanta
#
# Execute the program as below
# For Train:
# ./orient.py train train_file.txt model_file.txt [model]
# For Test:
# ./orient.py test test_file.txt model_file.txt [model]

# Image Source: http://www.flickr.com/photo_zoom.gne
# -----------------------------------------------------

import sys
import math
from knn import knntest, knnmodel
from nnet import photoRotation, dataLoader
from adaboost import AdaBoostTraining, AdaBoostTesting


def createModel(filename, model_file, model):
    if model == 'nearest':
        knnmodel(filename,model_file)
    elif model == 'adaboost':
        AdaBoostTraining(filename, model_file)
    elif model == 'nnet' or model == 'best':
		photoRotation.setTrainData((dataLoader(filename, norm_type='MAX')))
		photoRotation.setEpochs(epoch=9)
		photoRotation.setLayers(layers=[32, 32, 4], lr_layers=[0.04, 0.02, 0.01])
		photoRotation.buildModel()
		photoRotation.startTraining()
		photoRotation.saveModel(model_file)
    else:
        print 'Please provide valid input parameters!!'


def testModel(filename,model_file,model):
    if model == 'nearest':
        knntest(filename,model_file)
    elif model == 'adaboost':
        AdaBoostTesting(filename, model_file)
    elif model == 'nnet' or model == 'best':
        photoRotation.loadModel(model_file)
        photoRotation.testing(dataLoader(filename, norm_type='MAX'))
    else:
        print 'Please provide valid input parameters!!'


# Read in the input to the program
run_mode = sys.argv[1]
if run_mode == 'train':
    train_file, model_file, ml_model = sys.argv[2:]
    createModel(train_file, model_file, ml_model)
else:
    test_file, model_file, ml_model = sys.argv[2:]
    testModel(test_file, model_file, ml_model)
