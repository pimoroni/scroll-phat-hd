#!/usr/bin/env python

import signal
import time

import pigpio
import scrollphathd

print("""
Scroll pHAT HD: Hello World

Scrolls "Hello World" across the screen
using the default 5x7 pixel large font.

Press Ctrl+C to exit!

""")

class I2C_PIGPIO():
    def __init__(self):
        self.pi = pigpio.pi()
        self.i2c_handle = self.pi.i2c_open(1, 0x74)

    def write_byte_data(self, address, register, value):
        self.pi.i2c_write_byte_data(self.i2c_handle, register, value)

    def read_byte_data(self, address, register):
        return self.pi.i2c_read_byte_data(self.i2c_handle, register)

    def write_i2c_block_data(self, address, register, values):
        self.pi.i2c_write_i2c_block_data(self.i2c_handle, register, values)


scrollphathd.setup(i2c_dev=I2C_PIGPIO())
# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
#scrollphathd.rotate(degrees=180)

# Write the "Hello World!" string in the buffer and
#   set a more eye-friendly default brightness
scrollphathd.write_string(" Hello World!", brightness=0.5)

# Auto scroll using a while + time mechanism (no thread)
while True:
    # Show the buffer
    scrollphathd.show()
    # Scroll the buffer content
    scrollphathd.scroll()
    # Wait for 0.1s
    time.sleep(0.1)
