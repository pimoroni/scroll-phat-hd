#!/usr/bin/env python

import scrollphathd

try:
    while True:
        for x in range(18):
            scrollphathd.fill(0.1,0,0,x,7)
            scrollphathd.show()
        for x in range(18):
            scrollphathd.fill(0,0,0,x,7)
            scrollphathd.show()
except KeyboardInterrupt:
    scrollphathd.fill(0)
    scrollphathd.show()
