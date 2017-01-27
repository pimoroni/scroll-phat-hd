import time

import smbus
import is31fl3731

i2c = smbus.SMBus(1)
display = is31fl3731.ScrollPhatHD(i2c)

display.pixel(8,4,64)

try:
    while True:
        for x in [0,90,180,270]:
            display.rotate(x)
            display.show()
            time.sleep(0.1)

except KeyboardInterrupt:
    display.fill(0)
    display.show()
