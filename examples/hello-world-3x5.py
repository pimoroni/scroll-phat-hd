#!/usr/bin/env python

import time
import signal

import scrollphathd
from scrollphathd.fonts import font3x5

print("""
Scroll pHAT HD: Hello World

Scrolls "Hello World" across the screen
in a 3x5 pixel condensed font.

Press Ctrl+C to exit!

""")

# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
#scrollphathd.rotate(degrees=180)

#Set a more eye-friendly default brightness
scrollphathd.set_brightness(0.5)

scrollphathd.write_string(" Hello World!", y=1, font=font3x5)

while True:
    scrollphathd.show()
    scrollphathd.scroll()
    time.sleep(0.05)

