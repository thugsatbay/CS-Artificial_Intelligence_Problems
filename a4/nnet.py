import numpy as np
import os
import sys
import random
import time
import pickle


class Layer:
    def __init__(self,
                 layer_size,
                 previous_layer_size,
                 learning_rate=0.01,
                 initialization='UNIFORM',
                 activation='SIGMOID',
                 isFinalLayer=False):

        self._EPSILON = np.finfo(np.float32).eps
        self.weights = np.random.random(size=(previous_layer_size, layer_size))
        self.v = np.zeros(shape=(previous_layer_size, layer_size))
        self.bias = np.zeros(shape=(layer_size, 1))
        self.momentum = 0.925
        self.batch_size = 4.00
        self.alpha = learning_rate
        self.layer_size = layer_size
        self.previous_layer_size = previous_layer_size
        self.isFinalLayer = isFinalLayer
        self.activation = np.vectorize(self.sigmoid)
        self.derivativeActivation = np.vectorize(self.derivativeSigmoid)
        self.previous_layer_values, self.z, self.a = None, None, None
        if initialization == 'NORMAL':
            print "Weight initialization Normal for layer", str(layer_size), 'mean : 0.0, std : 0.10', '---'
            self.weights = np.random.normal(loc=0.0, scale=0.10, size=(previous_layer_size, layer_size))
        self.store = np.zeros(shape=(previous_layer_size, layer_size))

    def forwardPropogation(self, previous_layer_values):
        self.previous_layer_values = np.array(previous_layer_values, copy=True)
        self.a = np.add(np.sum(np.multiply(
                                            self.weights.transpose(),
                                            self.previous_layer_values.reshape(1, self.previous_layer_size)
                                          ), axis=1).reshape(self.layer_size, 1), self.bias)
        self.z = self.activation(self.a)
        if self.isFinalLayer:
            #clip y_pred
            self.z = np.minimum(np.maximum(self.z, self._EPSILON), 1.00 - self._EPSILON)
        return self.z

    def checkPrediction(self, y_true, print_command=False):
        if print_command:
            print "Prediction for sample", \
                  str(y_true.reshape(1, self.layer_size)), "=", \
                  str(self.z).reshape(1, self.layer_size)
        return np.argmax(y_true) == np.argmax(self.z), np.argmax(self.z)

    def backwardPropogation(self, forward_layer_errors, iteration):
        forward_layer_errors = np.array(forward_layer_errors, copy=True)
        if self.isFinalLayer:
            forward_layer_errors = np.array(self.derivativeLossFunction(forward_layer_errors), copy=True)

        delta_error = np.multiply(self.derivativeActivation(self.a), forward_layer_errors)
        return_value = np.sum(np.multiply(self.weights,
                                          delta_error.reshape(1, self.layer_size)), axis=1).reshape(self.previous_layer_size, 1)


        self.store += np.multiply(self.previous_layer_values, delta_error.reshape(1, self.layer_size))
        if not iteration%int(self.batch_size):
            self.v = self.momentum * self.v - (self.alpha * (self.store/self.batch_size))
            self.weights = np.add(self.weights, self.v)
            self.bias = np.add(
                                    self.bias,
                                    -self.alpha * delta_error
                            )
            self.store = np.zeros(shape=(self.previous_layer_size, self.layer_size))
        return return_value

    def sigmoid(self, x):
        return 1.0 / (1.0 + np.exp(-x))

    def derivativeSigmoid(self, x):
        return self.sigmoid(x) * self.sigmoid(1 - x)

    def updateLearningRate(self, value):
        self.alpha /= value

    def derivativeLossFunction(self, y_true):
        return self.z - y_true

    def lossFunction(self, y_true):
        return 0.5 * np.multiply((self.z - y_true), (self.z - y_true))

    def modelValues(self):
        return (self.weights, self.bias, self.alpha, self.previous_layer_values, self.z, self.a)

    def loadValues(self, loadLayer):
        self.weights, self.bias, self.alpha, self.previous_layer_values, self.z, self.a = loadLayer


class NNet():
    def __init__(self,
                 layers,
                 lr_layers,
                 epochs,
                 log_cycle,
                 initialization='UNIFORM',
                 activation='SIGMOID'):

        self.train_X, self.input_dim = None, None
        self.layers = layers
        self.lr = lr_layers
        self.EPOCHS = epochs
        self.init = initialization
        self.act = activation
        self.model = []
        self.log_cycle = log_cycle

    def setEpochs(self, epoch):
        self.EPOCHS = epoch

    def setLayers(self, layers, lr_layers):
		self.layers = layers
		self.lr = lr_layers
		self.layers.insert(0, self.input_dim)

    def setTrainData(self, data):
        self.train_X, self.input_dim = data
        self.layers.insert(0, self.input_dim)

    def saveModel(self, file_name):
        save_model = []
        for layer in self.model:
            save_model.append(layer.modelValues())
        with open(file_name, 'wb') as handle:
            pickle.dump([save_model, self.input_dim, self.layers, self.lr], handle)

    def loadModel(self, fileName):
        save_model = None
        with open(fileName, 'rb') as handle:
            save_model, self.input_dim, self.layers, self.lr = pickle.load(handle)
        self.buildModel()
        for index, layer in enumerate(self.model):
            layer.loadValues(save_model[index])
        print "Previous Saved Model Loaded Successfully ..."

    def buildModel(self):
        for index in xrange(1, len(self.layers), 1):
            self.model.append(Layer
                                    (
                                        layer_size=self.layers[index],
                                        previous_layer_size=self.layers[index - 1],
                                        learning_rate=self.lr[index - 1],
                                        initialization=self.init,
                                        activation=self.act,
                                        isFinalLayer=index==(len(self.layers)-1)
                                    ),
                             )

    def startTraining(self):
        for epoch in xrange(self.EPOCHS):
            random.shuffle(self.train_X)
            random.shuffle(self.train_X)
            correct = 0.0
            for index, sample in enumerate(self.train_X):
                X, Y = sample[:-1]
                for each_layer in self.model:
                    X = each_layer.forwardPropogation(X)
                correct += self.model[-1].checkPrediction(Y)[0]
                if not (index+1)%self.log_cycle:
                     print "EPOCH", str(epoch + 1) + "/" + str(self.EPOCHS), "ITERATION", index, "ACCURACY:", correct/float(index + 1)
                     print "LOSS"
                     print str(self.model[-1].lossFunction(Y))
                     print "Y"
                     print str(Y)
                     print "PRED_Y"
                     print str(X)
                for each_layer in self.model[::-1]:
                    Y = each_layer.backwardPropogation(Y, index+1)
            if not (epoch + 1)%3:
                for each_layer in self.model:
                    each_layer.updateLearningRate(1.00 + 3.0/(float(epoch + 1)))
            print "EPOCH", str(epoch + 1) + "/" + str(self.EPOCHS), \
                  "ACCURACY:", (correct/float(len(self.train_X))) * 100.0


    def testing(self, data):
        response = []
        test_X, lenn = data
        correct = 0
        for sample in test_X:
            X, Y, file_name = sample
            for each_layer in self.model:
                X = each_layer.forwardPropogation(X)
            pred = (self.model[-1].checkPrediction(Y))
            correct += pred[0]
            response.append((file_name, str(pred[1] * 90)))
        print "TEST ACCURACY:", (correct/float(len(test_X))) * 100.0
        with open('output.txt', 'w') as f:
            for each_response in response:
                f.write(" ".join(each_response)+'\n')

OUTPUT_LABEL={
                0: np.array([1.0, 0.0, 0.0, 0.0]),
                90: np.array([0.0, 1.0, 0.0, 0.0]),
                180: np.array([0.0, 0.0, 1.0, 0.0]),
                270: np.array([0.0, 0.0, 0.0, 1.0])
            }

def dataLoader(fileName, norm_type=None):
    train_X = []
    with open(fileName, 'rb') as f:
        for line in f:
            data = line.replace('\n','').split(' ')
            feature = normalizeFeature(
                                        np.array([data[2:]],dtype=np.float32).reshape(len(data[2:]), 1),
                                        norm_type=norm_type)
            train_X.append((
                                feature,
                                OUTPUT_LABEL[int(data[1])].reshape(len(OUTPUT_LABEL), 1),
                                str(data[0])
                            ))
    print "Loaded Training Data in memory,", str(len(train_X)), "Feature Size", str(len(data[2:]))
    return train_X, len(data[2:])

def normalizeFeature(data, norm_type='MAX'):
    if norm_type=='MAX':
        return data/255.0
    return data

photoRotation = NNet(
                        layers=[64, 16, 4],
                        lr_layers=[0.04, 0.02, 0.01],
                        epochs=12,
                        log_cycle=10000,
                        initialization='NORMAL'
                    )
