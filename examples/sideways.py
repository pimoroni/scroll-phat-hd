#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import font5x7

print("""
Scroll pHAT HD: Hello World

Scrolls "Hello World" across the screen
in a 5x7 pixel large font.

Press Ctrl+C to exit!

""")

scrollphathd.rotate(degrees=90)

# Set a more eye-friendly default brightness
scrollphathd.set_brightness(0.5)

scrollphathd.write_string("Hello World! ", x=0, y=0, font=font5x7)
scrollphathd.write_string("How are you? ", x=0, y=8, font=font5x7)
scrollphathd.show()

time.sleep(0.5)

while True:
    scrollphathd.show()
    scrollphathd.scroll()
    time.sleep(0.05)

