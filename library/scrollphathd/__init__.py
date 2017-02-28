import atexit
from sys import exit

try:
    import smbus
except ImportError:
    if version_info[0] < 3:
        exit("This library requires python-smbus\nInstall with: sudo apt-get install python-smbus")
    elif version_info[0] == 3:
        exit("This library requires python3-smbus\nInstall with: sudo apt-get install python3-smbus")

from . import is31fl3731

__version__ = '0.0.1'

i2c = smbus.SMBus(1)
display = is31fl3731.ScrollPhatHD(i2c)

DISPLAY_HEIGHT = 7
DISPLAY_WIDTH = 17

pixel = display.set_pixel
set_pixel = display.set_pixel
show = display.show
scroll = display.scroll
fill = display.fill
clear_rect = display.clear_rect
width = display.width
height = display.height
scroll_to = display.scroll_to
rotate = display.rotate
flip = display.flip
draw_char = display.draw_char
write_string = display.write_string
clear = display.clear
set_graph = display.set_graph

def _exit():
    display.clear()
    display.show()

atexit.register(_exit)
