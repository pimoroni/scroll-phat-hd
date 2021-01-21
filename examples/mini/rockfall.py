#!/usr/bin/env python3
"""
Little game for the Scroll HAT Mini.
"""

import math
import scrollphathd
import time

from gpiozero import Button
from random import random, shuffle

# ------------------------------------------------------------

print("""Scroll HAT Mini: rockfall.py

Dodge the falling rocks using the X and Y buttons on the HAT.

The A and B buttons make it easier or harder.

Press Ctrl+C to exit!

""")


scrollphathd.set_brightness(0.4)


class Rockfall():
    """
    Main game class.
    """
    # The extents of the screen
    WIDTH = scrollphathd.DISPLAY_WIDTH
    HEIGHT = scrollphathd.DISPLAY_HEIGHT

    # THe istarting wait time between ticks
    WAIT = 0.5

    # How much to change the wait time by each tick
    WAIT_DIFF = 0.001

    # The min and max population fractions, and how much the butttons change
    # it by
    MIN_FRAC = 1.0 / HEIGHT
    MAX_FRAC = 4.0 / HEIGHT
    FRAC_STEP = 1.0 / HEIGHT

    def __init__(self):
        # Set up the buttons
        self._button_A = Button(5)
        self._button_B = Button(6)
        self._button_X = Button(16)
        self._button_Y = Button(24)

        # How easy or hard
        self._frac_new = self.MIN_FRAC

        # The wait time between tocks
        self._wait = self.WAIT

        # The game area as a boolean bitmap. A True means there is a rock in an
        # entry. This is stored as a tuple of rows.
        self._arena = tuple([[False] * (self.WIDTH)
                             for i in range(self.HEIGHT)])

        # The player's position, at the end of the display
        self._hpos = self.HEIGHT // 2
        self._wpos = self.WIDTH - 3

    # ------------------------------------------------------------

    def init(self):
        """
        Reset the state to start of game.
        """
        for row in self._arena:
            for i in range(len(row)):
                row[i] = False
        self._hpos = self.HEIGHT // 2
        self._wait = self.WAIT

    def step(self):
        # Scroll the current values along by one
        for row in self._arena:
            row[1:] = row[:-1]
            row[0] = False

        # This fraction new, an interval between the minimum and the
        # difficulty value
        frac_new = max(self.MIN_FRAC, self._frac_new * random())

        # Add new ones at random indices
        indices = list(range(len(self._arena)))
        shuffle(indices)
        end = round(min(1, max(0, frac_new)) * len(indices))
        for index in indices[:int(end)]:
            self._arena[index][0] = True

    def explode(self):
        for r in range(int(self.WIDTH * 1.25)):
            for s in range(r):
                c = 1 + int(math.pi * 2 * r)
                for a in range(c):
                    o = 2 * math.pi / c * a
                    x = int(math.sin(o) * s + self.WIDTH - 1)
                    y = int(math.cos(o) * s + self._hpos)
                    v = s / r * (0.2 + 0.8 * random())
                    if 0 <= x < self.WIDTH and 0 <= y <= self.HEIGHT:
                        scrollphathd.pixel(x, y, v)
            scrollphathd.show()
            time.sleep(0.01)

    def run(self):
        """
        The main running loop.
        """

        # State variables
        self.init()
        last = time.time()
        start = last

        # Set things to the starting values

        # Loop forever now
        while True:
            now = time.time()
            since = now - last

            # Move the things down
            if since > self._wait:
                self.step()
                last = now
                self._wait = max(0.0, self._wait - self.WAIT_DIFF)

            # Make it easier or harder
            if self._button_A.is_active:
                self._frac_new = max(self.MIN_FRAC,
                                     self._frac_new - self.FRAC_STEP)
            if self._button_B.is_active:
                self._frac_new = min(self.MAX_FRAC,
                                     self._frac_new + self.FRAC_STEP)

            # Move the player
            if self._button_X.is_active and self._hpos > 0:
                self._hpos -= 1
            if self._button_Y.is_active and self._hpos < self.HEIGHT-1:
                self._hpos += 1

            # Draw the field
            for (y, row) in enumerate(self._arena):
                for (x, e) in enumerate(row):
                    v = 0.5 if e else 0.0
                    scrollphathd.pixel(x, y, v)

            # Draw the player
            scrollphathd.pixel(self._wpos, self._hpos, 1.0)

            # And display it all
            scrollphathd.show()

            # Collision?
            if self._arena[self._hpos][self._wpos]:
                # Print stats
                print("You survived for %0.1f seconds" % (now - start))
                print()

                # Draw the explosion
                self.explode()

                # And reset things
                self.init()
                start = now
                last = now

            # Wait for  bit befor emoving on
            time.sleep(0.05)

# ----------------------------------------------------------------------


if __name__ == "__main__":
    game = Rockfall()
    game.run()
