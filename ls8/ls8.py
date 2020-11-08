#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *

if len(sys.argv) < 2:
  print('Enter the name of the file you wish to load')
  sys.exit()

cpu = CPU()

cpu.load(sys.argv[1])
cpu.run()