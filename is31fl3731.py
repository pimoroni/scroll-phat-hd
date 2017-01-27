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

    def init(self):
        # Switch to configuration bank
        self._bank(_CONFIG_BANK)
        
        # Switch to Picture Mode
        self.i2c.write_i2c_block_data(self.address, _MODE_REGISTER, [_PICTURE_MODE])
        
        # Disable audio sync
        self.i2c.write_i2c_block_data(self.address, _AUDIOSYNC_REGISTER, [0])
        
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

    def autoplay(self, delay=0, loops=0, frames=0):
        if delay == 0:
            self._mode(_PICTURE_MODE)
            return

        delay //= 11

        if not 0 <= loops <= 7:
            raise ValueError("Loops out of range")

        if not 0 <= frames <= 7:
            raise ValueError("Frames out of range")

        if not 1 <= delay <= 64:
            raise ValueError("Delay out of range")

        self._register(_CONFIG_BANK, _AUTOPLAY1_REGISTER, loops << 4 | frames)
        self._register(_CONFIG_BANK, _AUTOPLAY2_REGISTER, delay % 64)
        self._mode(_AUTOPLAY_MODE | self._frame)

    def fade(self, fade_in=None, fade_out=None, pause=0):
        if fade_in is None and fade_out is None:
            self._register(_CONFIG_BANK, _BREATH2_REGISTER, 0)

        elif fade_in is None:
            fade_in = fade_out

        elif fade_out is None:
            fade_out = fade_in

        fade_in = int(math.log(fade_in / 26, 2))
        fade_out = int(math.log(fade_out / 26, 2))
        pause = int(math.log(pause / 26, 2))

        if not 0 <= fade_in <= 7:
            raise ValueError("Fade in out of range: 0-7")

        if not 0 <= fade_out <= 7:
            raise ValueError("Fade out out of range: 0-7")

        if not 0 <= pause <= 7:
            raise ValueError("Pause out of range: 0-7")

        self._register(_CONFIG_BANK, _BREATH1_REGISTER, fade_out << 4 | fade_in)
        self._register(_CONFIG_BANK, _BREATH2_REGISTER, 1 << 4 | pause)

    def frame(self, frame=None, show=True):
        if frame is None:
            return self._frame

        if not 0 <= frame <= 8:
            raise ValueError("Frame out of range: 0-8")

        self._frame = frame
        if show:
            self._register(_CONFIG_BANK, _FRAME_REGISTER, frame);

    def blink(self, rate=None):
        if rate is None:
            return (self._register(_CONFIG_BANK, _BLINK_REGISTER) & 0x07) * 270

        elif rate == 0:
            self._register(_CONFIG_BANK, _BLINK_REGISTER, 0x00)
            return

        rate //= 270
        self._register(_CONFIG_BANK, _BLINK_REGISTER, rate & 0x07 | 0x08)

    def fill(self, color=None, blink=None, frame=None):
        if frame is None:
            frame = self._frame

        self._bank(frame)
        
        if color is not None:
            if not 0 <= color <= 255:
                raise ValueError("Color out of range: 0-255")

            data = [color] * 24

            for row in range(6):
                #print data

                self.i2c.write_i2c_block_data(self.address, _COLOR_OFFSET + row * 24, data)

        if blink is not None:
            data = bool(blink) * 0xff
            for col in range(18):
                self._register(frame, _BLINK_OFFSET + col, data)

    def _pixel_addr(self, x, y):
        return x + y * 16
        
    def pixel(self, x, y, brightness):
        try:
            self.buf[x][y] = brightness
        
        except IndexError:
            if y > self.buf.shape[1]:
                self.buf = numpy.pad(self.buf, ((0,0),(0,y - self.buf.shape[1] + 1)), mode='constant')
                
            if x > self.buf.shape[0]:
                self.buf = numpy.pad(self.buf, ((0,x - self.buf.shape[0] + 1),(0,0)), mode='constant')
                
            self.buf[x][y] = brightness
        
    def show(self):
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
                idx = self._pixel_addr(x, y)
                
                try:
                    output[idx] = int(display_buffer[x][y])
                    
                except IndexError:
                    output[idx] = 0

        offset = 0
        for chunk in self._chunk(output, 32):
            #print(chunk)
            self.i2c.write_i2c_block_data(self.address, _COLOR_OFFSET + offset, chunk)
            offset += 32
        
        del display_buffer
        
    def _chunk(self, l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i + n]
                

'''
    def pixel(self, x, y, color=None, blink=None, frame=None):
        if not 0 <= x <= self.width:
            return

        if not 0 <= y <= self.height:
            return

        pixel = self._pixel_addr(x, y)

        if color is None and blink is None:
            return self._register(self._frame, pixel)

        if frame is None:
            frame = self._frame

        if color is not None:
            if not 0 <= color <= 255:
                raise ValueError("Color out of range")

            self._register(frame, _COLOR_OFFSET + pixel, color)

        if blink is not None:
            addr, bit = divmod(pixel, 8)
            bits = self._register(frame, _BLINK_OFFSET + addr)

            if blink:
                bits |= 1 << bit
            else:
                bits &= ~(1 << bit)

            self._register(frame, _BLINK_OFFSET + addr, bits)
'''

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
