#!/usr/bin/env python

import time
import signal

import scrollphathd
from scrollphathd.fonts import font3x5

print("""
Scroll pHAT HD: Hello World

Scrolls "Hello World" across the screen
in a 3x5 pixel condensed font.

Press Ctrl+C to exit!

""")

# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
#scrollphathd.rotate(degrees=180)

# Set a more eye-friendly default brightness
scrollphathd.set_brightness(0.5)

# Write the string to scroll
scrollphathd.write_string(" Hello World! ", x=0, y=1, font=font3x5, brightness=1.0)

def draw_static_elements(buf):
    # Buf is given as a two dimensional array of elements buf[x][y]
    # This method will blink a frame of alternating lights around
    # our scrolling text twice a second.

    if int(time.time() * 2) % 2 == 0:
        for x in range(scrollphathd.DISPLAY_WIDTH):
            if x % 2 == 0:
                buf[x][0] = 1.0
                buf[x][scrollphathd.DISPLAY_HEIGHT - 1] = 1.0

        for y in range(scrollphathd.DISPLAY_HEIGHT):
            if y % 2 == 0:
                buf[0][y] = 1.0
                buf[scrollphathd.DISPLAY_WIDTH - 1][y] = 1.0

    return buf

try:
    while True:
        scrollphathd.show(before_display=draw_static_elements)
        scrollphathd.scroll()
        time.sleep(0.05)
except KeyboardInterrupt:
    pass

