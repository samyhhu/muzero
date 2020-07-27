import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam 
from tensorflow.keras.layers import * 

def to_one_hot(x, n):
  ret = np.zeros(n)
  if x >= 0:
    ret[x] = 1.0
  return ret

def bstack(bb): # flatten ?
  ret = [[x] for x in bb[0]]
  for i in range(1, len(bb)):
    for j in range(len(bb[i])):
      ret[j].append(bb[i][j])
  return [np.array(x) for x in ret]

def reformat_batch(batch, act_dim):
  X,Y = [], []
  for o,a,outs in batch:
    x = [o] + [to_one_hot(x, act_dim) for x in a]
    y = []
    for ll in [list(x) for x in outs]:
      y += ll
    X.append(x)
    Y.append(y)
  X = bstack(X)
  Y = bstack(Y)
  Y = [Y[0]] + Y[2:]
  return X,Y

class MuZero():
  LAYER_COUNT = 4 # 4 layers nn
  LAYER_DIM = 128 # each layer has 128 neurons

  def __init__(self, obs_dim, act_dim, state_dim):
    self.obs_dim = obs_dim
    self.act_dim = act_dim
    self.state_dim = state_dim
    self.losses = []

    # 3 neuralnet needed for h, g, f
    # h: obs -> s
    x = o_0 = Input(obs_dim) # observation dim
    for i in range(self.LAYER_COUNT):
      x = Dense(self.LAYER_DIM, activation='elu')(x)
    s_0 = Dense(state_dim, name='s_0')(x)
    self.h = Model(o_0, s_0, name="h")

    # g: (s(k-1), a(k)) -> (r(k), s(k))
    s_km1 = Input(state_dim)
    a_k = Input(act_dim)
    x = Concatenate()([s_km1, a_k])
    for i in range(self.LAYER_COUNT):
      x = Dense(self.LAYER_DIM, activation='elu')(x)
    s_k = Dense(state_dim, name='s_k')(x)
    r_k = Dense(1, name='r_k')(x)
    self.g = Mode([s_km1, a_k],  [r_k, s_k], name='g')

    #f: s(k) -> (p(k), v(k))
    x = s_k = Input(state_dim)
    for i in range(self.LAYER_COUNT):
      x = Dense(self.LAYER_DIM, activation='elu')(x)
    v_k = Dense(1, name='v_k')(x)
    p_k = Dense(act_dim, name='p_k')(x)
    self.f = Model(s_k, [p_k, v_k], name='f')

    K = 5
    lr = 0.001
    self.make_mu(K, lr)
  
  def make_mu(self, K, lr):
    # prediction is made at time t at for 1...K steps 
    # condition on past observation and future action
    self.K = K
    o_0 = Input(self.obs_dim, name='o_0')
    s_km1 = self.h(o_0)

    a_all, mu_all, loss_all = [], [], []

    def softmax_ce_logits(y_true, y_pred):
      return tf.nn.softmax_cross_entropy_with_logits_v2(y_true, y_pred)

    p_km1, v_km1 = self.f([s_km1])
    mu_all += [v_km1, p_km1]
    loss_all += ["mse", softmax_ce_logits]

    for k in range(K):
      a_k = Input(self.act_dim, name="a_%d" % k)
      a_all.append(a_k)

      r_k, s_k = self.g([s_km1, a_k])
      p_k, v_k = self.f([s_k])
      mu_all += [v_k, r_k, p_k]
      loss_all += ["mse", "mse", softmax_ce_logits]
      s_km1 = s_k

    mu = Model([o_0] + a_all, mu_all)
    mu.compile(Adam(lr), loss_all)
    self.mu = mu

  def train(self, batch):
    X,Y = reformat_batch(batch, self.act_dim)
    l = self.mu.train_on_batch(X,Y)
    self.losses.append(l)
    return l

