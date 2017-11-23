#!/usr/bin/env python

import math
import sys
import time

import scrollphat


def millis():
    return int(round(time.time() * 1000))

scrollphat.set_brightness(2)

def clear(pause):
    for y in range(5):
        for x in range(11):
            scrollphat.set_pixel(x,y,0)
            scrollphat.update()
            time.sleep(pause)

def paint(pause):
    for y in range(5):
        for x in range(11):
            scrollphat.set_pixel(x,y,1)
            scrollphat.update()
            time.sleep(pause)

while(True):
    try:
        pause_time = 0.06
        paint(pause_time)
        clear(pause_time)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
