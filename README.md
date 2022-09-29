# sudop

A very simple sudoku solver in Python3

## Search Strategy

### Direct Search

If any tile is found can be filled with only one number, fill it.

### Backtracking

If none is found, start backtracking from the tile with least possibilies.

## How to Run in Jupyter Notebook

Copy & Paste puzzle.py into a notebook cell then append the following code (modify the game definition to your own one to be solved, of course)

```
game = '''
53  7
6  195
 98    6
8   6   3
4  8 3  1
7   2   6
 6    28
   419  5
    8  79
'''
Puzzle(game).solve().format()
```
