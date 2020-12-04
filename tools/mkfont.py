#!/usr/bin/env python

import os
import sys
import argparse
import numpy

try:
    from PIL import Image
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

parser = argparse.ArgumentParser(description='Process bitmap into scroll-phat-hd font')
parser.add_argument('file', help='image file to read')
parser.add_argument('-sz','--sheetsize', dest='sheetsize', default=[16,16], nargs='+', type=int,
                           help='sheet size (columns,rows) in characters (default: 16,16)')
parser.add_argument('-fz','--fontsize', dest='fontsize', default=[5,7], nargs='+', type=int,
                           help='font size (x,y) in pixels (default: 5,7)')
parser.add_argument('-s','--spacing', dest='spacing', default=[1,1], nargs='+', type=int,
                           help='pixel gap (x,y) between characters (default: 1,1)')
parser.add_argument('-m','--margin', dest='margin', default=[0,0], nargs='+', type=int,
                           help='pixel gap (x,y) from top left of sheet (default: 0,0)')
parser.add_argument('-vert','--vertical', dest='vertical', action='store_true',
                           help='characters are vertical in sheet')
parser.add_argument('-c','--characters', dest='charset', default='', type=str,
                           help='character set in the sheet (default: all 0-255)')
if len(sys.argv)<2:
    parser.print_usage(sys.stderr)
    sys.exit(1)
args = parser.parse_args()

FONT_FILE = args.file
(SHEET_WIDTH, SHEET_HEIGHT) = args.sheetsize
(FONT_WIDTH, FONT_HEIGHT) = args.fontsize
(MARGIN_X, MARGIN_Y) = args.margin
(CHAR_SPACING_X, CHAR_SPACING_Y) = args.spacing
CHAR_SET = []
if not args.charset:
    for i in range(0,256):
        CHAR_SET.append(i)
else:
    lc = ''
    for c in args.charset:
        if c != '\\' or lc == '\\':
            CHAR_SET.append( ord(c) )
        lc = c

    

def get_char_position(char):
    """Get the x/y position of the char"""
    i = CHAR_SET.index(char)
    if args.vertical:
        y = i % SHEET_HEIGHT
        x = i // SHEET_HEIGHT
    else:
        x = i % SHEET_WIDTH
        y = i // SHEET_WIDTH
    return (x, y)


def get_char_coords(x, y):
    """Get the x/y position of the char in pixels"""

    x = MARGIN_X + (x * (FONT_WIDTH + CHAR_SPACING_X))
    y = MARGIN_Y + (y * (FONT_HEIGHT + CHAR_SPACING_Y))

    return (x, y)


def get_color(font_image, color):
    offset = color * 3
    r, g, b = font_image.getpalette()[offset:offset+3]

    return 255 - max(r, g, b)


def get_char_data(font_image, o_x, o_y):
    char = [[0 for x in range(FONT_WIDTH)] for y in range(FONT_HEIGHT)]

    for x in range(FONT_WIDTH):
        for y in range(FONT_HEIGHT):
            try:
                palette_index = font_image.getpixel((o_x + x, o_y + y))
            except:
                raise IndexError("Invalid coordinates: {}:{}".format(o_x+x, o_y+y))
            color = get_color(font_image, palette_index)
            char[y][x] = color

    return numpy.array(char)


def load_font(font_file):
    font = {}

    font_path = os.path.join(os.path.dirname(__file__), font_file)
    font_image = Image.open(font_path)
    font_image = font_image.convert("P", palette=Image.ADAPTIVE, colors=256)

    for char in CHAR_SET:
        x, y = get_char_position(char)
        px, py = get_char_coords(x, y)
        font[ char ] = get_char_data(font_image, px, py)

    return font


def kern_font(font):
    for char, data in font.iteritems():
        badcols = [x == 0 for x in numpy.sum(data, axis=0)]

        if False in badcols:
            try:
                while badcols.pop(0):
                    data = numpy.delete(data, 0, axis=1)
            except IndexError:
                pass

            try:
                while badcols.pop(-1):
                    data = numpy.delete(data, -1, axis=1)
            except IndexError:
                pass

        badrows = [x == 0 for x in numpy.sum(data, axis=1)]

        if False in badrows:
            try:
                while badrows.pop(-1):
                    data = numpy.delete(data, -1, axis=0)
            except IndexError:
                pass

        font[char] = data

    return font


if __name__ == "__main__":
    font = kern_font(load_font(FONT_FILE))

    numpy.set_printoptions(formatter={'int': lambda x: "0x{:02x}".format(x)})

    print("data = {")
    for key, value in font.iteritems():
        print("0x{key:08x}: {value},\n".format(key=key, value=numpy.array2string(
            value,
            separator=',',
            prefix=' ' * 12
        )))
    print("}")
    print("width = {}".format(FONT_WIDTH))
    print("height = {}".format(FONT_HEIGHT))
    sys.exit()

    for char in range(CHAR_START, CHAR_END+1):
        for row in font[char]:
            r = ''
            for col in row:
                if col > 0:
                    r += '#'
                else:
                    r += ' '
            print(r)
        print("")
        print("-" * FONT_WIDTH)
        print("")
    # print("font = " + str(font))
