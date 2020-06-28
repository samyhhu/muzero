#!/usr/bin/python3 

# Tic Tac Toe using MCTS
def print_board(board):
  for row in board:
    print(row)

def check_full(board):
  for x in range(0,3):
    row = set([board[x][0],board[x][1],board[x][2]])
    if -1 in row:
      return False
  return True

def check_winner(board):
  for x in range(0,3):
    row = set([board[x][0],board[x][1],board[x][2]])
    if len(row) == 1 and board[x][0] != -1:
      return board[x][0]

  for x in range(0,3):
    col = set([board[0][x],board[1][x],board[2][x]])
    if len(col) == 1 and board[0][x] != -1:
      return board[0][x]

  diag1 = set([board[0][0],board[1][1],board[2][2]])
  diag2 = set([board[0][2],board[1][1],board[2][0]])
  if len(diag1) == 1 or len(diag2) == 1 and board[1][1] != -1:
    return board[1][1]
  return -1 

def check_open(board):
  open_spots = []
  for i in range(0,3):
    for j in range(0,3):
      if board[i][j] < 0:
        open_spots.append([i, j])  
  return open_spots

def game_finished(board):
  winner = check_winner(board)
  return winner == 0 or winner == 1 or check_full(board)

##################### GAME DRIVER ##############################
if __name__ == '__main__':
  player = 0
  board = [[-1] * 3 for _ in range(3)]
  while True:
    print_board(board)
    move = input(f"player {player}'s turn <row col>:")
    rc = move.split(' ')
    row, col = int(rc[0]), int(rc[1])
    if row < 0 or row > 2 or col < 0 or col > 2:
      print("invalid move, try again")
      continue
    board[row][col] = player
  
    winner = check_winner(board)
    if winner == 0 or winner == 1:
      print(f"Winner is player {winner}")
      print_board(board)
      break
    elif check_full(board):
      print(f"Game Draw")
      print_board(board)
      break
    player = (player + 1) % 2
