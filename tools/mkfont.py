import os
import sys
import numpy

try:
    from PIL import Image
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

FONT_FILE = "5x7-font.png"

SHEET_WIDTH = 16
SHEET_HEIGHT = 16

FONT_WIDTH = 5
FONT_HEIGHT = 7

CHAR_SPACING_X = 2
CHAR_SPACING_Y = 2
MARGIN_X = 2
MARGIN_Y = 2

CHAR_START = 0x00
CHAR_END = 0xff


def get_char_position(char):
    """Get the x/y position of the char"""

    x = char % SHEET_WIDTH
    y = char // SHEET_WIDTH

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
            palette_index = font_image.getpixel((o_x + x, o_y + y))
            color = get_color(font_image, palette_index)
            char[y][x] = color

    return numpy.array(char)


def load_font(font_file):
    font = {}

    font_path = os.path.join(os.path.dirname(__file__), font_file)
    font_image = Image.open(font_path)

    for char in range(CHAR_START, CHAR_END+1):
        x, y = get_char_position(char)
        px, py = get_char_coords(x, y)
        font[char] = get_char_data(font_image, px, py)

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
