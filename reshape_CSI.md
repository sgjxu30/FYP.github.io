# **Reshape CSI**
## **Complex number to Magnitude and Phase**
The combined CSI is a 2D array, whose number of columns is the number of all the CSI samples, and number of rows is 56, which stands for 56 subcarriers.

However, the element inside the array is a complex number, so we need to use functions to convert it to magnitude and phase.

This is simply done with the code below.
```Python
magnitude = np.abs(combined_csi)
phase = np.angle(combined_csi)
```

## **StandardScaler**
'StandardScaler' is a class in scikit-learn that scales the input data to have zero mean and unit variance. This is a common preprocessing step in machine learning to ensure that features are on the same scale and to prevent some features from dominating others. 
```Python
scaler = StandardScaler()
magnitude = scaler.fit_transform(magnitude.T).T
phase = scaler.fit_transform(phase.T).T
```

'magnitude.T' and 'phase.T' transpose the matrices magnitude and phase, respectively. 
+ This is done to ensure that the scaling is done along the correct axis.

The 'fit_transform' method of 'scaler' is then called on the transposed 'magnitude' and 'phase' matrices. 
+ This method first fits the scaler to the data, computing the mean and standard deviation for each feature. 
+ It then transforms the data by subtracting the mean and dividing by the standard deviation. 
+ The resulting data is returned as a new array, which is then transposed back to its original shape using the '.T' method.

## **Reshape the data for CNN training**
Then the data need to be reshaped to fit the CNN model.
```Python
# Reshape the data for CNN (num_samples, num_subcarriers, 1, num_channels)
X_magnitude = magnitude.T.reshape((-1, 56, 1, 1))
X_phase = phase.T.reshape((-1, 56, 1, 1))

# Stack magnitude and phase along the channel axis (num_samples, num_subcarriers, 1, num_channels)
X = np.concatenate((X_magnitude, X_phase), axis=3)
y = combined_labels
```

## **Split the data into training and testing sets**
We can also split the training and teasting sets to do the validation. Say, we take 20% of the data as the validation set.
```Python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

So now all the preparation work are done and we can construct the CNN model and train it.

*Updated Semester 2 Week6*