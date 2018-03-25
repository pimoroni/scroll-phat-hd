#!/usr/bin/env python

import sys
import time

try:
    import psutil
except ImportError:
    sys.exit("This script requires the psutil module\nInstall with: sudo pip install psutil")

import scrollphat


i = 0
scrollphat.set_brightness(20)

cpu_values = [0] * 11

while True:
    try:
        cpu_values.pop(0)
        cpu_values.append(psutil.cpu_percent())

        scrollphat.graph(cpu_values, 0, 25)

        time.sleep(0.2)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
