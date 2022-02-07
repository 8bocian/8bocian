#  Copyright (c) 2021. Oskar "Bocian" Możdżeń
#  All rights reserved.

import seaborn as sn
import matplotlib.pyplot as plt
from DecisionTree import DecisionTree
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

digits = load_digits()
X, y = digits.data, digits.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=5214)

tree = DecisionTree(min_samples_split=2, max_depth=200)
tree.fit(X_train, y_train)
y_pred = tree.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
sn.heatmap(cm, annot=True)
plt.title(f'Accuracy of the model: {accuracy_score(y_test, y_pred)}')
plt.show()
