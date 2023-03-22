# **Deep Learning and RFFI**
The key idea behind RFF is to **extract unique patterns (or features) and use them as signatures to identigy devices**.

features at:
+ physical layer
+ control (MAC) payer
+ upper layers

Loaction-based features are susceptible to mobility and envirmental changes: 
+ RSS - radipp signal strength
+ CSI - channel statement information

[![IMG-1778.jpg](https://i.postimg.cc/52KFpfZK/IMG-1778.jpg)](https://postimg.cc/NKTMjvGR)

## **Supervised Learning**
Requires a large collection of **labeled** samples.
### **similarity-based**
+ supervised Batesian

### **classification-based**
#### **Conventional**
  + I/Q imbalance
  + phase imbalance
  + frequency error
  + received signal strength
  + etc.

possible models: 
+ KNN - k-nearest neighbours
+ SVM - support vector machine
+ GTID using artificial neural networks

#### **Deep Learning**
Apply deep learning at the physical layer.
+ offers a powerful framework for supervised learning approach
+ learn functions of increasing complexity
+ leverage large datasets
+ greatly increase the layers

## **Unsupervised Learning**
Effective when there are **no prior label** information about the device.

## **CNN Architecture**

[![IMG-1779.jpg](https://i.postimg.cc/qvhsCtFM/IMG-1779.jpg)](https://postimg.cc/Js8Dfhm9)

+ pooling layer
  + downsamples the feature maps
  + reduce dimentsionality of the feature map
  + in turn reduces the number of parameters and computation in network
+ fully connected or dense layer
  + traditional multi layer perceptron (MLP)
  + neurons have full connections to all activation steps in previous layer

### **Model Selection**
+ number of filters
  +  computation complexity
  +  performance
+ prevent overfitting
  + regularization parameters
  + dropout rate