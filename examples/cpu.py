#!/usr/bin/env python

import sys
import time

try:
    import psutil
except ImportError:
    sys.exit("This script requires the psutil module\nInstall with: sudo pip install psutil")

import scrollphathd as sphd

print("""
Scroll pHAT HD: CPU

Displays a graph with CPU values.

Press Ctrl+C to exit!

""")

i = 0

cpu_values = [0] * sphd.DISPLAY_WIDTH

sphd.rotate(180)

while True:
    try:
        cpu_values.pop(0)
        cpu_values.append(psutil.cpu_percent())

        sphd.set_graph(cpu_values, low=0, high=25, brightness=0.25)

        sphd.show()
        time.sleep(0.2)
    except KeyboardInterrupt:
        sphd.clear()
        sys.exit(-1)
