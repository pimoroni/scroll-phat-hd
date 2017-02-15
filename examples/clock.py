#!/usr/bin/env python

import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x5

BRIGHTNESS = 0.5

scrollphathd.rotate(180)

while True:
    scrollphathd.clear()
    float_sec = (time.time() % 60) / 60.0
    bar_sec = float_sec * 17 * BRIGHTNESS

    for y in range(17):
        b = BRIGHTNESS if bar_sec >= BRIGHTNESS else bar_sec

        scrollphathd.set_pixel(y,6,b)

        bar_sec -= BRIGHTNESS

        if bar_sec < 0:
            bar_sec = 0

    str_time = time.strftime("%H:%M")
    scrollphathd.write_string(str_time, x=0, y=0, font=font5x5, brightness=0.5)
    scrollphathd.show()
    time.sleep(0.1)

