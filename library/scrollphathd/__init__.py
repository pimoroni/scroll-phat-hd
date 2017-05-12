import atexit
from sys import exit, version_info

try:
    import smbus
except ImportError:
    if version_info[0] < 3:
        exit("This library requires python-smbus\nInstall with: sudo apt-get install python-smbus")
    elif version_info[0] == 3:
        exit("This library requires python3-smbus\nInstall with: sudo apt-get install python3-smbus")

from . import is31fl3731

__version__ = '1.0.1'

i2c = None

try:
    i2c = smbus.SMBus(1)
except IOError as e:
    if hasattr(e,"errno") and e.errno == 2:
        e.strerror += "\n\nMake sure you've enabled i2c in your Raspberry Pi configuration.\n"
    raise e

display = is31fl3731.ScrollPhatHD(i2c, gamma_table=is31fl3731.LED_GAMMA)
_clear_on_exit = True

DISPLAY_HEIGHT = 7
DISPLAY_WIDTH = 17

pixel = display.set_pixel
set_pixel = display.set_pixel
set_brightness = display.set_brightness
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
get_buffer_shape = display.get_buffer_shape
get_shape = display.get_shape

def set_clear_on_exit(value=True):
    """Set whether Scroll pHAT HD should be cleared upon exit.

    By default Scroll pHAT HD will turn off the pixels on exit, but calling::

        scrollphathd.set_clear_on_exit(False)

    Will ensure that it does not.

    :param value: True or False (default True)

    """

    global _clear_on_exit
    _clear_on_exit = value

def _exit():
    if _clear_on_exit:
        display.clear()
        display.show()

atexit.register(_exit)
