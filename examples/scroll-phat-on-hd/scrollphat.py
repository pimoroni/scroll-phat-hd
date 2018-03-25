#!/usr/bin/env python

try:
    import scrollphathd
except ImportError:
        exit("This library emulate scrollphat on a scrollphathd so it requires scrollphathd\nInstall with: sudo apt-get install ???")

font = {32: [], 33: [23], 34: [3, 0, 3], 35: [10, 31, 10, 31, 10], 36: [2, 21, 31, 21, 8], 37: [9, 4, 18], 38: [10, 21, 10, 16], 39: [3], 40: [14, 17], 41: [17, 14], 42: [20, 14, 20], 43: [4, 14, 4], 44: [16, 8], 45: [4, 4], 46: [16], 47: [24, 6], 48: [14, 21, 14], 49: [18, 31, 16], 50: [25, 21, 18], 51: [17, 21, 10], 52: [14, 9, 28], 53: [23, 21, 9], 54: [14, 21, 8], 55: [25, 5, 3], 56: [10, 21, 10], 57: [2, 21, 14], 58: [10], 59: [16, 10], 60: [4, 10], 61: [10, 10, 10], 62: [10, 4], 63: [1, 21, 2], 64: [14, 29, 21, 14], 65: [30, 5, 30], 66: [31, 21, 10], 67: [14, 17, 17], 68: [31, 17, 14], 69: [31, 21, 17], 70: [31, 5, 1], 71: [14, 17, 29], 72: [31, 4, 31], 73: [17, 31, 17], 74: [9, 17, 15], 75: [31, 4, 27], 76: [31, 16, 16], 77: [31, 2, 4, 2, 31], 78: [31, 2, 12, 31], 79: [14, 17, 14], 80: [31, 9, 6], 81: [14, 17, 9, 22], 82: [31, 9, 22], 83: [18, 21, 9], 84: [1, 31, 1], 85: [15, 16, 16, 15], 86: [15, 16, 15], 87: [15, 16, 8, 16, 15], 88: [27, 4, 27], 89: [3, 28, 3], 90: [25, 21, 19], 91: [31, 17], 92: [6, 24], 93: [17, 31], 94: [2, 1, 2], 95: [16, 16, 16], 96: [1, 2], 97: [8, 20, 28], 98: [31, 20, 8], 99: [8, 20], 100: [8, 20, 31], 101: [14, 21, 2], 102: [30, 5], 103: [2, 21, 15], 104: [31, 4, 24], 105: [29], 106: [16, 13], 107: [31, 4, 26], 108: [31], 109: [28, 4, 24, 4, 24], 110: [28, 4, 24], 111: [8, 20, 8], 112: [30, 10, 4], 113: [4, 10, 30], 114: [28, 2], 115: [20, 10], 116: [15, 18], 117: [12, 16, 28], 118: [12, 16, 12], 119: [12, 16, 8, 16, 12], 120: [20, 8, 20], 121: [2, 20, 14], 122: [18, 26, 22], 123: [4, 14, 17], 124: [31], 125: [17, 14, 4], 126: [8, 4, 8, 4], 127: []}

from .IS31FL3730 import IS31FL3730, I2cConstants


ROTATE_OFF = False
ROTATE_180 = True

controller = IS31FL3730(smbus, font)

def set_rotate(value):
    """Set the rotation of Scroll pHAT

    :param value: Rotate 180 degrees: True/False
    """

    controller.set_rotate(value)

# The public interface maintains compatibility with previous singleton
# pattern.
def rotate5bits(x):
    controller.rotate5bits(x)

def update():
    """Update Scroll pHAT with the current buffer"""

    scrollphathd.show()



def set_buffer(buf):
    """Overwrite the buffer

    :param buf: One dimensional array of int: 0 to 31 - pixels are 1,2,4,8,16 and 1 is top-most pixel
    """
    controller.set_buffer(buf)

def set_brightness(brightness):
    """Set the brightness of Scroll pHAT
    
    :param brightness: Brightness value: 0 to 255
    """
    scrollphathd.set_brightness(brightness)

def set_col(x, value):
    """Set a single column in the buffer

    :param x: Position of column to set, buffer will auto-expand if necessary
    :param value: Value to set: 0 to 31 - pixels are 1,2,4,8,16 and 1 is top-most pixel
    """
    controller.set_col(x, value)

def write_string( chars, x = 0):
    """Write a text string to the buffer

    :param chars: Text string to write
    :param x: Left offset in pixels
    """
    controller.write_string(chars,x)

def graph(values, low=None, high=None):
    """Write a bar graph to the buffer

    :param values: List of values to display
    :param low: Lowest possible value (default min(values))
    :param high: Highest possible value (default max(values))
    """
    controller.graph(values, low, high)

def buffer_len():
    """Returns the length of the internal buffer"""
    return controller.buffer_len()

def scroll(delta = 1):
    """Scroll the offset

    Scroll pHAT displays an 11 column wide window into the buffer,
    which starts at the left offset.

    :param delta: Amount to scroll (default 1)
    """
    controller.scroll(delta)

def clear_buffer():
    """Clear just the buffer, do not update Scroll pHAT"""
    controller.clear_buffer()

def clear():
    """Clear the buffer, and then update Scroll pHAT"""
    controller.clear()

def load_font(new_font):
    """Replace the internal font array

    The font is a dictionary of lists, keyed on character ordinal.

    For example, space ' ' would have the key 32 (ord(' ')).

    Each list includes one or more numbers between 0 and 31, these
    numbers specify which pixels in that column will be on.

    Each pixel is assigned a bit, either: 1, 2, 4, 8 or 16.

    1 is the top-most pixel (nearest the header) and 16 the bottom-most.

    A value of 17 would light the top and bottom pixels.
    """
    controller.load_font(new_font)

def scroll_to(pos = 0):
    """Set the internal offset to a specific position

    :param pos: Position to set
    """
    controller.scroll_to(pos)

def io_errors():
    """Return the internal count of IO Error events"""
    return controller.io_errors()

def set_pixel(x,y,value):
    """Turn a specific pixel on or off

    :param x: The horizontal position of the pixel
    :param y: The vertical position of the pixel: 0 to 4
    :param value: On/Off state: True/False
    """
    controller.set_pixel(x,y,value)
    scrollphathd.pixel(x, y, value)

def set_pixels(handler, auto_update=False):
    """Use a pixel shader function to set 11x5 pixels

    Useful for displaying patterns and animations, or the result of simple functions. For example::

        scrollphat.set_pixels(lambda x, y: (x + y) % 2, True)

    Will display a check pattern.

    :param handler: A function which accepts an x and y position, and returns True or False
    :param auto_update: Whether to update Scroll pHAT after setting all pixels (default False)    
    """
    for x in range(11):
        for y in range(5):
            set_pixel(x, y, handler(x, y))
    if auto_update:
        update()
