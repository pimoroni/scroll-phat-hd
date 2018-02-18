#!/usr/bin/env python

import time
import signal

import scrollphathd

print("""
Scroll pHAT HD: Hello World

Scrolls "Hello World" across the screen
using the default 5x7 pixel large font.

Press Ctrl+C to exit!

""")

# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
#scrollphathd.rotate(degrees=180)

#Set a more eye-friendly default brightness
scrollphathd.set_brightness(0.5)

scrollphathd.write_string(" Hello World!")

while True:
    scrollphathd.show()
    scrollphathd.scroll()
    time.sleep(0.05)

