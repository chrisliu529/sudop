#!/usr/bin/env python3

import sys
from puzzle import Puzzle

p = Puzzle(sys.argv[1]).solve()
if p is None:
    print('bad game')
else:
    p.format()
