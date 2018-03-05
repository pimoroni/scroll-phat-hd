#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x7

print("""
Scroll pHAT HD: Hello utf-8

Scrolls the 256 characters Scroll pHAT supports across the screen.

Note: many otherwise useless control characters have been 
replaced with symbols you might find useful!

Press Ctrl+C to exit!

""")

#Uncomment to rotate the text
#scrollphathd.rotate(180)

#Set a more eye-friendly default brightness
scrollphathd.set_brightness(0.5)

text = [unichr(x) for x in range(256)]

text = u"{}        ".format(u"".join(text))

scrollphathd.write_string(text, x=0, y=0, font=font5x7, brightness=0.5)

while True:
    scrollphathd.show()
    scrollphathd.scroll()
    time.sleep(0.05)
