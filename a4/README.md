# Assignment 4 Machine Learning Techniques

### Team Members: Dhaval Niphade, Gurleen Singh Dhody, Rashmi Ranjan Bidanta

### Problem Statement

Classify the images based on its orientation into following categories

**0-degree** ![Zero](./images/18079654.jpg)
**90-degree** ![Ninty](./images/6568344.jpg)
**180-degree** ![180](./images/9476980.jpg)
**270-degree** ![270](./images/19712937.jpg)

### Algorithms:
* K-Nearest Neighbour
* AdaBoost
* Neural Network
* Best Algorithm


#### __K-Nearest Neighbor__

***Parameters:***
* *Distance measure:* Euclidean and Cosine.
* *K-Parameter:* Tested for 5 and 193 neighbors

***Training:*** The training model is "No Model". Takes all the training data as input.
*Time Taken:* Negligible

***Testing:*** Testing takes the most time as the Algorithm compares how far a test feature is from the training features of all the categories/orientation.

***Performance:***

| K  | Time            | Accuracy    |
| ---|:--------------: | :---------: |
| 5  |  5m15.799s      | 69.0349%    |
| 193|  5m28.544s      | 71.3679%    |

Test performance was slow, however the linear algebra library from Numpy helped in improving the timing but still it takes close to 5 minutes for 71% accuracy

#### __AdaBoost__

***Parameters:***
Decision Stumps as weak classifier. Simple pixel intensity comparison as a model for creating Decision stumps.


***Training:***  We compare the pixel values randomly over 192 pixels across R,G and B channels and take each comparison as a decision stump to build several weak classifiers. Since this is a multi-class classification problem we used One-Vs-All approach for classification.

***Performance:***

|Decision Stumps|Training - Accuracy|Testing - Accuracy|
|---------------|-------------------|------------------|
| 48  | 66.13%  | 62.14% |
| 64 | 68.17% | 65.21% |
| 128 | 70.35% | 66.60% |

The time taken for 64 stump adaboost was 7 mins and 56 seconds for training.

The default model is the 64 decision stumps for adaboost. To change it one needs to edit the stump_count variable in the adaboost.py file.

#### __Neural Network__

***Parameters Considered:***
* *Hidden Layers*
* *Neurons*
* *Epochs*
* *Learn Rate*

***Training:*** Generate a model of weights and biases that minimizes the cost of determining image orientation. During training we used [Stochastic Gradient Descent](https://en.wikipedia.org/wiki/Stochastic_gradient_descent) taking average gradient of 4 images in a batch. We also used [Momentum](https://en.wikipedia.org/wiki/Stochastic_gradient_descent#Momentum) to update the weights. For all models we have taken variable learning rate, different for each layer, reducing with time.

***Testing:*** Forward pass on each image and taking the maximum of neuron value in the output layer.

***Performance:***

|Hidden Layers | Neurons | Epochs  |Learn Rate|Accuracy - Training|Accuracy - Testing|
| ---          | ------- | ------  |----------|--------|----------|
| 1            |   64    |    9     |  [0.03, 0.01]      |    76.97%    |    73.5%      |
| 1            |   32    |      9   |  [0.03, 0.01]        |   76.73%     |    74.02%      |
| 2            |  64x16  |    9     | [0.04, 0.02 0.01]         |   77.15%     |   74.55%       |
| 2            |  32x32  | 9     |  [0.04, 0.02 0.01]    |   76.76     |     74.86%     |

For NNet we are currently using the 32x32. Though you can change the layers learning rate and epochs in the orient.py file itself.

#### __Best Model__
The best model is also the Neural network model, which is the 32x32

#### Other Reference:
[3BlueOneBrown](http://www.3blue1brown.com/videos/2017/10/9/neural-network)

[Back propagation Demystified](https://ayearofai.com/rohan-lenny-1-neural-networks-the-backpropagation-algorithm-explained-abf4609d4f9d)

[Linear Algebra in ANN](https://sudeepraja.github.io/Neural/)

[Adaboost Multi-class Classification](http://ieeexplore.ieee.org/document/5597629/?reload=true)
