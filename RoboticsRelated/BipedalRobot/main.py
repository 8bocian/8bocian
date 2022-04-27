#  Copyright (c) 2022. Oskar "Bocian" Możdżeń
#  All rights reserved.

import numpy as np
import time
import pylab as p
from environment import WalkerEnv


env = WalkerEnv()
n_episodes = 20000
n_steps = 1000000

print(env.action_space)

for episode in range(n_episodes):
    score = []
    done = False

    for t in range(n_steps):
        # get random action
        action = env.action_space.sample()
        # pass action to step function to apply action
        obs, reward, done, info = env.step(action)
        score.append(reward)
        # time needs a small adjustment
        time.sleep(0.001)
        if done:
            break
    print(f"Episode: {episode}\nScore: {np.mean(score):.3f}")
    env.reset()
env.close()
