#  Copyright (c) 2021. Oskar "Bocian" Możdżeń
#  All rights reserved.

import seaborn as sn
import matplotlib.pyplot as plt
from RandomForest import RandomForest
from sklearn.datasets import load_digits
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split

data = load_digits()
X, y = data.data, data.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1234)

forest = RandomForest(n_trees=100)
forest.fit(X_train, y_train)
y_pred = forest.predict(X_test)

cm = confusion_matrix(y_test, y_pred)
sn.heatmap(cm, annot=True)
plt.title(f'{accuracy_score(y_test, y_pred)}')
plt.show()
