#!/usr/bin/env python

# simple binary clock
# bcd for hours, minutes and seconds
# chart for time past the hour (one light per whole ten minutes)
# please see disclaimer at bottom of file

import sys
import time

import scrollphat


def string_to_bcd(digit):

    bcd_digit = bin(int(digit))[2:]
    return ('00000' + bcd_digit)[-5:]


def plot_digit(digit, position):

    bcd_digit = string_to_bcd(digit)
    for y in range(0, 5, 1):
        scrollphat.set_pixel(position, y, int(bcd_digit[y]) == 1)

while True:
    try:
        current = time.strftime('%H0%M0%S')
        for x in range(0, 8):
            plot_digit(current[x], x)
        for i in range(0, 5):
            scrollphat.set_pixel(10, i, (5 - i) <= ((int(current[3:5])) / 10))
        scrollphat.update()
        time.sleep(0.5)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)


# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.
