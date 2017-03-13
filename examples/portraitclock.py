#!/usr/bin/env python

import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x5

print("""
Scroll pHAT HD: Portrait Clock

Displays hours, minutes and seconds in text.

Press Ctrl+C to exit!

""")

scrollphathd.set_brightness(0.1)
scrollphathd.rotate(270)

while True:
    scrollphathd.clear()

    str_time = time.strftime("%H") 
    scrollphathd.write_string(str_time, x=0, y=0, font=font5x5)

    str_time = time.strftime("%M")
    scrollphathd.write_string(str_time, x=0, y=6, font=font5x5)

    str_time = time.strftime("%S")
    scrollphathd.write_string(str_time, x=0, y=12, font=font5x5)

    scrollphathd.show()
    time.sleep(0.1)

