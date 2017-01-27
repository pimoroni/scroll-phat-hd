import time

import smbus
import is31fl3731

i2c = smbus.SMBus(1)
display = is31fl3731.ScrollPhatHD(i2c)


display.pixel(0,0,64)

try:
    while True:
        display.scroll(-1,-1)
        display.show()
        time.sleep(0.1)
except KeyboardInterrupt:
    display.fill(0)
    display.show()
