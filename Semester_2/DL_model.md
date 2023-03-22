# **Deep Learning Model**
## **CNN**
The most basic DL model is CNN, the architecture pf the model is based on the reading done at semester, details can be seen in 'Deep_Learning_Method.md'.

```Python
# CNN architecture
model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 1), activation='relu', input_shape=(56, 1, 2)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(Conv2D(filters=64, kernel_size=(3, 1), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(5, activation='softmax'))  # 5 classes

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
```
The overall accuracy can be shown using this.
```Python
# Evaluate the model
_, accuracy = model.evaluate(X_test, y_test)
print(f"Test accuracy: {accuracy * 100:.2f}%")
```

The accuracy can be up to 94%.

*Updated in Semester 2 Week 5-6*

## **RNN**
CNN
+ mainly used for tasks related to image and video processing
+ designed to automatically detect and extract features from the input data by convolving the input with a set of filters (kernels)
+ allows the network to identify patterns in the data, regardless of their location within the input
+ can handle input data of different sizes and shapes and can learn hierarchical representations of the data by stacking multiple convolutional layers

RNN
+ used for tasks related to sequential data, such as time-series analysis, speech recognition, and natural language processing. 
+ use a recurrent connection to pass information from one step to the next, allowing the network to maintain an internal memory of the previous inputs
+ enables RNNs to model the temporal dependencies in the data and capture long-term patterns

In the CSI classification, where the goal is to classify the channel quality based on the CSI data collected over time, **RNNs may be more suitable**. 
+ RNNs are specifically designed to model sequential data and can capture the temporal dependencies between consecutive CSI samples
+ it may be possible to extract more meaningful information from the CSI data and improve the classification accuracy

After comparing the difference bewteen CNN and RNN, and been through the negative results during interence stage, I found that RNN may be more useful for classify CSI.

So below is the updated architecture for RNN model applying LSTM(Long Short-Term Memory).
```Python
# RNN model
model = Sequential()
model.add(LSTM(units=32, return_sequences=True, input_shape=(56, 2)))
model.add(LSTM(units=64))
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(5, activation='softmax'))  # 5 classes

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)
```

This model takes more time and epoches to train. In this case, I have used 50 epoches and the accuracy has reached nearly 90%.

## **CRNNs**
There is also a model combined with CNN and RNN called CRNNs.
```Python
# Create a CRNN model
model = Sequential()
model.add(Conv2D(filters=32, kernel_size=(3, 1), activation='relu', input_shape=(56, 1, 2)))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(Conv2D(filters=64, kernel_size=(3, 1), activation='relu'))
model.add(BatchNormalization())
model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(TimeDistributed(Flatten()))
model.add(LSTM(128, activation='tanh', return_sequences=False))
model.add(Dropout(0.5))
model.add(Dense(5, activation='softmax'))  # 5 classes

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)
```
The performance of this model is similar to CNN model, so does the time and epoch it takes to train. So I did not go deep in this model.

*Updated in Semester 2 Week 8 20 March*

## **Some other classification methods (Supervised Learning)**
To use those method, the shape of the input CSI should be modified.
```Python
# Flatten the data for Random Forest
X_magnitude_flat = magnitude.T
X_phase_flat = phase.T

# Stack magnitude and phase
X_flat = np.hstack((X_magnitude_flat, X_phase_flat))
y = combined_labels
```

### **KNN**
```Python
# Create a KNN model
knn = KNeighborsClassifier(n_neighbors=5)

# Train the model
knn.fit(X_train, y_train)
```
This reaches accuracy of 72.47%
### **Random Forest**
```Python
# Create a Random Forest model
rf = RandomForestClassifier(n_estimators=100, random_state=42)

# Train the model
rf.fit(X_train, y_train)
```
This reached accuracy of 88.2%. 

The aboved 2 methods are just used as comparision with DL models, and it shows that DL methods will gain higher accuracy.

*Updated in Semester 2 Week8 21 March*