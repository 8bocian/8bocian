#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import tensorflow.keras as keras
from tensorflow.keras.layers import Dense


class PolicyNetwork(keras.Model):
    def __init__(self, n_actions, l1_size=256, l2_size=256):
        super(PolicyNetwork, self).__init__()
        self.l1 = Dense(l1_size, activation='relu')
        self.l2 = Dense(l2_size, activation='relu')
        self.l3 = Dense(n_actions, activation='softmax')

    def call(self, state):
        x = self.l1(state)
        x = self.l2(x)
        x = self.l3(x)

        return x


class CriticNetwork(keras.Model):
    def __init__(self, l1_size=256, l2_size=256):
        super(CriticNetwork, self).__init__()
        self.l1 = Dense(l1_size, activation='relu')
        self.l2 = Dense(l2_size, activation='relu')
        self.l3 = Dense(1, activation=None)

    def call(self, state):
        x = self.l1(state)
        x = self.l2(x)
        x = self.l3(x)

        return x
