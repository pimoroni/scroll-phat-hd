#!/usr/bin/env python

import time

import scrollphathd

scrollphathd.pixel(8,4,1.0)

try:
    while True:
        for x in [0,90,180,270]:
            scrollphathd.rotate(x)
            scrollphathd.show()
            time.sleep(0.1)

except KeyboardInterrupt:
    scrollphathd.fill(0)
    scrollphathd.show()
