#  Copyright (c) 2021. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
from collections import Counter


class Node:
    def __init__(self, feature=None, threshold=None, left=None, right=None, info_gain=None, value=None):
        self.feature = feature
        self.threshold = threshold
        self.left = left
        self.right = right
        self.info_gain = info_gain

        self.value = value


class DecisionTree:
    def __init__(self, min_samples_split=2, max_depth=100):
        self.min_samples_split = min_samples_split
        self.max_depth = max_depth

        self.root = None

    def fit(self, X, y):
        self.root = self._grow_tree(X, y)

    def _grow_tree(self, X, y, depth=0):
        n_samples, n_features = X.shape
        n_labels = len(np.unique(y))

        if (n_samples <= self.min_samples_split
                or depth >= self.max_depth
                or n_labels == 1):
            leaf_value = self._calculate_leaf_value(y)
            return Node(value=leaf_value)

        split_feature, split_threshold, info_gain = self._calculate_split_values(X, y, n_features)

        left_idxs, right_idxs = self._split(X[:, split_feature], split_threshold)

        left = self._grow_tree(X[left_idxs, :], y[left_idxs], depth + 1)
        right = self._grow_tree(X[right_idxs, :], y[right_idxs], depth + 1)

        return Node(split_feature, split_threshold, left, right, info_gain)

    def _calculate_split_values(self, X, y, n_features):
        best_feature, best_threshold = None, None
        best_gain = -float('inf')
        for feature_idx in range(n_features):
            feature_values = X[:, feature_idx]
            thresholds = np.unique(feature_values)
            for threshold in thresholds:
                info_gain = self._calculate_info_gain(y, feature_values, threshold)

                if info_gain > best_gain:
                    best_gain = info_gain
                    best_threshold = threshold
                    best_feature = feature_idx
        return best_feature, best_threshold, best_gain

    def _calculate_info_gain(self, y, feature_values, threshold):
        parent_entropy = self._entropy(y)

        left_idxs, right_idxs = self._split(feature_values, threshold)

        if len(left_idxs) == 0 or len(right_idxs) == 0:
            return 0

        n = len(y)
        n_l, n_r = len(left_idxs), len(right_idxs)
        e_l, e_r = self._entropy(y[left_idxs]), self._entropy(y[right_idxs])

        children_entropy = (n_l / n) * e_l + (n_r / n) * e_r

        info_gain = parent_entropy - children_entropy
        return info_gain

    @staticmethod
    def _split(feature_values, threshold):
        left_idxs = np.argwhere(feature_values <= threshold).flatten()
        right_idxs = np.argwhere(feature_values > threshold).flatten()
        return left_idxs, right_idxs

    @staticmethod
    def _entropy(y):
        class_labels = np.unique(y)
        entropy = 0
        for cls in class_labels:
            p_cls = len(y[y == cls]) / len(y)
            entropy += -p_cls * np.log2(p_cls)
        return entropy

    @staticmethod
    def _calculate_leaf_value(y):
        counter = Counter(y)
        most_common = counter.most_common(1)[0][0]
        return most_common

    def predict(self, X):
        return [self._traverse_tree(x, self.root) for x in X]

    def _traverse_tree(self, x, node):
        if node.value is not None:
            return node.value

        if x[node.feature] <= node.threshold:
            return self._traverse_tree(x, node.left)
        return self._traverse_tree(x, node.right)
