# Checkers-AI-Agent

Checkers artificial intelligence agent written in Python using the minimax algorithm with alpha-beta pruning.

## Input

The program reads an input.txt file representing the current game state in the following format:

SINGLE 
WHITE 
100.0 
.b.b.b.b
b.b.b.b.
.b.b.b.b
........
........
w.w.w.w.
.w.w.w.w
w.w.w.w.

## Output

The program outputs an output.txt file with the next chosen move using the following notation:

E FROM_POS TO_POS - The agent moves a piece from location FROM_POS to an adjacent diagonal empty location TO_POS.
J FROM_POS TO_POS - The agent moves a piece from location FROM_POS to empty location TO_POS by jumping over a piece in between.
