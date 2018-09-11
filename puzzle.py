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

def finished(tiles):
    return len(tiles.keys()) == 81 and \
        all([lambda x: isinstance(x, int) for x in tiles.values()])

def fill(x, y, n):
    def set_n(tiles):
        tiles[(x, y)] = n
        return tiles
    return set_n

def start_search(x, y, v):
    def backtrack(tiles):
        for n in v:
            tiles[(x, y)] = n
            nt = Puzzle(tiles).solve()
            if nt is None:
                continue
            return nt.tiles
    return backtrack

def verify(tiles):
    def dup_found(l):
        return len(l) > len(set(l))

    for x in range(9):
        col = [i for i in [tiles.get((x, y), 0) for y in range(9)] if i > 0]
        if dup_found(col):
            return False

        row = [i for i in [tiles.get((y, x), 0) for y in range(9)] if i > 0]
        if dup_found(row):
            return False

    d = {}
    for x in range(9):
        for y in range(9):
            ix = x//3*3
            iy = y//3*3
            l = d.setdefault((ix, iy), [])
            n = tiles.get((x, y), 0)
            if n > 0 and n in l:
                return False
    return True

def analyze(tiles):
    def rule_out(x, y):
        s = set(range(1, 10))
        for ix in range(9):
            v = tiles.get((ix, y), 0)
            if v > 0:
                s -= set([v])
        for iy in range(9):
            v = tiles.get((x, iy), 0)
            if v > 0:
                s -= set([v])
        x0 = x//3*3
        y0 = y//3*3
        for ix in range(x0, x0+3):
            for iy in range(y0, y0+3):
                v = tiles.get((ix, iy), 0)
                if v > 0:
                    s -= set([v])
        return s

    candidates = []
    for x in range(9):
        for y in range(9):
            v = tiles.get((x, y), set())
            if isinstance(v, int):
                continue
            v = rule_out(x, y)
            if len(v) == 0:
                return 'give_up'
            if len(v) == 1:
                return fill(x, y, v.pop())
            candidates.append((x, y, v))

    def branches(candidate):
        x, y, v = candidate
        return len(v)

    return start_search(*min(candidates, key=branches))

class Puzzle:
    def __init__(self, source):
        if isinstance(source, str):
            self.tiles = _load_puzzle(source)
        else:
            self.tiles = dict(source)

    def solve(self):
        if not verify(self.tiles):
            return None

        while not finished(self.tiles):
            action = analyze(self.tiles)
            if action == 'give_up':
                return None
            data = action(self.tiles)
            if data is None:
                return None
            self.tiles = data
        return self

    def format(self):
        write = sys.stdout.write
        for y in range(9):
            for x in range(9):
                write(str(self.tiles.get((x, y), '?')))
            write('\n')
