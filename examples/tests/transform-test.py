#!/usr/bin/env python

import time
import signal
import math
import argparse

import scrollphathd
from scrollphathd.fonts import font3x5

print("""
Scroll pHAT HD: Transformation Test

Shows a message with arbitrary transformations specified
on the command line. See --help.

Press Ctrl+C to exit!

""")


parser = argparse.ArgumentParser(description='Scroll Hat HD transformation test.')

parser.add_argument('-r', '--rotate', metavar='DEGREES', type=int, help='Rotate the display.', default=0)
parser.add_argument('-x', '--flip-x', help='Flip in the X axis.', action='store_true')
parser.add_argument('-y', '--flip-y', help='Flip in the Y axis.', action='store_true')
parser.add_argument('-s', '--scroll-x', metavar='PIXELS', type=int, help='Scroll in the X axis.', default=0)
parser.add_argument('-t', '--scroll-y', metavar='PIXELS', type=int, help='Scroll in the Y axis.', default=0)
parser.add_argument('-m', '--message', metavar='MESSAGE', type=str, help='Message to display.', default='Does it work? ')

args = parser.parse_args()

scrollphathd.set_brightness(0.5)
scrollphathd.clear()
scrollphathd.write_string(args.message, x=0, y=0, font=font3x5, brightness=0.5)


while True:

    scrollphathd.flip(args.flip_x, args.flip_y)
    scrollphathd.rotate(args.rotate)
    scrollphathd.scroll(args.scroll_x, args.scroll_y)
    scrollphathd.show()
    time.sleep(0.1)
