#!/usr/bin/env python3

import argparse
from puzzle import Puzzle

parser = argparse.ArgumentParser(description='A very simple soduku solver')
parser.add_argument("file", type=str, default=None, help="File to process.")
parser.add_argument("-d", "--details", default=None, action="store_true", help="Output steps in details")
args = parser.parse_args()

p = Puzzle(args.file)
p.output_details = args.details
p.solve().format()
