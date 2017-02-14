#!/usr/bin/env python

import time
import random

import scrollphathd

scrollphathd.rotate(180)

values = []

while True:
    values.insert(0,random.randrange(0,50))
    if len(values) > 17:
        values.pop(-1)

    scrollphathd.set_graph(values, low=0, high=50, brightness=0.1)
    scrollphathd.show()
    time.sleep(0.05)

