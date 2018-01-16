from sys import version_info
from .api.http import start_background_thread, scrollphathd_blueprint
from . import is31fl3731

__version__ = '1.1.1'

display = is31fl3731.ScrollPhatHD(None, gamma_table=is31fl3731.LED_GAMMA)

DISPLAY_HEIGHT = display._height
DISPLAY_WIDTH = display._width

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
set_clear_on_exit = display.set_clear_on_exit

