#!/usr/bin/env python

import sys
import time

import scrollphat


scrollphat.set_brightness(2)

if len(sys.argv) != 2:
    print("\nusage: python simple-text-scroll.py \"message\" \npress CTRL-C to exit\n")
    sys.exit(0)

scrollphat.write_string(sys.argv[1], 11)
length = scrollphat.buffer_len()

for i in range(length):
    try:
        scrollphat.scroll()
        time.sleep(0.1)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
