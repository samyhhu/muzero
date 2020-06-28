from tictactoe import *

def test_board_full():
  board = [[-1] * 3 for _ in range(3)]
  assert check_full(board) == False

  board = [[0] * 3 for _ in range(3)]
  assert check_full(board) == True 
