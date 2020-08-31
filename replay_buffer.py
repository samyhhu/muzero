class Game:
  def __init__(self, env):
    self.env = env
    self.observations = []
    self.history = []
    self.rewards = []
    self.policies = []
    self.done = False
    self.observation = env.reset()
    self.total_reward = 0

  def apply(self, action):
    self.env.step(action)
    pass

class ReplayBuffer:
  def __init__(self):
    self._games = []
    pass

  def save_game(self, game):
    pass

  def sample_game(self, game);
    pass
