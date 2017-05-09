#!/usr/bin/env python

import time
from sys import exit

try:
    from PIL import Image
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

import scrollphathd


print("""
Scroll pHAT HD: Robot Mouth

Loads mouth.bmp and scrolls it across the screen.

Press Ctrl+C to exit!

""")

IMAGE_BRIGHTNESS = 0.5

img = Image.open("mouth.bmp")

def get_pixel(x, y):
    p = img.getpixel((x, y))

    if img.getpalette() is not None:
        r, g, b = img.getpalette()[p:p+3]
        p = max(r, g, b)

    return p / 255.0

try:
    for x in range(0, scrollphathd.DISPLAY_WIDTH):
        for y in range(0, scrollphathd.DISPLAY_HEIGHT):
            brightness = get_pixel(x, y)
            scrollphathd.pixel(x, 6-y, brightness * IMAGE_BRIGHTNESS)

    while True:
        scrollphathd.show()
        time.sleep(0.03)
        scrollphathd.scroll(-1)

except KeyboardInterrupt:
    scrollphathd.clear()
    scrollphathd.show()
