#!/usr/bin/env python

import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x7 as font5x7

scrollphathd.rotate(180)

for char in range(len(font5x7.data)):
    scrollphathd.draw_char(char * (3 + font5x7.width), 0, char, font=font5x7)

while True:
    scrollphathd.show()
    scrollphathd.scroll(-1,0)
    time.sleep(0.01)

