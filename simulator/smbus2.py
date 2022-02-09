import sys
import subprocess
import pickle
import os


class SMBus:
    def __init__(self, dummy):
        self._start_simulator()
        self.pixels = [0 for x in range(144)]

    def _start_simulator(self):
        self.sdl_phat_process = subprocess.Popen(
            [sys.executable, os.path.dirname(os.path.abspath(
                __file__)) + '/scroll_phat_simulator.py'],
            stdin=subprocess.PIPE)

    def write_byte_data(self, addr, reg, data):
        pass

    def write_i2c_block_data(self, addr, cmd, vals):
        I2C_ADDR = 0x74

        assert addr == I2C_ADDR

        if cmd < 0x24:  # Start of pixel data
            return

        offset = cmd - 0x24

        self.pixels[offset:offset + len(vals)] = vals

        try:
            pickle.dump(self.pixels, self.sdl_phat_process.stdin)
            self.sdl_phat_process.stdin.flush()
        except OSError:
            print('lost connection with scroll pHAT simulator')
            sys.exit(-1)
