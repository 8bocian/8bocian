#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
import gym
from agent import Agent
import matplotlib.pyplot as plt


########################################################################
# parameters to tune
# description of hyper-parameters - https://arxiv.org/pdf/1707.06347.pdf
epsilon = 0.2
gamma = 0.99
gae_lambda = 0.95
batch_size = 5
n_learning_epochs = 4
learning_freq = 20
policy_learning_rate = 0.003
critic_learning_rate = 0.003
l1_policy_size = 256
l2_policy_size = 256
l1_critic_size = 256
l2_critic_size = 256
########################################################################

env = gym.make('CartPole-v0')
agent = Agent(epsilon=epsilon, gamma=gamma, gae_lambda=gae_lambda,
              batch_size=batch_size, n_actions=env.action_space.n, n_learning_epochs=n_learning_epochs,
              l1_policy_size=l1_policy_size, l2_policy_size=l2_policy_size,
              l1_critic_size=l1_critic_size, l2_critic_size=l2_critic_size)


n_episodes = 300
scores = []
mean_scores = []
high_scores = []
high_score = 0
t = 0

for i in range(n_episodes):
    score = 0
    observation = env.reset()
    done = False

    while not done:
        action, probs, value = agent.choose_action(observation)
        observation_, reward, done, info = env.step(action)
        agent.memory.store_memory(observation, action, reward, value, probs, done)
        env.render(mode="human")

        t += 1
        score += reward
        observation = observation_

        if t % learning_freq == 0:
            agent.learn()

    if score >= high_score:
        high_score = score

    high_scores.append(high_score)
    scores.append(score)
    mean_scores.append(np.mean(scores[-100:]))

    print(f"Episode: {i+1} Mean: {np.mean(scores[-100:]):.3f} Score: {score}")

plt.plot(scores, color='b')
plt.plot(high_scores, color='r')
plt.plot(mean_scores, color='g')
plt.show()
