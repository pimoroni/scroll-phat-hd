#!/usr/bin/env python

import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x5

print("""
Scroll pHAT HD: Clock

Displays hours, minutes and seconds in text.

Press Ctrl+C to exit!

""")

BRIGHTNESS = 0.5

scrollphathd.rotate(270)

while True:
    scrollphathd.clear()

    str_time = time.strftime("%H") 
    scrollphathd.write_string(str_time, x=0, y=0, font=font5x5, brightness=0.5)

    str_time = time.strftime("%M")
    scrollphathd.write_string(str_time, x=0, y=6, font=font5x5, brightness=0.5)

    str_time = time.strftime("%S")
    scrollphathd.write_string(str_time, x=0, y=12, font=font5x5, brightness=0.5)

    scrollphathd.show()
    time.sleep(0.1)

