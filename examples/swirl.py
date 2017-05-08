#!/usr/bin/env python

import time
import math

import scrollphathd

print("""
Scroll pHAT HD: Swirl

Displays a basic demo-scene style pattern.

Press Ctrl+C to exit!

""")

def swirl(x, y, step):
    x -= (scrollphathd.DISPLAY_WIDTH/2.0)
    y -= (scrollphathd.DISPLAY_HEIGHT/2.0)

    dist = math.sqrt(pow(x, 2) + pow(y, 2))

    angle = (step / 10.0) + dist / 1.5

    s = math.sin(angle)
    c = math.cos(angle)

    xs = x * c - y * s
    ys = x * s + y * c

    r = abs(xs + ys)

    return max(0.0, 0.7 - min(1.0, r/8.0))

scrollphathd.set_brightness(0.8)

while True:
    timestep = math.sin(time.time() / 18) * 1500

    for x in range(0, scrollphathd.DISPLAY_WIDTH):
        for y in range(0, scrollphathd.DISPLAY_HEIGHT):
            v = swirl(x, y, timestep)
            scrollphathd.pixel(x, y, v)

    time.sleep(0.001)
    scrollphathd.show()
