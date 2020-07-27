#!/usr/bin/python3
'''
MCTS
'''
from copy import deepcopy
import random
from tictactoe import *

class State:
  '''
  state of each node
  '''
  def __init__(self, board=None, player=None):
    self.visit = 0
    self.win = 0
    self.loss = 0
    self.draw = 0
    self.board = board
    self.player = player

  def __str__(self):
    return f"p: {self.player} w: {self.win} l: {self.loss} d: {self.draw}\n {self.board}"

  @staticmethod
  def get_opponent(player):
    return (player + 1) % 2

  def get_nextstates(self):
    nextstates = []
    next_player = State.get_opponent(self.player)
    for i in range(0, 3):
      for j in range(0, 3):
        if self.board[i][j] < 0: # spot open
          next_board = deepcopy(self.board)
          next_board[i][j] = next_player
          nextstate = State(next_board, next_player)
          nextstates.append(nextstate)
    return nextstates

  def update_playout(self, playout):
    if playout == self.player:
      self.win += 1
    elif playout == State.get_opponent(self.player):
      self.loss += 1
    else:
      self.draw += 1

  def random_play(self):
    self.player = State.get_opponent(self.player)
    poss_moves = check_open(self.board)
    move = random.choice(poss_moves)
    self.board[move[0]][move[1]] = self.player

class Node:
  def __new__(cls, board, player, parent=None):
    self = super().__new__(cls)
    self.parent = parent 
    self.state = State(board, player)
    self.child = set() # TODO make this a set with custom hash of node
    return self
  
  def __getnewargs__(self):
    return (self.state.board, self.state.player,)
 
  def __eq__(self, other):
    return self.state.board == other.state.board
  
  def __hash__(self):
    return hash(str(self.state.board))
  
  def next_best_move(self):
    child_tuple = tuple(self.child)
    win_list = [n.state.win/n.state.loss for n in child_tuple]
    win_list_idx = win_list.index(max(win_list))
    return child_tuple[win_list_idx]

  def upper_conf_bound(self): # ucb
    return 0. 

class Tree:
  def __init__(self, board, player):
    self.root = Node(board, State.get_opponent(player))
    self.num_iter = 1000

  def find_next_move(self):
    n = 0
    while n < self.num_iter:
      # select promising nodes from root
      node = self.select()
      if not game_finished(node.state.board):
        # game is not done, expand
        self.expand(node)
      # pick node to explore, and simulate
      explore_node = node
      if len(node.child) > 0:
        explore_node = random.choice(tuple(node.child))

      # playout, -1 draw, 0 or 1
      playout = self.simulate(explore_node)
      # print(f"winner is {playout}")
      # backpropagate, to update result
      self.backpropagate(explore_node, playout)
      n += 1
    _ = [print(n.state) for n in self.root.child]
    self.root = self.root.next_best_move()
    return self.root.state

  '''
  select: choose highest value according to UCT
    uct = wi/ni + c*sqrt(ln(Ni) / ni)
    wi numer of wins for the node after ith move
    ni number of simuations for the node after ith move
    Ni: total number of simuation after ith move
    c: exploration parameter
  '''
  def select(self):
    if len(self.root.child) == 0:
      return self.root
    # find the childen of the root with the highest uct
    # uct_list = [n.upper_conf_bound() for n in self.root.child]
    # max_uct_idx = uct_list.index(max(uct_list))
    return random.choice(tuple(self.root.child))

  '''
  expand: given a node, expand to populate child nodes
  '''
  def expand(self, node):
    nextstates = node.state.get_nextstates()
    for s in nextstates: 
      new_node = Node(s.board, s.player, node)
      if new_node not in node.child:
        node.child.add(new_node)

  '''
  simulate: given a node, simulate til the game ends 
  '''
  def simulate(self, node):
    temp_node = deepcopy(node)
    while not game_finished(temp_node.state.board):
      temp_node.state.random_play()  # this should fill the board
      # print_board(temp_node.state.board)
      # print("")
    return check_winner(temp_node.state.board)

  '''
  backpropagate
  '''
  def backpropagate(self, node, playout):
    node.state.update_playout(playout)
    temp_node = node.parent
    while temp_node:
      temp_node.state.update_playout(playout)
      temp_node = temp_node.parent

if __name__ == '__main__':
  player = 0
  board = [[-1] * 3 for _ in range(3)]
  mcts = Tree(board, player)
  nextstate = mcts.find_next_move()
  print(f"next best move for player {nextstate.player}")
  print_board(nextstate.board)

  # nextstate = mcts.find_next_move()
  # print(f"next best move for player {nextstate.player}")
  # print_board(nextstate.board)
