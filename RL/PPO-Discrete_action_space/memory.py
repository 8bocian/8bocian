#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np


class PPOMemory:
    def __init__(self, batch_size=64):
        self.states_memory = []
        self.actions_memory = []
        self.rewards_memory = []
        self.values_memory = []
        self.probabilities_memory = []
        self.dones_memory = []
        self.batch_size = batch_size

    def store_memory(self, states, actions, rewards, values, probabilities, dones):
        self.states_memory.append(states)
        self.actions_memory.append(actions)
        self.rewards_memory.append(rewards)
        self.values_memory.append(values)
        self.probabilities_memory.append(probabilities)
        self.dones_memory.append(dones)

    def clear_memory(self):
        self.states_memory = []
        self.actions_memory = []
        self.rewards_memory = []
        self.values_memory = []
        self.probabilities_memory = []
        self.dones_memory = []

    def return_batches(self):
        idxs = np.arange(0, len(self.states_memory))
        np.random.shuffle(idxs)
        idxs = idxs[:self.batch_size * (idxs.shape[0]//self.batch_size)]
        batches = idxs.reshape(idxs.shape[0]//self.batch_size, self.batch_size)

        return np.array(self.states_memory), \
            np.array(self.actions_memory), \
            np.array(self.rewards_memory), \
            np.array(self.values_memory), \
            np.array(self.probabilities_memory), \
            np.array(self.dones_memory), \
            batches
