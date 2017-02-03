import math
import time
import numpy

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
        self.reset()
        self.init()
       
        self._font = None
        self._frame = 0 
        self._scroll = [0,0]
        self._rotate = 0 # Increments of 90 degrees
        self._flipx = False
        self._flipy = False
        
    def scroll(self, x=0, y=0):
        self._scroll[0] += x
        self._scroll[1] += y
        
    def scroll_to(self, x=0, y=0):
        self._scroll = [x,y]

    def rotate(self, degrees=0):
        self._rotate = int(round(degrees/90.0))
        
    def flip(self, x=False, y=False):
        self._flipx = x
        self._flipy = y

    def _bank(self, bank=None):
        #print "bank", bank

        if bank is None:
            return self.i2c.readfrom_mem(self.address, _BANK_ADDRESS, 1)[0]

        self.i2c.write_i2c_block_data(self.address, _BANK_ADDRESS, [bank])

    def _register(self, bank, register, value=None):
        self._bank(bank)

        if value is None:
            return self.i2c.readfrom_mem(self.address, register, 1)[0]

        #print "reg", value

        self.i2c.write_i2c_block_data(self.address, register, [value])

    def draw_char(self, o_x, o_y, char, font=None):
        if font is None:
            if self._font is not None:
                font = self._font
            else:
                return (o_x, o_y)

        if char not in font.data:
            return (o_x, o_y)

        char = font.data[char]

        for x in range(font.width):
            for y in range(font.height):
                self.pixel(o_x + x, o_y + y, char[y][x])

        return (o_x + x, o_y + y)

    def init(self):
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

    def reset(self):
        self.sleep(True)
        time.sleep(0.00001)
        self.sleep(False)

    def sleep(self, value):
        return self._register(_CONFIG_BANK, _SHUTDOWN_REGISTER, not value)

    def frame(self, frame=None, show=True):
        if frame is None:
            return self._frame

        if not 0 <= frame <= 8:
            raise ValueError("Frame out of range: 0-8")

        self._frame = frame
        if show:
            self._register(_CONFIG_BANK, _FRAME_REGISTER, frame);

    def fill(self, brightness):
        for x in range(self.width):
            for y in range(self.height):
                self.pixel(x, y,  brightness)

        self.show()

    def _pixel_addr(self, x, y):
        return x + y * 16
        
    def pixel(self, x, y, brightness):
        try:
            self.buf[x][y] = brightness
        
        except IndexError:
            if y >= self.buf.shape[1]:
                self.buf = numpy.pad(self.buf, ((0,0),(0,y - self.buf.shape[1] + 1)), mode='constant')
                
            if x >= self.buf.shape[0]:
                self.buf = numpy.pad(self.buf, ((0,x - self.buf.shape[0] + 1),(0,0)), mode='constant')
                
            self.buf[x][y] = brightness
        
    def show(self):
        next_frame = 0 if self.frame == 1 else 0

        display_buffer = numpy.copy(self.buf)
        
        for axis in [0,1]:
            if not self._scroll[axis] == 0:
                display_buffer = numpy.roll(display_buffer, self._scroll[axis], axis=axis)
                
        if self._rotate:
            display_buffer = numpy.rot90(display_buffer, self._rotate)
            
        if self._flipy:
            display_buffer = numpy.flipud(display_buffer)
            
        if self._flipx:
            display_buffer = numpy.fliplr(display_buffer)
            
        # Chop a width * height window out of the display buffer
        display_buffer = display_buffer[:self.width, :self.height]
        
        #if self.height > display_buffer.shape[1]:
        #    display_buffer = numpy.pad(display_buffer, ((0,0),(0,self.height - display_buffer.shape[1] + 1)), mode='constant')
            
        #if self.width > display_buffer.shape[0]:
        #    display_buffer = numpy.pad(display_buffer, ((0,self.width - display_buffer.shape[0] + 1),(0,0)), mode='constant')
        
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

        self.frame(next_frame)
        
        del display_buffer
        
    def _chunk(self, l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i + n]
                

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
