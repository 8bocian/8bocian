#  Copyright (c) 2021. Oskar "Bocian" Możdżeń
#  All rights reserved.

import os
import numpy as np
from tensorflow import keras

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()

pt = X_test

X_train = X_train / 255
X_test = X_test / 255

X_train = X_train.reshape(len(X_train), 28 * 28)
X_test = X_test.reshape(len(X_test), 28 * 28)

optimizer = "Adam"
loss = "sparse_categorical_crossentropy"
metrics = ['accuracy']

model = keras.Sequential([
    keras.layers.Dense(100, activation='relu'),
    keras.layers.Dense(10, activation='sigmoid')

])
model.compile(optimizer=optimizer,
              loss=loss,
              metrics=metrics)
model.fit(X_train, y_train, epochs=5)

model.evaluate(X_test, y_test)

y_pred = model.predict(X_test)

predictions = [np.argmax(prediction) for prediction in y_pred]
accuracy = len(y_test[y_test == predictions]) / len(y_test)

print(f'Accuracy: {accuracy} Optimizer: {optimizer} Loss: {loss}')

