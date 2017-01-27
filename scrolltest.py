import time
import math

import smbus
import is31fl3731

i2c = smbus.SMBus(1)
display = is31fl3731.ScrollPhatHD(i2c)

speed_factor = 4

try:
    while True:
        scale = (math.sin(time.time() * speed_factor) + 1) / 2
        display.fill(int(64 * scale))
except KeyboardInterrupt:
    display.fill(0)
