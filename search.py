import numpy as np

def softmax(x):
  e_x = np.exp(x - np.max(x))
  return e_x / e_x.sum()

def get_action_space(K, n):
  def to_one_hot(x,n):
    ret = np.zeros([n])
    ret[x] = 1.0
    return ret
  import itertools
  aopts = list(itertools.product(list(range(n)), repeat=K))
  aoptss = np.array([[to_one_hot(x, n) for x in aa] for aa in aopts])
  aoptss = aoptss.swapaxes(0,1)
  aoptss = [aoptss[x] for x in range(K)]
  return aopts,aoptss

aspace = {}
def naive_search(m, o_0, debug=False, T=1):
  K,n = m.K, m.act_dim
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
