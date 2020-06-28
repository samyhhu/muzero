AlphaGo/MuZero Notes
--------------------
- Deep Neural Net f_theta with parameter theta 
  - input: 
    - board representation s and history
  - output: - (p,v)
    - p is vector of probability of selecting each move a
    - v scalar value of probability that player winning at position s
  - f_theta = (p, b)
- MCTS
  - each position s, MCTS algo is executed guided by neural net f_theta
  - uses as policy improvement operator
  - ouput: probability pi of playing each move

[AlphaGoZero Paper](https://deepmind.com/research/publications/mastering-game-go-without-human-knowledge)
[MuZero Paper](https://arxiv.org/pdf/1911.08265.pdf)

MCTS Notes
-----------
- should converge to minimax solution
- Principle of Operation 
  - selection: start from root R, select until leaf node L is reached, can biase child leafs to more promissing moves 
  - expansion: expand unless L ends the game, create one or more nodes choose node C from one of them
  - simulation: complete random playout of node C, choose uniform random moves until game ends
  - backpropagation: use result of playout to update information of the node and Path from C to R

TODO
----
- [x] implement mcts with tictactoe
- [ ] use gym and outline muzero framework
