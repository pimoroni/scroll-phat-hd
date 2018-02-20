#!/usr/bin/env python

import argparse
import random
import time

import scrollphathd


def generate_lightning(intensity):
    """Generate a lightning bolt"""
    if random.random() < intensity:
        x = random.randint(0, width-1)
        
        # generate a random crooked path from top to bottom,
        # making sure to not go off the sides
        for y in xrange(0, height):
            if y > 1 and y < height - 1:
                branch = random.random()
                if branch < .3:
                    x -= 1
                    if x <= 0:
                        x = 0
                elif branch > .6:
                    x += 1
                    if x >= width-1:
                        x = width-1

            # generate a wider flash around the bolt itself
            wide = [int(x-(width/2)), int(x+(width/2))]
            med = [int(x-(width/4)), int(x+(width/4))]
            small = [x-1, x+1]

            for val in [wide, med, small]:
                if val[0] < 0:
                    val[0] = 0
                if val[1] > width - 1:
                    val[1] = width - 1

            for flash in [[wide, .1], [med, .2], [small, .4]]:
                scrollphathd.fill(
                    flash[1],
                    x=flash[0][0],
                    y=y,
                    width=flash[0][1]-flash[0][0]+1,
                    height=1
                )

            scrollphathd.set_pixel(x, y, brightness=1)

            scrollphathd.show()
        scrollphathd.clear()


def new_drop(pixels, values):
    """Generate a new particle at the top of the board"""
    
    # First, get a list of columns that haven't generated
    # a particle recently
    cols = []
    for x in xrange(0, width):
        good_col = True
        for y in xrange(0, int(height*values['safe'])):
            if pixels[x][y] == values['brightness']:
                good_col = False
        if good_col is True:
            cols.append(x)

    # Then pick a random value from this list,
    # test a random number against the amount variable,
    # and generate a new particle in that column.
    # Then remove it from the list.
    # Do this as many times as required by the intensity variable
    if len(cols) > 0:
        random.shuffle(cols)
        cols_left = values['intensity']
        while len(cols) > 0 and cols_left > 0:
            if random.random() <= values['amount']:
                pixels[cols.pop()][0] = values['brightness'] + values['fade']
            cols_left -= 1


def fade_pixels(pixel_array, fade):
    """Fade all the lit particles on the board by the fade variable"""
    for x in xrange(0, width):
        for y in xrange(0, height):
            if pixel_array[x][y] > 0:
                pixel_array[x][y] -= fade
                pixel_array[x][y] = round(pixel_array[x][y], 2)
            if pixel_array[x][y] < 0:
                pixel_array[x][y] = 0
    return pixel_array


def update_pixels(pixels, values):
    """Update the board by lighting new pixels as they fall"""
    for x in xrange(0, width):
        for y in xrange(0, height-1):
            if pixels[x][y] == values['brightness']:
                pixels[x][y+1] = values['brightness'] + values['fade']

    fade_pixels(pixels, values['fade'])

    x = xrange(width)
    y = xrange(height)
    [[[scrollphathd.set_pixel(a, b, pixels[a][b])] for a in x] for b in y]

    for a in xrange(0, len(pixels)):
        for b in xrange(0, len(pixels[a])):
            scrollphathd.set_pixel(a, b, pixels[a][b])

    scrollphathd.show()

# Command line argument parsing functions
def msg(name=None):
    return '''precip.py [options...]
        '''


def setup_parser():

    parser = argparse.ArgumentParser(
        description='Generate precipitation; CTRL+C to exit',
        usage=msg(),
        argument_default=argparse.SUPPRESS
        )
    parser.add_argument(
        "-a",
        "--amount",
        help="Chance of generating a new particle in each possible column "
        "(0 to 1)",
        type=float
    )
    parser.add_argument(
        "-b",
        "--brightness",
        help="Initial brightness of a particle (0 to 1)",
        type=float
    )
    parser.add_argument(
        "-d",
        "--delay",
        help="Delay between steps (0 and up, in seconds)",
        type=float
    )
    parser.add_argument(
        "-f",
        "--fade",
        help="How quickly a particle fades; determines how long the tail is"
        " (0 to 1)",
        type=float
    )
    parser.add_argument(
        "-i",
        "--intensity",
        help="How many columns have the chance "
        "to generate a new particle each tick (0 to width, integer)",
        type=int
    )
    parser.add_argument(
        "-l",
        "--lightning",
        help="Chance of lightning on each tick (0 to 1)",
        type=float
    )
    parser.add_argument(
        "-q",
        "--quiet",
        help="Suppress output",
        action="store_false"
    )
    parser.add_argument(
        "-r",
        "--rotate",
        help="Rotate the board",
        default=0,
        choices=[
            0,
            90,
            180,
            270
        ],
        type=int
        )
    parser.add_argument(
        "-s",
        "--safe",
        help="How far down a column a particle must get "
        "before a new particle can be generated in that column "
        "(0 to 1, fraction of the column)",
        type=float
        )
    parser.add_argument(
        "-t",
        "--type",
        help="Type of precipitation. Sets a preset for all conditions; "
        "will be overridden by any specified conditions.",
        default="thunderstorm",
        choices=[
            "rain",
            "heavy rain",
            "snow",
            "heavy snow",
            "thunderstorm"
        ]
    )

    return parser

if __name__ == '__main__':

    # Set up command line argument parsing
    parser = setup_parser()
    args = parser.parse_args()
    arguments = vars(args)

    scrollphathd.set_clear_on_exit()
    scrollphathd.set_brightness(1)

    # Board rotation
    scrollphathd.rotate(arguments.get('rotate'))

    width = scrollphathd.get_shape()[0]
    height = scrollphathd.get_shape()[1]

    presets = {
        "thunderstorm": {
            "amount": .7,
            "brightness": .15,
            "delay": 0,
            "fade": .05,
            "intensity": 1,
            "lightning": .01,
            "safe": .3
        },
        "rain": {
            "amount": .7,
            "brightness": .15,
            "delay": 0,
            "fade": .05,
            "intensity": 1,
            "lightning": 0,
            "safe": .3
        },
        "heavy rain": {
            "amount": .7,
            "brightness": .15,
            "delay": 0,
            "fade": .05,
            "intensity": 4,
            "lightning": 0,
            "safe": .3
        },
        "snow": {
            "amount": .2,
            "brightness": .4,
            "delay": .25,
            "fade": .4,
            "intensity": 2,
            "lightning": 0,
            "safe": .3
        },
        "heavy snow": {
            "amount": .3,
            "brightness": .4,
            "delay": .25,
            "fade": .4,
            "intensity": 4,
            "lightning": 0,
            "safe": .3
        }
    }

    values = {}

    conditions = [
        'amount',
        'brightness',
        'delay',
        'fade',
        'intensity',
        'lightning',
        'safe'
    ]

    # Set initial values from arguments or preset
    for condition in conditions:
        values[condition] = arguments.get(
            condition,
            presets[arguments['type']][condition]
        )

    # Set up initial pixel matrix
    pixels = []

    for x in xrange(width):
        pixels.append([])
        for y in xrange(height):
            pixels[x].append(0)

    # Print conditions
    if arguments.get('quiet') is not False:
        print("Current conditions:")
        for condition in conditions:
            print("{}: {}".format(condition, values[condition]))

    # Run display loop
    while True:
        if values['lightning'] > 0:
            generate_lightning(values['lightning'])
        new_drop(pixels, values)
        update_pixels(pixels, values)
        time.sleep(values['delay'])