#!/usr/bin/env python
import os
import sys
import time
import scrollphat

#-----------------------------------------------------------------------------
# This example uses a custome font set, read from
# the image file my-font, which has the lower-case
# letters replaced with symbols.
# For example:
#   a - tick
#   b - cross
#   f - flag
#   h - love heart 
#   j - smiley face
#   u,d,l,r - arrows (up down left and right respectively)
#-------------------------------------------------------------------------------

try:
    from PIL import Image
except ImportError:
    exit("This script requires the pillow module\nInstall with: sudo pip install pillow")

#-----------------------------------------------------------------------------
# This funtion will read the supplied image
# and convert it into font data for Scoll pHAT.
# The expect format of the image is as follows:
# Each font image contains a 16 x 6 table of squares,
# one for each ASCII character, starting with a space (0x20) and
#  incrementing from left to right. Each square is 6x6 box
# boarding the 5x5 image of the individual characters.
def convert_png2font(font_file):

    font = {}
    font_path = os.path.join(os.path.dirname(__file__), font_file)
    font_image = Image.open(font_path)

    char = 0x20
    gridsize_x = 16
    gridsize_y = 6
    border = 1
    for char_y in range(0, gridsize_y):
        for char_x in range(0, gridsize_x):
            char_bits = []
            for x in range(0, 5):
                bits = 0
                for y in range(0, 5):
                     pixel=font_image.getpixel((border+(char_x * 6) + x , border+(char_y * 6) + y )) 
                     if pixel == 1:
                        bits |= (1 << y)
                char_bits.append(bits)

            # remove all "empty" columns from the right of the character
            while len(char_bits) > 0 and char_bits[-1] == 0:
                char_bits.pop()

            font[char] = char_bits

            char += 1
    return font
#-----------------------------------------------------------------------------


#-----------------------------------------------------------------------------
# Main program block
#-----------------------------------------------------------------------------
scrollphat.set_brightness(2)
scrollphat.set_rotate(True)
scrollphat.load_font(convert_png2font('my-font.png'))

if len(sys.argv) != 2:
    print("\nUsage: python scroll-text-in-my-font.py \"MESSAGE\" " )
    print ("press CTRL-C to exit\n")
    print("In this example the lettters are read from the \"my-font.png\" file,")
    print("where lower-case letters are replaced with fun symbols and icons.")    
    sys.exit(0)

scrollphat.write_string(sys.argv[1], 11)

while True:
    try:
        scrollphat.scroll()
        time.sleep(0.1)
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)
