import sys
from collections import namedtuple

given = {}
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
                    given[(x, y)] = True
                except ValueError:
                    tiles[(x, y)] = 0
                x += 1
            for i in range(9):
                if (i, y) not in tiles:
                    tiles[(i, y)] = 0
            y += 1
            if y >= 9:
                break
    return tiles

def fill(x, y, n):
    def set_n(tiles):
        tiles[(x, y)] = n
    return set_n

def serialize(tiles):
    l = []
    for x in range(9):
        for y in range(9):
            l.append(tiles[(x, y)])
    return ''.join([str(x) for x in l])

visited = {}
def start_search(x, y, v):
    def backtrack(p):
        for n in v:
            p.tiles[(x, y)] = n
            text = serialize(p.tiles)
            if text in visited:
                continue
            p2 = Puzzle(p.tiles)
            p2.solve()
            visited[text] = True
            if p2.solutions:
                p.solutions.update(p2.solutions)
    return backtrack

def verify(tiles):
    def dup_found(l):
        return len(l) > len(set(l))

    for x in range(9):
        col = [i for i in [tiles[(x, y)] for y in range(9)] if i > 0]
        if dup_found(col):
            return False

        row = [i for i in [tiles[(y, x)] for y in range(9)] if i > 0]
        if dup_found(row):
            return False

    d = {}
    for x in range(9):
        for y in range(9):
            ix = x//3*3
            iy = y//3*3
            l = d.setdefault((ix, iy), [])
            n = tiles[(x, y)]
            if n > 0 and n in l:
                return False
    return True

Action = namedtuple('Action', 'name func')
def analyze(tiles):
    def rule_out(x, y):
        s = set(range(1, 10))
        for ix in range(9):
            v = tiles[(ix, y)]
            if v > 0:
                s -= set([v])
        for iy in range(9):
            v = tiles[(x, iy)]
            if v > 0:
                s -= set([v])
        x0 = x//3*3
        y0 = y//3*3
        for ix in range(x0, x0+3):
            for iy in range(y0, y0+3):
                v = tiles[(ix, iy)]
                if v > 0:
                    s -= set([v])
        return s

    candidates = []
    for x in range(9):
        for y in range(9):
            if tiles[(x, y)] > 0:
                continue
            v = rule_out(x, y)
            if len(v) == 0:
                return Action(name='give_up', func=None)
            if len(v) == 1:
                return Action(name='fill', func=fill(x, y, v.pop()))
            candidates.append((x, y, v))

    def branches(c):
        return len(c[2])

    return Action(name='search', func=start_search(*min(candidates, key=branches)))

def format_tiles(tiles, write):
    for y in range(9):
        for x in range(9):
            v = str(tiles.get((x, y), '?'))
            if (x, y) in given:
                write(f'\033[91m{v}\033[00m')
            else:
                write(v)
        write('\n')

class Puzzle:
    def __init__(self, source):
        self.solutions = {}
        if isinstance(source, str):
            self.tiles = load_puzzle(source)
        else:
            self.tiles = dict(source)

    def finished(self):
        return all([x > 0 for x in self.tiles.values()])

    def solve(self):
        if not verify(self.tiles):
            return self

        while not self.finished():
            action = analyze(self.tiles)
            if action.name == 'give_up':
                return self
            elif action.name == 'search':
                action.func(self)
                return self
            else: # fill
                action.func(self.tiles)

        self.solutions[serialize(self.tiles)] = self.tiles
        return self

    def format(self):
        if not self.solutions:
            print('bad game')
        else:
            ns = len(self.solutions.keys())
            solutions = self.solutions.values()
            if ns > 1:
                print(f'false game, found {ns} solutions:')
                for s in solutions:
                    print('-'*9)
                    format_tiles(s, sys.stdout.write)
            else:
                format_tiles(list(solutions)[0], sys.stdout.write)
