#!/usr/bin/env python3

import argparse
from puzzle import Puzzle

P = argparse.ArgumentParser(description='A very simple soduku solver')
P.add_argument("file", type=str, default=None, help="File to process.")
P.add_argument("-d", "--details", default=None, action="store_true", help="Output steps in details")
A = P.parse_args()

Puzzle(A.file, A.details).solve().format()
