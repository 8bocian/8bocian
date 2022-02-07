#  Copyright (c) 2021. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
from main import NaiveBayes
from sklearn.model_selection import train_test_split
from sklearn.datasets import make_classification


def accuracy(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)


X, y = make_classification(n_samples=1000, n_features=10, n_classes=2, random_state=123)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

nb = NaiveBayes()
nb.fit(X_train, y_train)
y_pred = nb.predict(X_test)

print(f"Naive Bayes classification accuracy {accuracy(y_test, y_pred)}")
