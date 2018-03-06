#!/usr/bin/env python

import signal
import time

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

# Write the "Hello World!" string in the buffer and
#   set a more eye-friendly default brightness
scrollphathd.write_string(" Hello World!", y=1, font=font3x5, brightness=0.5)

# Auto scroll using a while + time mechanism (no thread)
while True:
    # Show the buffer
    scrollphathd.show()
    # Scroll the buffer content
    scrollphathd.scroll()
    # Wait for 0.1s
    time.sleep(0.1)
