# **Inference**
The inference stage for different models are similar, but you should be careful with the shape of CSI.

Below is the basic steps of the inference of the CNN model.

1. First, we need to load all another set of CSI samples for the 5 devices, the steps are similar to those when doing the preprocess steps before training
2. Second, give new labels to the samples so that we can plot the confusion matrix. Note, this step can be ignored if you donot want to plot the confusion matrix.
3. Next, compare the predicted label with the true label.
4. Finnaly, show in result in confusion matrix.

The entire script can be found in 'cnn_inf.py'. 

*Updated in Semester 2 Week 7*

