#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import font5x5

print("""
Scroll pHAT HD: Portrait Clock

Displays hours, minutes and seconds in text.

Press Ctrl+C to exit!

""")

scrollphathd.set_brightness(0.3)
scrollphathd.rotate(270)

while True:
    scrollphathd.clear()

    # See https://docs.python.org/2/library/time.html
    # for more information on what the time formats below do.

    # Display the hour as two digits
    scrollphathd.write_string(
        time.strftime("%H"),
        x=0,
        y=0,
        font=font5x5)

    # Display the minute as two digits
    scrollphathd.write_string(
        time.strftime("%M"),
        x=0,
        y=6,
        font=font5x5)

    # Display the second as two digits
    scrollphathd.write_string(
        time.strftime("%S"),
        x=0,
        y=12,
        font=font5x5)

    scrollphathd.show()
    time.sleep(0.1)
