"""IS31FL3731 144 LED Matrix Driver."""
import time

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

_NUM_PIXELS = 144
_NUM_FRAMES = 8


class IS31FL3731:
    """Class representing the IS31FL3731 matrix driver."""

    def __init__(self, i2c=None, address=0x74):
        """Initialise the IS31FL3731.

        :param i2c: smbus-compatible i2c object
        :param address: 7-bit i2c address of attached IS31FL3731

        """
        self.i2c = i2c
        self.address = address
        self.clear()

        if self.i2c is not None:
            for attr in ('read_byte_data', 'write_byte_data', 'write_i2c_block_data'):
                if not hasattr(self.i2c, attr):
                    raise RuntimeError('i2c transport must implement: "{}"'.format(attr))

        if self.i2c is None:
            try:
                import smbus
                self.i2c = smbus.SMBus(1)
            except ImportError as e:
                raise ImportError('You must supply an i2c device or install the smbus library.')
            except IOError as e:
                if hasattr(e, 'errno') and e.errno == 2:
                    e.strerror += "\n\nMake sure you've enabled i2c in your Raspberry Pi configuration.\n"
                raise e

        try:
            self.reset()
        except IOError as e:
            if hasattr(e, 'errno') and e.errno == 5:
                e.strerror += '\n\nMake sure your Scroll pHAT HD is attached, and double-check your soldering.\n'
            raise e

        for frame in reversed(range(_NUM_FRAMES)):
            self.update_frame(frame)
            self.show_frame(frame)

        self.set_mode(_PICTURE_MODE)
        self.set_audiosync(False)

    def set_mode(self, mode):
        """Set display mode."""
        if mode not in [_PICTURE_MODE, _AUTOPLAY_MODE, _AUDIOPLAY_MODE]:
            raise ValueError('Mode "{}" Unsupported'.format(mode))

        self._i2c_write(_MODE_REGISTER, mode, bank=_CONFIG_BANK)

    def set_audiosync(self, state):
        """Set Audio Sync mode."""
        self._i2c_write(_AUDIOSYNC_REGISTER, state, bank=_CONFIG_BANK)

    def enable_leds(self, frame, enable_pattern):
        """Enable LEDs."""
        self.set_bank(frame)
        self.i2c.write_i2c_block_data(self.address, 0x00, enable_pattern)

    def clear(self):
        """Clear the buffer.

        You must call `show` after clearing the buffer to update the display.

        """
        self._buf = [[0 for x in range(_NUM_PIXELS)] for y in range(_NUM_FRAMES)]

    def set_pixel(self, frame, index, brightness):
        """Set a single pixel in the buffer.

        :param x: Position of pixel from 0 to 143
        :param brightness: Intensity of the pixel, from 0 to 255.


        """
        if brightness > 255 or brightness < 0:
            raise ValueError('Value {} out of range. Brightness must be between 0 and 255'.format(brightness))

        if index < 0 or index > 143:
            raise ValueError('Index must be between 0 and 143')

        self._buf[frame][index] = brightness

    def set_frame(self, frame, values):
        """Set the entire display buffer for a frame."""
        self._buf[frame] = values

    def update_frame(self, frame):
        """Show the buffer contents on the display."""
        self.set_bank(frame)
        offset = 0
        for chunk in self._chunk(self._buf[frame], 32):
            self.i2c.write_i2c_block_data(self.address, _COLOR_OFFSET + offset, chunk)
            offset += 32

    def reset(self):
        """Reset the IS31FL3731."""
        self.sleep(True)
        time.sleep(0.00001)
        self.sleep(False)

    def sleep(self, value):
        """Put the IS31FL3731 into sleep mode."""
        return self._i2c_write(_SHUTDOWN_REGISTER, not value, bank=_CONFIG_BANK)

    def show_frame(self, frame):
        """Switch to showing a specific frame.

        :param frame: Frame to show


        """
        self._i2c_write(_FRAME_REGISTER, frame, bank=_CONFIG_BANK)

    def set_bank(self, bank):
        """Set the current memory bank/frame."""
        self._i2c_write(_BANK_ADDRESS, bank)

    def get_bank(self):
        """Get the current memory bank/frame."""
        return self._i2c_read(_BANK_ADDRESS)

    def _i2c_write(self, register, value, bank=None):
        """Write a byte to an i2c register."""
        if bank is not None:
            self.set_bank(bank)
        self.i2c.write_byte_data(self.address, register, value)

    def _i2c_read(self, register, bank=None):
        """Read a byte from an i2c register."""
        if bank is not None:
            self.set_bank(bank)
        return self.i2c.read_byte_data(self.address, register)

    def _chunk(self, l, n):
        """Split a list of values in to chunks of length n."""
        for i in range(0, len(l) + 1, n):
            yield l[i:i + n]
