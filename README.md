# sudop

[ ![Codeship Status for chrisliu529/sudop](https://app.codeship.com/projects/3ebf0a60-97c0-0136-16d8-62fbbf92ef69/status?branch=master)](https://app.codeship.com/projects/305087)

A very simple sudoku solver in Python3

## Search Strategy

### Direct Search

If any tile is found can be filled with only one number, fill it.

### Backtracking

If none is found, start backtracking from the tile with least possibilies.

