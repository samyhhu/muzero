#!/usr/bin/python3 

import os
import sys
import gym
import pdb

env = gym.make('CartPole-v0')
print(env.action_space)
print(env.observation_space)

# env = gym.make('MsPacman-v0')
for i_episode in range(20):
  observation = env.reset()
  for t in range(100):
    env.render()
    print(observation)
    action = env.action_space.sample()

    # should not matter, what those observations are, but..
    # [position of cart, velocity of cart, angle of pole, rotation rate of pole]
    observation, reward, done, info = env.step(action)
    if done:
      print(f"episode finished after {t+1} timesteps")
      break
env.close()

