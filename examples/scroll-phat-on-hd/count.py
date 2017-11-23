#!/usr/bin/env python

import sys
import time

import scrollphat


if(len(sys.argv) == 1):
    print("Type a number in under 999 as an argument.")
    sys.exit(-1)
val = int(sys.argv[1])

if(val > 999):
    print("Number must be under 999 to fit on screen")
    sys.exit(-1)

scrollphat.set_brightness(7)

for x in range(1, val+1):
    try:
        scrollphat.write_string(str(x))
        time.sleep(0.35)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
