# **Model Validation**
To validate the model, we can simply use 2 plots to show the result.

## **Model accuracy**
This will show the accuracy on both training sets and validation sets.
```Python
# First we need to store all the history, change the previous code to this
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# Below is the script to draw the accuracy plot
# Plot training and validation accuracy values
plt.plot(history.history['accuracy'])
plt.plot(history.history['val_accuracy'])
plt.title('Model accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(['Train', 'Validation'], loc='upper left')
plt.show()
```

## **Confusion matrix**
This is the best way to visualize the accuracy of classifiaction. 
```Python
# Make predictions on the test set
y_pred = np.argmax(model.predict(X_test), axis=1)

# Calculate the confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot the confusion matrix
fig, ax = plt.subplots(figsize=(8, 8))
cax = ax.matshow(cm, cmap=plt.cm.Blues)
fig.colorbar(cax)
ax.set_xticks(range(5))
ax.set_yticks(range(5))
ax.set_xticklabels(range(1, 6))
ax.set_yticklabels(range(1, 6))
ax.set_xlabel('Predicted')
ax.set_ylabel('True')

# Add the number of samples in each cell
for i in range(cm.shape[0]):
    for j in range(cm.shape[1]):
        ax.text(j, i, cm[i, j], ha='center', va='center', color='red')

plt.show()
```

*Updated in Semester 2 Week 6*