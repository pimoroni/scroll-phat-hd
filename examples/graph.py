#!/usr/bin/env python

import time
import random

import scrollphathd

print("""
Scroll pHAT HD: Graph

Displays a graph with random values.

Press Ctrl+C to exit!

""")



scrollphathd.rotate(180)

values = []
for i in range(17):
    values.append(0)

while True:
    values.insert(0,random.randrange(0,50))
    if len(values) > 17:
        values.pop(-1)

    scrollphathd.set_graph(values, low=0, high=50, brightness=0.5)
    scrollphathd.show()
    time.sleep(0.05)
