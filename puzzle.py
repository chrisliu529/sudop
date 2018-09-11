import sys

def _load_puzzle(filename):
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

def fill(x, y, n):
    def set_n(tiles):
        tiles[(x, y)] = n
    return set_n

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

class Puzzle:
    def __init__(self, filename):
        self.tiles = _load_puzzle(filename)

    def solve(self):
        def finished(tiles):
            return len(tiles.keys()) == 81 and \
                all([lambda x: isinstance(x, int) for x in tiles.values()])

        while not finished(self.tiles):
            action = analyze(self.tiles)
            action(self.tiles)
        write = sys.stdout.write
        for y in range(9):
            for x in range(9):
                write(str(self.tiles[(x, y)]))
            write('\n')
