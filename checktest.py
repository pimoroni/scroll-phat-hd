import time
import math

import smbus
import is31fl3731

i2c = smbus.SMBus(1)
display = is31fl3731.ScrollPhatHD(i2c)

speed_factor = 10

try:
    while True:
        scale = (math.sin(time.time() * speed_factor) + 1) / 2
        offset = 0
        for x in range(display.width):
            for y in range(display.height):
                offset += 1
                color = int(64 * scale) * (offset % 2)
                display.pixel(x, y, color)

        display.show()

except KeyboardInterrupt:
    display.fill(0)
