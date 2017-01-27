import time
import math
import signal

import smbus
import is31fl3731

i2c = smbus.SMBus(1)
display = is31fl3731.ScrollPhatHD(i2c)

speed_factor = 4

def display_check(starting_offset=0, brightness=64):
    offset = starting_offset
    for x in range(display.width):
        for y in range(display.height):
            offset += 1
            color = brightness * (offset % 2)
            display.pixel(x, y, color=color, frame=starting_offset)

display_check(0)
display_check(1)

display.autoplay(delay=64, loops=0, frames=2)

signal.pause()

try:
    while True:
        display.frame(0)
        time.sleep(1)
        display.frame(1)
        time.sleep(1)
except KeyboardInterrupt:
    pass
