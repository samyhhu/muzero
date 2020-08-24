#!/usr/bin/python3 

import gym
import pdb
import numpy as np

env = gym.make('CartPole-v0')
print(env.action_space)
print(env.observation_space)

def softmax(x):
  e_x = np.exp(x - np.max(x))
  return e_x / e_x.sum()

def naive_search(m, o_0, debug=False, T=1):
  K,n = m.K, m.a_dim
  if (K,n) not in aspace:
    aspace[(K,n)] = get_action_space(K, n)
  aopts,aoptss = aspace[(K,n)]

  # concatenate the current state with every possible action
  o_0s = np.repeat(np.array(o_0)[None], len(aopts), axis=0)
  ret = m.mu.predict([o_0s]+aoptss)
  v_s = ret[-3]
  
  minimum = min(v_s)
  maximum = max(v_s)
  v_s = (v_s - minimum) / (maximum - minimum)
  
  # group the value with the action rollout that caused it
  v = [(v_s[i][0], aopts[i]) for i in range(len(v_s))]
  if debug:
    print(sorted(v, reverse=True))
  
  av = [0] * n
  for vk, ak in v:
    av[ak[0]] += vk

  av = np.array(av).astype(np.float64) / T
  policy = softmax(av)
  return policy

# class ReplayBuffer 

# act_dim = env.action_space.n
# obs_dim = env.observation_space.shape[0]
# state_dim = 20
n_games = 20
# muzero = MuZero(obs_dim, act_dim, state_dim)

rews = np.zeros(n_games)
for i_game in range(n_games):
	# while # of games < n games
	# 1. play cartpole with existing mu model til game end
	#    - use mcts search to search for optimal action
	# 2. save game in replay buffer
	# 3. train mu model based on n sampled game from replay buffer
  observation = env.reset()
  for t in range(100):
    env.render()
    print(observation)
    action = env.action_space.sample()
    # use muzero to search for action
    # use naive search
		# naive_search(muzero, obs) 

    # should not matter, what those observations are, but..
    # [position of cart, velocity of cart, angle of pole, rotation rate of pole]
    observation, reward, done, info = env.step(action)
    if done:
      rews[i_game] = t+1
      print(f"episode finished after {t+1} timesteps")
      break
  # save history in replay buffer
	# train on batch sampling n from replay buffer


print(f"avg reward: {np.sum(rews) / n_games}")
env.close()

# Note: rewards 1.0 for every step that the environment doesn't end, and 
#       accumulates reward depending on how long it doesn't fail the current episode.

# Episode Termination
#   Pole Angle is more than ±12°
#   Cart Position is more than ±2.4 (center of the cart reaches the edge of the display)
#   Episode length is greater than 200
# Solved Requirements
#   Considered solved when the average reward is greater than or equal to 195.0 over 100 consecutive trials.


