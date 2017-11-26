from sys import exit, version_info

import scrollphathd

try:
    import smbus
except ImportError:
    if version_info[0] < 3:
        raise ImportError("This library requires python-smbus\nInstall with: sudo apt-get install python-smbus")
    elif version_info[0] == 3:
        raise ImportError("This library requires python3-smbus\nInstall with: sudo apt-get install python3-smbus")

MODE_5X11 = 0b00000011

class I2cConstants:
    def __init__(self):
        self.I2C_ADDR = 0x60
        self.CMD_SET_MODE = 0x00
        self.CMD_SET_BRIGHTNESS = 0x19
        self.MODE_5X11 = 0b00000011

class IS31FL3730:
    def __init__(self, smbus, font):
        self.bus = smbus
        self.font = font
        self.i2cConstants = I2cConstants()
        self._rotate = False

        self.bus = self.bus.SMBus(1)
        self.buffer = [0] * 11
        self.offset = 0
        self.error_count = 0
        self.set_mode(self.i2cConstants.MODE_5X11)

    def set_rotate(self, value):
        self._rotate = value

    def rotate5bits(self, x):
        r = 0
        if x & 16:
            r = r | 1
        if x & 8:
            r = r | 2
        if x & 4:
            r = r | 4
        if x & 2:
            r = r | 8
        if x & 1:
            r = r | 16
        return r

    def update(self):
        if self.offset + 11 <= len(self.buffer):
            self.window = self.buffer[self.offset:self.offset + 11]
        else:
            self.window = self.buffer[self.offset:]
            self.window += self.buffer[:11 - len(self.window)]

        if self._rotate:
            self.window.reverse()
            for i in range(len(self.window)):
                self.window[i] = self.rotate5bits(self.window[i])

        self.window.append(0xff)


### Copy the buffer to ScrollphatHD vvv
        real_brightness = max (self.brightness / 255, 0.1)
        for x in range(0, 11):
            for y in range(0, 5):
                if ( (self.window[x] & (1 << y)) == 0):
                    scrollphathd.set_pixel(x+3, y+1, 0.0)
                else:
                    scrollphathd.set_pixel(x+3, y+1, real_brightness)
        scrollphathd.show()
### Copy the buffer to ScrollphatHD ^^^



#        try:
#            self.bus.write_i2c_block_data(self.i2cConstants.I2C_ADDR, 0x01, self.window)
#        except IOError:
#            self.error_count += 1
#            if self.error_count == 10:
#                print("A high number of IO Errors have occurred, please check your soldering/connections.")

    def set_mode(self, mode=MODE_5X11):
         pass
#        self.bus.write_i2c_block_data(self.i2cConstants.I2C_ADDR, self.i2cConstants.CMD_SET_MODE, [self.i2cConstants.MODE_5X11])

    def get_brightness(self):
        if hasattr(self, 'brightness'):
            return self.brightness
        return -1

    def set_brightness(self, brightness):
        self.brightness = brightness
#        self.bus.write_i2c_block_data(self.i2cConstants.I2C_ADDR, self.i2cConstants.CMD_SET_BRIGHTNESS, [self.brightness])

    def set_col(self, x, value):
        if len(self.buffer) <= x:
            self.buffer += [0] * (x - len(self.buffer) + 1)

        self.buffer[x] = value

    def write_string(self, chars, x = 0):
        for char in chars:
            if ord(char) == 0x20 or ord(char) not in self.font:
                self.set_col(x, 0)
                x += 1
                self.set_col(x, 0)
                x += 1
                self.set_col(x, 0)
                x += 1
            else:
                font_char = self.font[ord(char)]
                for i in range(0, len(font_char)):
                    self.set_col(x, font_char[i])
                    x += 1

                self.set_col(x, 0)
                x += 1 # space between chars
        self.update()

    # draw a graph across the screen either using
    # the supplied min/max for scaling or auto
    # scaling the output to the min/max values
    # supplied
    def graph(self, values, low=None, high=None):
        values = [float(x) for x in values]

        if low == None:
            low = min(values)

        if high == None:
            high = max(values)

        span = high - low

        for col, value in enumerate(values):
            value -= low
            value /= span
            value *= 5

            if value > 5: value = 5
            if value < 0: value = 0

            self.set_col(col, [0,16,24,28,30,31][int(value)])

        self.update()

    def set_buffer(self, replacement):
        self.buffer = replacement

    def buffer_len(self):
        return len(self.buffer)

    def scroll(self, delta = 1):
        self.offset += delta
        self.offset %= len(self.buffer)
        self.update()

    def clear_buffer(self):
        self.offset = 0
        self.buffer = [0] * 11

    def clear(self):
        self.clear_buffer()
        self.update()

    def load_font(self, new_font):
        self.font = new_font

    def scroll_to(self, pos = 0):
        self.offset = pos
        self.offset %= len(self.buffer)
        self.update()

    def io_errors(self):
        return self.error_count

    def set_pixel(self, x,y,value):
        if value:
            self.buffer[x] |= (1 << y)
        else:
            self.buffer[x] &= ~(1 << y)

font = {32: [], 33: [23], 34: [3, 0, 3], 35: [10, 31, 10, 31, 10], 36: [2, 21, 31, 21, 8], 37: [9, 4, 18], 38: [10, 21, 10, 16], 39: [3], 40: [14, 17], 41: [17, 14], 42: [20, 14, 20], 43: [4, 14, 4], 44: [16, 8], 45: [4, 4], 46: [16], 47: [24, 6], 48: [14, 21, 14], 49: [18, 31, 16], 50: [25, 21, 18], 51: [17, 21, 10], 52: [14, 9, 28], 53: [23, 21, 9], 54: [14, 21, 8], 55: [25, 5, 3], 56: [10, 21, 10], 57: [2, 21, 14], 58: [10], 59: [16, 10], 60: [4, 10], 61: [10, 10, 10], 62: [10, 4], 63: [1, 21, 2], 64: [14, 29, 21, 14], 65: [30, 5, 30], 66: [31, 21, 10], 67: [14, 17, 17], 68: [31, 17, 14], 69: [31, 21, 17], 70: [31, 5, 1], 71: [14, 17, 29], 72: [31, 4, 31], 73: [17, 31, 17], 74: [9, 17, 15], 75: [31, 4, 27], 76: [31, 16, 16], 77: [31, 2, 4, 2, 31], 78: [31, 2, 12, 31], 79: [14, 17, 14], 80: [31, 9, 6], 81: [14, 17, 9, 22], 82: [31, 9, 22], 83: [18, 21, 9], 84: [1, 31, 1], 85: [15, 16, 16, 15], 86: [15, 16, 15], 87: [15, 16, 8, 16, 15], 88: [27, 4, 27], 89: [3, 28, 3], 90: [25, 21, 19], 91: [31, 17], 92: [6, 24], 93: [17, 31], 94: [2, 1, 2], 95: [16, 16, 16], 96: [1, 2], 97: [8, 20, 28], 98: [31, 20, 8], 99: [8, 20], 100: [8, 20, 31], 101: [14, 21, 2], 102: [30, 5], 103: [2, 21, 15], 104: [31, 4, 24], 105: [29], 106: [16, 13], 107: [31, 4, 26], 108: [31], 109: [28, 4, 24, 4, 24], 110: [28, 4, 24], 111: [8, 20, 8], 112: [30, 10, 4], 113: [4, 10, 30], 114: [28, 2], 115: [20, 10], 116: [15, 18], 117: [12, 16, 28], 118: [12, 16, 12], 119: [12, 16, 8, 16, 12], 120: [20, 8, 20], 121: [2, 20, 14], 122: [18, 26, 22], 123: [4, 14, 17], 124: [31], 125: [17, 14, 4], 126: [8, 4, 8, 4], 127: []}

__version__ = '0.0.7'

ROTATE_OFF = False
ROTATE_180 = True

controller = None

def _get_controller():
    global controller

    if controller is None:
        controller = IS31FL3730(smbus, font)

    return controller

def set_rotate(value):
    """Set the rotation of Scroll pHAT

    :param value: Rotate 180 degrees: True/False
    """

    _get_controller().set_rotate(value)

# The public interface maintains compatibility with previous singleton
# pattern.
def rotate5bits(x):
    _get_controller().rotate5bits(x)

def update():
    """Update Scroll pHAT with the current buffer"""

    _get_controller().update()

def set_buffer(buf):
    """Overwrite the buffer

    :param buf: One dimensional array of int: 0 to 31 - pixels are 1,2,4,8,16 and 1 is top-most pixel
    """
    _get_controller().set_buffer(buf)

def set_brightness(brightness):
    """Set the brightness of Scroll pHAT
    
    :param brightness: Brightness value: 0 to 255
    """
    _get_controller().set_brightness(brightness)

def set_col(x, value):
    """Set a single column in the buffer

    :param x: Position of column to set, buffer will auto-expand if necessary
    :param value: Value to set: 0 to 31 - pixels are 1,2,4,8,16 and 1 is top-most pixel
    """
    _get_controller().set_col(x, value)

def write_string( chars, x = 0):
    """Write a text string to the buffer

    :param chars: Text string to write
    :param x: Left offset in pixels
    """
    _get_controller().write_string(chars,x)

def graph(values, low=None, high=None):
    """Write a bar graph to the buffer

    :param values: List of values to display
    :param low: Lowest possible value (default min(values))
    :param high: Highest possible value (default max(values))
    """
    _get_controller().graph(values, low, high)

def buffer_len():
    """Returns the length of the internal buffer"""
    return _get_controller().buffer_len()

def scroll(delta = 1):
    """Scroll the offset

    Scroll pHAT displays an 11 column wide window into the buffer,
    which starts at the left offset.

    :param delta: Amount to scroll (default 1)
    """
    _get_controller().scroll(delta)

def clear_buffer():
    """Clear just the buffer, do not update Scroll pHAT"""
    _get_controller().clear_buffer()

def clear():
    """Clear the buffer, and then update Scroll pHAT"""
    _get_controller().clear()

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
    _get_controller().load_font(new_font)

def scroll_to(pos = 0):
    """Set the internal offset to a specific position

    :param pos: Position to set
    """
    _get_controller().scroll_to(pos)

def io_errors():
    """Return the internal count of IO Error events"""
    return _get_controller().io_errors()

def set_pixel(x,y,value):
    """Turn a specific pixel on or off

    :param x: The horizontal position of the pixel
    :param y: The vertical position of the pixel: 0 to 4
    :param value: On/Off state: True/False
    """
    _get_controller().set_pixel(x,y,value)

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
