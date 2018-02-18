#!/usr/bin/env python

import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x7 as font5x7

# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
#scrollphathd.rotate(degrees=180)

for char in range(len(font5x7.data)):
    scrollphathd.draw_char(char * (3 + font5x7.width), 0, char, font=font5x7)

while True:
    scrollphathd.show()
    scrollphathd.scroll()
    time.sleep(0.1)
