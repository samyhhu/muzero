#!/usr/bin/python3 

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

# Note: rewards 1.0 for every step that the environment doesn't end, and 
#       accumulates reward depending on how long it doesn't fail the current episode.

# Episode Termination
#   Pole Angle is more than ±12°
#   Cart Position is more than ±2.4 (center of the cart reaches the edge of the display)
#   Episode length is greater than 200
# Solved Requirements
#   Considered solved when the average reward is greater than or equal to 195.0 over 100 consecutive trials.

# while # of games < n games
# 1. play cartpole with existing mu model til game end
#    - use mcts search to search for optimal action
# 2. save game in replay buffer
# 3. train mu model based on n sampled game from replay buffer
