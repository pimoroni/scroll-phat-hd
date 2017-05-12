#!/usr/bin/env python

import signal

import scrollphathd
from scrollphathd.fonts import font3x5

scrollphathd.set_brightness(0.3)

scrollphathd.fill(1, 0, 0, 17, 7)

scrollphathd.write_string("Ahoy!", y=1, font=font3x5, brightness=0)

scrollphathd.show()

signal.pause()
