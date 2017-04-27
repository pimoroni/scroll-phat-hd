#!/usr/bin/env python

import time
import scrollphathd

DELAY = 0.0001

try:
    while True:
       for x in range(255):
           scrollphathd.fill(x/255.0, 0, 0, 17, 7)
           scrollphathd.show()
           time.sleep(DELAY)
       for x in reversed(range(255)):
           scrollphathd.fill(x/255.0, 0, 0, 17, 7)
           scrollphathd.show()
           time.sleep(DELAY)

except KeyboardInterrupt:
    scrollphathd.fill(0)
    scrollphathd.show()
