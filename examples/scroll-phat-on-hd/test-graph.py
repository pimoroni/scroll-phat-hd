#!/usr/bin/env python

import time

import scrollphat


scrollphat.set_brightness(64)

while True:
    print("0 to 5")
    scrollphat.graph([0,1,2,3,4,5])
    time.sleep(1.0)
    scrollphat.clear()
    print("0 to 10")
    scrollphat.graph([0,2,4,6,8,10])
    time.sleep(1.0)
    scrollphat.clear()
