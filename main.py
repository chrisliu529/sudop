#!/usr/bin/env python3

import sys

def load_puzzle(filename):
    tiles = {}
    with open(filename) as f:
        lines = f.read().split('\n')
        y = 0
        for line in lines:
            x = 0
            for char in line:
                try:
                    tiles[(x, y)] = int(char)
                except:
                    pass
                x += 1
            y += 1
    return tiles

def finished(tiles):
    return len(tiles.keys()) == 81 and all([lambda x: isinstance(x, int) for x in tiles.values()])
    
def fill(x, y, n):
    def _fill(tiles):
        tiles[(x, y)] = n
    return _fill

def analyze(tiles):
    def rule_out(x, y):
        s = set(range(1, 10))
        for ix in range(9):
            v = tiles.get((ix, y), set())
            if isinstance(v, int):
                s -= set([v])
        for iy in range(9):
            v = tiles.get((x, iy), set())
            if isinstance(v, int):
                s -= set([v])
        x0 = x//3*3
        y0 = y//3*3
        for ix in range(x0, x0+3):
            for iy in range(y0, y0+3):
                v = tiles.get((ix, iy), set())
                if isinstance(v, int):
                    s -= set([v])
        return s

    for x in range(9):
        for y in range(9):
            v = tiles.get((x, y), set())
            if isinstance(v, int):
                continue
            v = rule_out(x, y)
            if len(v) == 1:
                return fill(x, y, v.pop())

def solve(tiles):
    while not finished(tiles):
        action = analyze(tiles)
        action(tiles)
    return tiles

tiles = solve(load_puzzle(sys.argv[1]))
for y in range(9):
    for x in range(9):
        sys.stdout.write(str(tiles[(x, y)]))
    sys.stdout.write('\n')
