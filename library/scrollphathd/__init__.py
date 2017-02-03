import atexit

import smbus
from . import is31fl3731

__version__ = '0.0.1'

i2c = smbus.SMBus(1)
display = is31fl3731.ScrollPhatHD(i2c)

pixel = display.pixel
show = display.show
scroll = display.scroll
fill = display.fill
width = display.width
height = display.height
scroll_to = display.scroll_to
rotate = display.rotate
flip = display.flip
draw_char = display.draw_char

def clear():
    display.fill(0)
    display.show()

atexit.register(clear)
