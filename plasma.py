import time
import math

import smbus
import is31fl3731

i2c = smbus.SMBus(1)
display = is31fl3731.ScrollPhatHD(i2c)

speed_factor = 10

i = 0
while True:
    i += 2
    s = math.sin(i / 50.0) * 2.0 + 6.0
    print(s)
    for x in range(0, 17):
        for y in range(0, 7):
            v = 128.0 + (128.0 * math.sin((x * s) + i / 4.0) * math.cos((y * s) + i / 4.0))

            display.pixel(x, y, v)

    time.sleep(0.01)
    display.show()
