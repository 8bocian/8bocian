#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import tensorflow as tf
import numpy as np
from network import PolicyNetwork, CriticNetwork
from tensorflow.keras.optimizers import Adam
import tensorflow.keras as keras
from memory import PPOMemory
import tensorflow_probability as tfp

#########################################################################################################
# all implementation details are explained in this paper about PPO - https://arxiv.org/pdf/1707.06347.pdf
#########################################################################################################


class Agent:
    def __init__(self, epsilon=0.2, gamma=0.99, gae_lambda=0.95,
                 batch_size=64, n_actions=4, n_learning_epochs=10,
                 policy_learning_rate=0.0003, critic_learning_rate=0.0003,
                 l1_policy_size=256, l2_policy_size=256,
                 l1_critic_size=256, l2_critic_size=256):
        self.epsilon = epsilon
        self.gamma = gamma
        self.gae_lambda = gae_lambda
        self.batch_size = batch_size
        self.n_actions = n_actions
        self.n_learning_epochs = n_learning_epochs
        self.alpha_policy = policy_learning_rate
        self.alpha_critic = critic_learning_rate

        self.policy = PolicyNetwork(n_actions, l1_policy_size, l2_policy_size)
        self.critic = CriticNetwork(l1_critic_size, l2_critic_size)
        self.policy.compile(optimizer=Adam(learning_rate=policy_learning_rate))
        self.critic.compile(optimizer=Adam(learning_rate=critic_learning_rate))
        self.memory = PPOMemory(batch_size)

    def choose_action(self, observation):
        state = tf.convert_to_tensor([observation])
        probabilities = self.policy(state)

        distribution = tfp.distributions.Categorical(probabilities)
        action = distribution.sample()
        log_probabilities = distribution.log_prob(action)

        value = self.critic(state)

        action = np.array(action)[0]
        log_probabilities = np.array(log_probabilities)[0]
        value = np.array(value)[0]

        return action, log_probabilities, value

    def learn(self):
        for _ in range(self.n_learning_epochs):
            states, actions, rewards, values, old_probabilities, dones, batches = self.memory.return_batches()

            advantages = np.zeros(len(rewards))
            for t in range(len(rewards) - 1):
                for k in range(t, len(rewards) - 1):
                    delta = rewards[k] + (self.gamma * values[k + 1] * (1 - int(dones[k]))) - values[k]
                    advantages[t] += delta * ((self.gamma * self.gae_lambda) ** (k - t))

            for batch in batches:
                with tf.GradientTape(persistent=True) as tape:
                    states_batch, actions_batch, old_log_probabilities_batch = tf.convert_to_tensor(states[batch]), \
                                                                           tf.convert_to_tensor(actions[batch]), \
                                                                           tf.convert_to_tensor(old_probabilities[batch])
                    rewards_batch, old_values_batch, advantages_batch = rewards[batch], values[batch], advantages[batch]

                    new_probabilities = self.policy(states_batch)
                    distribution = tfp.distributions.Categorical(new_probabilities)
                    new_log_probabilities = distribution.log_prob(actions_batch)

                    new_value = self.critic(states_batch)
                    new_value = tf.squeeze(new_value, 1)

                    log_probabilities_ratio = tf.math.exp(new_log_probabilities - old_log_probabilities_batch)
                    weighted_log_probabilities = advantages_batch * log_probabilities_ratio

                    clipped_probs = tf.clip_by_value(log_probabilities_ratio,
                                                     1 - self.epsilon,
                                                     1 + self.epsilon)
                    weighted_clipped_probabilities = clipped_probs * advantages_batch

                    policy_loss = -tf.math.minimum(weighted_log_probabilities,
                                                   weighted_clipped_probabilities)
                    policy_loss = tf.math.reduce_mean(policy_loss)

                    returns = advantages_batch + old_values_batch

                    critic_loss = keras.losses.MSE(new_value, returns)

                policy_gradient = tape.gradient(policy_loss, self.policy.trainable_variables)
                critic_gradient = tape.gradient(critic_loss, self.critic.trainable_variables)

                self.policy.optimizer.apply_gradients(zip(policy_gradient, self.policy.trainable_variables))
                self.critic.optimizer.apply_gradients(zip(critic_gradient, self.critic.trainable_variables))
        self.memory.clear_memory()
