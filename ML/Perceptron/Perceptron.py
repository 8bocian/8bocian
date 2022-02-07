#  Copyright (c) 2021. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np

class Perceptron:

    def __init__(self, lr=0.01, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
        self.weights = None
        self.bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.weights = np.zeros(n_features)
        self.bias = 0

        y_ = np.array([1 if i > 0.5 else 0 for i in y])

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                y_pred = self.predict(x_i)

                update = self.lr * (y_[idx] - y_pred)
                self.weights += update * x_i
                self.bias += update

    def predict(self, X):
        linear_model = np.dot(X, self.weights) + self.bias
        y_pred =  self.activation_func(linear_model)
        return y_pred

    def activation_func(self, X):
        return np.where(X >= 0, 1, 0)
