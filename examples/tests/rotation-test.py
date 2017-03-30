#!/usr/bin/env python

import time

import scrollphathd

scrollphathd.set_pixel(0,0,1)
scrollphathd.set_pixel(1,1,1)

try:
    while True:
        for x in [0,90,180,270]:
            scrollphathd.rotate(x)
            scrollphathd.show()
            time.sleep(0.1)

except KeyboardInterrupt:
    scrollphathd.fill(0)
    scrollphathd.show()
