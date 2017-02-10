#!/usr/bin/env python

import time
from PIL import Image

import scrollphathd

IMAGE_BRIGHTNESS = 0.5

img = Image.open("mouth.bmp")

def get_pixel(x, y):
    p = img.getpixel((x,y))

    if img.getpalette() is not None:
        r, g, b = img.getpalette()[p:p+3]
        p = max(r, g, b)

    return p / 255.0

try:
    for x in range(0, 17):
        for y in range(0, 7):
            brightness = get_pixel(x, y)
            scrollphathd.pixel(x, 6-y, brightness * IMAGE_BRIGHTNESS)

    while True:
        scrollphathd.show()
        time.sleep(0.03)
        scrollphathd.scroll(-1)

except KeyboardInterrupt:
    scrollphathd.clear()
    scrollphathd.show()
