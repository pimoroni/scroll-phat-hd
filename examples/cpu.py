#!/usr/bin/env python

import sys
import time
import signal   # Used to turn off Scroll pHAT HD if auto started using systemd

# Required to define the clear on shutdown if auto started using systemd
def clearshut():
    sphd.clear()

# This part captures the relevant shutdown signal to turn off Scroll pHAT HD on shutdown
def handler(signum, frame):
    clearshut()
    exit(0)

signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

# Use psutil to check CPU usage
try:
    import psutil
except ImportError:
    sys.exit("This script requires the psutil module\nInstall with: sudo pip install psutil")

# Shortening the Scroll pHAT HD library
import scrollphathd as sphd

# Sets the display width correctly
i = 0
cpu_values = [0] * sphd.DISPLAY_WIDTH

# Rotates the graph - uncomment if displays upside down depending on which USB port your power your Pi Zero from
#sphd.rotate(180)

# The main code - get CPU stats using psutil and then displays usage via the graph function on Scroll pHAT HD
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
