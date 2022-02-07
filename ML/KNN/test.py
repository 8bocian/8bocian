#  Copyright (c) 2021. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
import matplotlib.pyplot as plt
from main import KNN
from matplotlib.colors import ListedColormap
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

cmap = ListedColormap(['#FF0000', '#00FF00', '#0000FF'])

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

plt.figure()
plt.scatter(X[:, 2], X[:, 3], c=y, cmap=cmap, edgecolors='k', s=20)
plt.show()

knn = KNN(k=int(np.floor(np.sqrt(len(X_train)))))
knn.fit(X_train, y_train)
y_pred = knn.predict(X_test)
print(np.sum(y_pred == y_test)/len(y_test))
