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

#Uncomment to rotate the text
#scrollphathd.rotate(180)

#Set a more eye-friendly default brightness
scrollphathd.set_brightness(0.1)

scrollphathd.write_string("Hello World! ", x=0, y=1, font=font3x5, brightness=0.5)

while True:
    scrollphathd.show()
    scrollphathd.scroll()
    time.sleep(0.05)

