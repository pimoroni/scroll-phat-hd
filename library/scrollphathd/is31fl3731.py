import math
import time
import atexit

try:
    import numpy
except ImportError:
    raise ImportError("This library requires the numpy module\nInstall with: sudo pip install numpy")

try:
    import smbus
except ImportError:
    if version_info[0] < 3:
        raise ImportError("This library requires python-smbus\nInstall with: sudo apt-get install python-smbus")
    elif version_info[0] == 3:
        raise ImportError("This library requires python3-smbus\nInstall with: sudo apt-get install python3-smbus")

# Default font
from .fonts import font5x7

_MODE_REGISTER = 0x00
_FRAME_REGISTER = 0x01
_AUTOPLAY1_REGISTER = 0x02
_AUTOPLAY2_REGISTER = 0x03
_BLINK_REGISTER = 0x05
_AUDIOSYNC_REGISTER = 0x06
_BREATH1_REGISTER = 0x08
_BREATH2_REGISTER = 0x09
_SHUTDOWN_REGISTER = 0x0a
_GAIN_REGISTER = 0x0b
_ADC_REGISTER = 0x0c

_CONFIG_BANK = 0x0b
_BANK_ADDRESS = 0xfd

_PICTURE_MODE = 0x00
_AUTOPLAY_MODE = 0x08
_AUDIOPLAY_MODE = 0x18

_ENABLE_OFFSET = 0x00
_BLINK_OFFSET = 0x12
_COLOR_OFFSET = 0x24

LED_GAMMA = [
0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5,
6, 6, 6, 7, 7, 7, 8, 8, 8, 9, 9, 9, 10, 10, 11, 11,
11, 12, 12, 13, 13, 13, 14, 14, 15, 15, 16, 16, 17, 17, 18, 18,
19, 19, 20, 21, 21, 22, 22, 23, 23, 24, 25, 25, 26, 27, 27, 28,
29, 29, 30, 31, 31, 32, 33, 34, 34, 35, 36, 37, 37, 38, 39, 40,
40, 41, 42, 43, 44, 45, 46, 46, 47, 48, 49, 50, 51, 52, 53, 54,
55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70,
71, 72, 73, 74, 76, 77, 78, 79, 80, 81, 83, 84, 85, 86, 88, 89,
90, 91, 93, 94, 95, 96, 98, 99,100,102,103,104,106,107,109,110,
111,113,114,116,117,119,120,121,123,124,126,128,129,131,132,134,
135,137,138,140,142,143,145,146,148,150,151,153,155,157,158,160,
162,163,165,167,169,170,172,174,176,178,179,181,183,185,187,189,
191,193,194,196,198,200,202,204,206,208,210,212,214,216,218,220,
222,224,227,229,231,233,235,237,239,241,244,246,248,250,252,255]

class Matrix:
    _width = 17
    _height = 7

    def __init__(self, i2c, address=0x74, gamma_table=None):
        self.i2c = i2c
        self.address = address
        self._is_setup = False
        self._clear_on_exit = True

        if gamma_table is None:
            gamma_table = list(range(256))

        self._gamma_table = gamma_table

        self._font = font5x7
        self._rotate = 0 # Increments of 90 degrees
        self._flipx = False
        self._flipy = False
        self._brightness = 1.0

        self.clear()

    def setup(self):
        if self._is_setup:
            return True

        self._is_setup = True

        if self.i2c is None:
            try:
                self.i2c = smbus.SMBus(1)
            except IOError as e:
                if hasattr(e,"errno") and e.errno == 2:
                    e.strerror += "\n\nMake sure you've enabled i2c in your Raspberry Pi configuration.\n"
                raise e

        try:
            self._reset()
        except IOError as e:
            if hasattr(e,"errno") and e.errno == 5:
                e.strerror += "\n\nMake sure your Scroll pHAT HD is attached, and double-check your soldering.\n"
            raise e

        self.show()

        # Display initialization

        # Switch to configuration bank
        self._bank(_CONFIG_BANK)

        # Switch to Picture Mode
        self.i2c.write_i2c_block_data(self.address, _MODE_REGISTER, [_PICTURE_MODE])

        # Disable audio sync
        self.i2c.write_i2c_block_data(self.address, _AUDIOSYNC_REGISTER, [0])

        # Enable only connected LEDs,
        # Bytes correspond to groups of 8 LEDs, little-endian
        # eg: [ 7 6 5 4 3 2 1 0 ] [ 15 14 13 12 11 10 9 8 ]
        # This is a bi-directional 8x9 matrix, for a total of 144 LEDs
        # we're enabling 119 (17x7) of them.
        enable_pattern = [
        #   Matrix A    Matrix B
            0b01111111, 0b01111111,
            0b01111111, 0b01111111,
            0b01111111, 0b01111111,
            0b01111111, 0b01111111,
            0b01111111, 0b01111111,
            0b01111111, 0b01111111,
            0b01111111, 0b01111111,
            0b01111111, 0b01111111,
            0b01111111, 0b00000000,
        ]

        # Enable LEDs
        for bank in [1, 0]:
            self._bank(bank)
            self.i2c.write_i2c_block_data(self.address, 0x00, enable_pattern)

        # Switch to bank 0 ( frame 0 )
        self._bank(0)

        atexit.register(self._exit)

    def set_clear_on_exit(self, value=True):
        """Set whether Scroll pHAT HD should be cleared upon exit.

        By default Scroll pHAT HD will turn off the pixels on exit, but calling::

            scrollphathd.set_clear_on_exit(False)

        Will ensure that it does not.

        :param value: True or False (default True)

        """

        self._clear_on_exit = value

    def _exit(self):
        if self._clear_on_exit:
            self.clear()
            self.show()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def set_gamma(self, gamma_table):
        """Set the LED gamma table.

        Set the table of values used to give the LEDs a pleasing
        to the eye brightness curve.

        :param gamma_table: List of 256 values in the range 0-255.

        """

        if len(gamma_table) != 256 or not isinstance(gamma_table, list):
            raise ValueError("Gamma table must be a list with 256 values.")

        self._gamma_table = gamma_table

    def scroll(self, x=1, y=0):
        """Offset the buffer by x/y pixels.

        Scroll pHAT HD displays an 17x7 pixel window into the buffer,
        which starts at the left offset and wraps around.

        The x and y values are added to the internal scroll offset.

        If called with no arguments, a horizontal right to left scroll is used.

        :param x: Amount to scroll on x-axis (default 1)
        :param y: Amount to scroll on y-axis (default 0)

        """

        self._scroll[0] += x
        self._scroll[1] += y

    def scroll_to(self, x=0, y=0):
        """Scroll the buffer to a specific location.

        Scroll pHAT HD displays a 17x7 pixel window into the buffer,
        which starts at the left offset and wraps around.

        The x and y values set the internal scroll offset.

        If called with no arguments, the scroll offset is reset to 0,0

        :param x: Position to scroll to on x-axis (default 0)
        :param y: Position to scroll to on y-axis (default 0)

        """

        self._scroll = [x,y]

    def rotate(self, degrees=0):
        """Rotate the buffer 0, 90, 180 or 270 degrees before dislaying.


        :param degrees: Amount to rotate- will snap to the nearest 90 degrees

        """

        self._rotate = int(round(degrees/90.0))

    def flip(self, x=False, y=False):
        """Flip the buffer horizontally and/or vertically before displaying.

        :param x: Flip horizontally left to right
        :param y: Flip vertically up to down

        """

        self._flipx = x
        self._flipy = y

    def clear(self):
        """Clear the buffer

        You must call `show` after clearing the buffer to update the display.

        """

        self._current_frame = 0
        self._scroll = [0,0]

        try:
            del self.buf
        except AttributeError:
            pass

        self.buf = numpy.zeros((self._width, self._height))

    def draw_char(self, x, y, char, font=None, brightness=1.0, monospaced=False):
        """Draw a single character to the buffer.

        Returns the x and y coordinates of the bottom left-most corner of the drawn character.

        :param o_x: Offset x - distance of the char from the left of the buffer
        :param o_y: Offset y - distance of the char from the top of the buffer
        :param char: Char to display- either an integer ordinal or a single letter
        :param font: Font to use, default is to use one specified with `set_font`
        :param brightness: Brightness of the pixels that compromise the char, from 0.0 to 1.0
        :param monospaced: Whether to space characters out evenly

        """

        if font is None:
            if self._font is not None:
                font = self._font
            else:
                return (x, y)

        if char in font.data:
            char_map = font.data[char]
        elif type(char) is not int and ord(char) in font.data:
            char_map = font.data[ord(char)]
        else:
            return (x, y)

        for px in range(len(char_map[0])):
            for py in range(len(char_map)):
                pixel = char_map[py][px]
                if pixel > 0:
                    self.set_pixel(x + px, y + py, (pixel / 255.0) * brightness)

        if monospaced:
            px = font.width - 1

        return (x + px, y + font.height)

    def calculate_string_width(self, string, font=None, letter_spacing=1, monospaced=False):
        """Calculate the width of a string.

        :param string: The string to measure
        :param font: Font to use, default is to use the one specified with `set_font`
        :param letter_spacing: Distance (in pixels) between characters
        :param monospaced: Whether to space characters out evenly (using `font.width`)

        """

        width = 0

        for char in string:
            width += self.calculate_char_width(char, font=font, monospaced=monospaced)
            width += 1 + letter_spacing

        return width

    def calculate_char_width(self, char, font=None, monospaced=False):
        """Calculate the width of a single character.

        :param char: The character to measure
        :param font: Font to use, default is to use the one specified with `set_font`
        :param monospaced: Whether to space characters out evenly (using `font.width`)

        """
 
        if font is None:
            if self._font is not None:
                font = self._font
            else:
                return 0

        if char in font.data:
            char_map = font.data[char]
        elif type(char) is not int and ord(char) in font.data:
            char_map = font.data[ord(char)]
        else:
            return 0

        if monospaced:
            return font.width - 1
        else:
            return len(char_map[0]) - 1

    def write_string(self, string, x=0, y=0, font=None, letter_spacing=1, brightness=1.0, monospaced=False, fill_background=False):
        """Write a string to the buffer. Calls draw_char for each character.

        :param string: The string to display
        :param x: Offset x - distance of the string from the left of the buffer
        :param y: Offset y - distance of the string from the top of the buffer
        :param letter_spacing: Distance (in pixels) between characters
        :param font: Font to use, default is to use the one specified with `set_font`
        :param brightness: Brightness of the pixels that compromise the text, from 0.0 to 1.0
        :param monospaced: Whether to space characters out evenly (using `font.width`)
        :param fill_background: Not used!

        """

        o_x = x

        if font is None:
            if self._font is not None:
                font = self._font
            else:
                raise ValueError("Must supply a valid font")

        string_width = self.calculate_string_width(string, font, letter_spacing, monospaced)

        # Grow the buffer once to avoid *very* slow incremental growth as each individual pixel is set
        self.buf = self._grow_buffer(self.buf, (x + string_width, y + font.height))

        for char in string:
            x, n = self.draw_char(x, y, char, font=font, brightness=brightness, monospaced=monospaced)
            x += 1 + letter_spacing

        return x - o_x

    def fill(self, brightness, x=0, y=0, width=None, height=None):
        """Fill an area of the display.

        :param brightness: Brightness of pixels
        :param x: Offset x - distance of the area from the left of the buffer
        :param y: Offset y - distance of the area from the top of the buffer
        :param width: Width of the area (default is buffer width)
        :param height: Height of the area (default is buffer height)

        """

        if width is None:
            width = self.buf.shape[0]

        if height is None:
            height = self.buf.shape[1]

        # if the buffer is not big enough, grow it in one operation.
        if (x + width) > self.buf.shape[0] or (y + height) > self.buf.shape[1]:
            self.buf = self._grow_buffer(self.buf, (x + width, y + height))

        # fill in one operation using a slice
        self.buf[x:x+width,y:y+height] = brightness

    def clear_rect(self, x, y, width, height):
        """Clear a rectangle.

        :param x: Offset x - distance of the area from the left of the buffer
        :param y: Offset y - distance of the area from the top of the buffer
        :param width: Width of the area (default is 17)
        :param height: Height of the area (default is 7)

        """

        self.fill(0, x, y, width, height)

    def set_graph(self, values, low=None, high=None, brightness=1.0, x=0, y=0, width=None, height=None):
        """Plot a series of values into the display buffer.

        :param values: A list of numerical values to display
        :param low: The lowest possible value (default min(values))
        :param high:  The highest possible value (default max(values))
        :param brightness:  Maximum graph brightness (from 0.0 to 1.0)
        :param x: x position of graph in display buffer (default 0)
        :param y: y position of graph in display buffer (default 0)
        :param width: width of graph in display buffer (default 17)
        :param height: height of graph in display buffer (default 7)
        :return: None

        """
        if width is None:
            width = self._width

        if height is None:
            height = self._height

        if low is None:
            low = min(values)

        if high is None:
            high = max(values)

        self.buf = self._grow_buffer(self.buf, (x + width, y + height))

        span = high - low

        for p_x in range(width):
            try:
                value = values[p_x]
                value -= low
                value /= float(span)
                value *= height * 10.0

                value = min(value, height * 10)
                value = max(value, 0)

                for p_y in range(height):
                    self.set_pixel(x+p_x, y+(height-p_y), brightness if value > 10 else (value / 10.0) * brightness)
                    value -= 10
                    if value < 0:
                        value = 0

            except IndexError:
                return

    def set_brightness(self, brightness):
        """Set a global brightness value.

        :param brightness: Brightness value from 0.0 to 1.0

        """

        self._brightness = brightness

    def set_font(self, font):
        """Set a global font value.

        :param font: Font value from .font (font3x5, font5x5, font5x7, font5x7smoothed)

        Note: Import the font before invoking set_font(), (available by) default is font5x7.

        """

        self._font = font

    def _grow_buffer(self, buffer, newshape):
        """Grows a copy of buffer until the new shape fits inside it.

        :param buffer: Buffer to grow.
        :param newshape: Tuple containing the minimum (x,y) size.

        Returns the new buffer.

        """
        x_pad = max(0, newshape[0] - buffer.shape[0])
        y_pad = max(0, newshape[1] - buffer.shape[1])

        return numpy.pad(buffer, ((0, x_pad), (0, y_pad)), 'constant')

    def set_pixel(self, x, y, brightness):
        """Set a single pixel in the buffer.

        :param x: Position of pixel from left of buffer
        :param y: Position of pixel from top of buffer
        :param brightness: Intensity of the pixel, from 0.0 to 1.0.

        """

        if brightness > 1.0 or brightness < 0:
            raise ValueError("Value {} out of range. Brightness must be between 0 and 1".format(brightness))

        if x < 0 or y < 0:
            raise ValueError("Pixel coordinates x and y must be positive integers")

        try:
            self.buf[x][y] = brightness

        except IndexError:
            self.buf = self._grow_buffer(self.buf, (x+1, y+1))
            self.buf[x][y] = brightness

    def get_buffer_shape(self):
        """Get the size/shape of the internal buffer.

        Returns a tuple containing the width and height of the buffer.

        """

        return self.buf.shape

    def get_shape(self):
        """Get the size/shape of the display.

        Returns a tuple containing the width and height of the display,
        after applying rotation.

        """

        if self._rotate % 2:
            return (self._height, self._width)
        else:
            return (self._width, self._height)

    def show(self, before_display=None):
        """Show the buffer contents on the display.

        The buffer is copied, then  scrolling, rotation and flip y/x
        transforms applied before taking a 17x7 slice and displaying.

        """

        self.setup()

        next_frame = 0 if self._current_frame == 1 else 0
        display_shape = self.get_shape()

        display_buffer = self._grow_buffer(self.buf, display_shape)

        for axis in [0,1]:
            if not self._scroll[axis] == 0:
                display_buffer = numpy.roll(display_buffer, -self._scroll[axis], axis=axis)

        # Chop a width * height window out of the display buffer
        display_buffer = display_buffer[:display_shape[0], :display_shape[1]]

        # Allow the cropped buffer to be modified in-place before it's transformed and displayed
        # This permits static elements to be drawn over the top of a scrolling buffer
        if callable(before_display):
            display_buffer = before_display(display_buffer)

        if self._flipx:
            display_buffer = numpy.flipud(display_buffer)

        if self._flipy:
            display_buffer = numpy.fliplr(display_buffer)

        if self._rotate:
            display_buffer = numpy.rot90(display_buffer, self._rotate)

        output = [0 for x in range(144)]

        for x in range(self._width):
            for y in range(self._height):
                idx = self._pixel_addr(x, self._height-(y+1))

                try:
                    output[idx] = self._gamma_table[int(display_buffer[x][y] * 255 * self._brightness)]

                except IndexError:
                    output[idx] = 0

        self._bank(next_frame)

        offset = 0
        for chunk in self._chunk(output, 32):
            self.i2c.write_i2c_block_data(self.address, _COLOR_OFFSET + offset, chunk)
            offset += 32

        self._frame(next_frame)

        del display_buffer

    def _reset(self):
        self._sleep(True)
        time.sleep(0.00001)
        self._sleep(False)

    def _sleep(self, value):
        return self._register(_CONFIG_BANK, _SHUTDOWN_REGISTER, not value)

    def _frame(self, frame=None, show=True):
        if frame is None:
            return self._current_frame

        if not 0 <= frame <= 8:
            raise ValueError("Frame out of range: 0-8")

        self._current_frame = frame

        if show:
            self._register(_CONFIG_BANK, _FRAME_REGISTER, frame);

    def _bank(self, bank=None):
        """Switch display driver memory bank"""

        if bank is None:
            return self.i2c.readfrom_mem(self.address, _BANK_ADDRESS, 1)[0]

        self.i2c.write_i2c_block_data(self.address, _BANK_ADDRESS, [bank])

    def _register(self, bank, register, value=None):
        """Write display driver register"""

        self._bank(bank)

        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]

        self.i2c.write_i2c_block_data(self.address, register, [value])

    def _chunk(self, l, n):
        for i in range(0, len(l)+1, n):
            yield l[i:i + n]

    def _pixel_addr(self, x, y):
        return x + y * 16


class ScrollPhatHD(Matrix):
    width = 17
    height = 7

    def _pixel_addr(self, x, y):
        if x > 8:
            x = x - 8
            y = 6 - (y + 8)
        else:
            x = 8 - x

        return x * 16 + y
