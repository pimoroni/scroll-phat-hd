import math
import time

try:
    import numpy
except ImportError:
    exit("This library requires the numpy module\nInstall with: sudo pip install numpy")


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

class Matrix:
    width = 17
    height = 7

    def __init__(self, i2c, address=0x74):
        self.buf = numpy.zeros((self.width, self.height))
        self.i2c = i2c
        self.address = address
        self._reset()

        self._font = font5x7
        self._current_frame = 0
        self._scroll = [0,0]
        self._rotate = 0 # Increments of 90 degrees
        self._flipx = False
        self._flipy = False

        # Display initialization

        # Switch to configuration bank
        self._bank(_CONFIG_BANK)

        # Switch to Picture Mode
        self.i2c.write_i2c_block_data(self.address, _MODE_REGISTER, [_PICTURE_MODE])

        # Disable audio sync
        self.i2c.write_i2c_block_data(self.address, _AUDIOSYNC_REGISTER, [0])

        self._bank(1)
        self.i2c.write_i2c_block_data(self.address, 0, [255] * 17)

        # Switch to bank 0 ( frame 0 )
        self._bank(0)

        # Enable all LEDs
        self.i2c.write_i2c_block_data(self.address, 0, [255] * 17)

    def scroll(self, x=0, y=0):
        """Offset the buffer by x/y pixels

        Scroll pHAT HD displays an 17x7 pixel window into the bufer,
        which starts at the left offset and wraps around.

        The x and y values are added to the internal scroll offset.

        If called with no arguments, a horizontal right to left scroll is used.

        :param x: Amount to scroll on x-axis
        :param y: Amount to scroll on y-axis

        """

        if x == 0 and y == 0:
            x = -1

        self._scroll[0] += x
        self._scroll[1] += y

    def scroll_to(self, x=0, y=0):
        """Scroll the buffer to a specific location.

        Scroll pHAT HD displays a 17x7 pixel window into the buffer,
        which starts at the left offset and wraps around.

        The x and y values set the internal scroll offset.

        If called with no arguments, the scroll offset is reset to 0,0

        :param x: Position to scroll to on x-axis
        :param y: Position to scroll to on y-axis

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

        del self.buf
        self.buf = numpy.zeros((self.width, self.height))

    def draw_char(self, x, y, char, font=None, brightness=1.0):
        """Draw a single character to the buffer.

        :param o_x: Offset x - distance of the char from the left of the buffer
        :param o_y: Offset y - distance of the char from the top of the buffer
        :param char: Char to display- either an integer ordinal or a single letter
        :param font: Font to use, default is to use one specified with `set_font`
        :param brightness: Brightness of the pixels that compromise the char, from 0.0 to 1.0

        """

        if font is None:
            if self._font is not None:
                font = self._font
            else:
                return (x, y)

        if type(char) is not int:
            char = ord(char)

        if char not in font.data:
            return (x, y)

        char = font.data[char]

        for px in range(len(char[0])):
            for py in range(len(char)):
                self.set_pixel(x + px, y + py, (char[py][px] / 255.0) * brightness)

        return (x + px, y + font.height)

    def write_string(self, string, x=0, y=0, font=None, letter_spacing=1, brightness=1.0):
        """Write a string to the buffer. Calls draw_char for each character.

        :param string: The string to display
        :param x: Offset x - distance of the string from the left of the buffer
        :param y: Offset y - distance of the string from the top of the buffer
        :param font: Font to use, default is to use the one specified with `set_font`
        :param brightness: Brightness of the pixels that compromise the text, from 0.0 to 1.0

        """

        o_x = x

        for char in string:
            x, n = self.draw_char(x, y, char, font=font, brightness=brightness)
            x += 1 + letter_spacing

        return x - o_x

    def fill(self, brightness, x=0, y=0, width=0, height=0):
        """Fill an area of the display.

        :param brightness: Brightness of pixels
        :param x: Offset x - distance of the area from the left of the buffer
        :param y: Offset y - distance of the area from the top of the buffer
        :param width: Width of the area (default is 17)
        :param height: Height of the area (default is 7)

        """

        if width == 0:
            width = self.width

        if height == 0:
            height = self.height

        for px in range(width):
            for py in range(height):
                self.set_pixel(x+px, y+py,  brightness)

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
            width = self.width

        if height is None:
            height = self.height

        if low is None:
            low = min(values)

        if high is None:
            high = max(values)

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

            except KeyError:
                return

    def set_pixel(self, x, y, brightness):
        """Set a single pixel in the buffer.

        :param x: Position of pixel from left of buffer
        :param y: Position of pixel from top of buffer
        :param brightness: Intensity of the pixel, from 0.0 to 1.0 or 0 to 255.

        """

        brightness = int(255.0 * brightness)

        if brightness > 255 or brightness < 0:
            raise ValueError("Value {} out of range. Brightness should be between 0 and 1".format(brightness))

        try:
            self.buf[x][y] = brightness

        except IndexError:
            if y >= self.buf.shape[1]:
                self.buf = numpy.pad(self.buf, ((0,0),(0,y - self.buf.shape[1] + 1)), mode='constant')

            if x >= self.buf.shape[0]:
                self.buf = numpy.pad(self.buf, ((0,x - self.buf.shape[0] + 1),(0,0)), mode='constant')

            self.buf[x][y] = brightness

    def show(self):
        """Show the buffer contents on the display.

        The buffer is copied, then  scrolling, rotation and flip y/x
        transforms applied before taking a 17x7 slice and displaying.

        """

        next_frame = 0 if self._current_frame == 1 else 0

        display_buffer = numpy.copy(self.buf)

        for axis in [0,1]:
            if not self._scroll[axis] == 0:
                display_buffer = numpy.roll(display_buffer, -self._scroll[axis], axis=axis)

        # Chop a width * height window out of the display buffer
        display_buffer = display_buffer[:self.width, :self.height]

        if self._rotate:
            display_buffer = numpy.rot90(display_buffer, self._rotate)

        if self._flipy:
            display_buffer = numpy.flipud(display_buffer)

        if self._flipx:
            display_buffer = numpy.fliplr(display_buffer)

        output = [0 for x in range(144)]

        for x in range(self.width):
            for y in range(self.height):
                idx = self._pixel_addr(x, 6-y)

                try:
                    output[idx] = int(display_buffer[x][y])

                except IndexError:
                    output[idx] = 0

        self._bank(next_frame)

        offset = 0
        for chunk in self._chunk(output, 32):
            #print(chunk)
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

        #print "reg", value

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
