import numpy as np

class LogisticRegression:
    def __init__(self, lr=0.001, n_iters=1000):
        self.lr = lr
        self.n_iters = n_iters
        self.Weights = None
        self.Bias = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.Weights = np.zeros(n_features)
        self.Bias = 0

        for _ in range(self.n_iters):
            linear_model = np.dot(X, self.Weights) + self.Bias
            y_pred = self._sigmoid(linear_model)

            dw = 1 / n_samples * np.dot(X.T, (y_pred - y))
            db = 1 / n_samples * np.sum(y_pred - y)

            self.Weights -= self.lr * dw
            self.Bias -= self.lr * db

    def predict(self, X):
        linear_model = np.dot(X, self.Weights) + self.Bias
        y_pred = self._sigmoid(linear_model)
        y_pred_cls = [1 if i > 0.5 else 0 for i in y_pred]
        return y_pred_cls

    def _sigmoid(self, x):
        return 1/(1+np.exp(-x))
