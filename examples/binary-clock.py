#!/usr/bin/env python
#
# binary_clock.py - A Python implementation of a binary clock
# for the Pimoroni Scroll Bot.
# Copyright (C) 2018 Freddy Spierenburg
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA 02110-1301 USA

import scrollphathd
import datetime
import math
import random


class Time(object):
    def __init__(self):
        self.update()

    def hour(self):
        return self._now.hour

    def minute(self):
        return self._now.minute

    def second(self):
        return self._now.second

    def update(self):
        self._now = datetime.datetime.now()


class Clock(Time):
    def __init__(self):
        Time.__init__(self)

    def _hour(self):
        print self.hour()

    def _minute(self):
        print self.minute()

    def _second(self):
        print self.second()

    def draw(self):
        self._hour()
        self._minute()
        self._second()


class BinaryClock(Clock):
    def __init__(self):
        self._SPHD = ScrollPhatHD()
        self._max_degree = 45
        self._hand_position = [2, 4, 7, 9, 12, 14]
        self._hand_bits = 4
        self._last_minute = None
        self._max_intensity = 0.7
        Clock.__init__(self)

    def _draw_binary(self, x, value):
        for y in range(self._hand_bits):
            self._SPHD.set_pixel(
                x,
                ((self._hand_bits - 1 - y) * 2),
                1 if value & (1 << y) > 0 else self._brightness[x][y])

    def _draw_hand(self, x_left, x_right, value):
        self._draw_binary(x_left, value / 10)
        self._draw_binary(x_right, value % 10)

    def _hour(self):
        self._draw_hand(self._hand_position[0],
                        self._hand_position[1],
                        self.hour())

    def _minute(self):
        self._draw_hand(self._hand_position[2],
                        self._hand_position[3],
                        self.minute())

    def _second(self):
        self._draw_hand(self._hand_position[4],
                        self._hand_position[5],
                        self.second())

    def draw(self):
        Clock.draw(self)
        self._SPHD.show()

    def _intensities_init(self, max_intensity):
        self._intensities = {
            hand_position: [
                self._intensity(int(random.uniform(-self._max_degree, self._max_degree)), max_intensity) for hand_bit in range(self._hand_bits)
            ] for hand_position in self._hand_position
        }

    def _brightness_step(self):
        self._brightness = {
            hand_position: [
                next(self._intensities[hand_position][hand_bit]) for hand_bit in range(self._hand_bits)
            ] for hand_position in self._intensities.keys()
        }

    def _intensity(self, start_degree, max_intensity):
        degrees = range(self._max_degree) + list(reversed(range(self._max_degree)))
        if start_degree < 0:
            start_degree = self._max_degree * 2 + max(start_degree, -self._max_degree)
        while True:
            for degree in degrees[start_degree::]:
                yield math.tan(math.radians(degree)) * max_intensity
            start_degree = 0

    def update(self):
        Clock.update(self)
        if self._last_minute != self.minute():
            self._intensities_init(self._max_intensity)
            self._last_minute = self.minute()
        self._brightness_step()


class ScrollPhatHD(object):
    def __init__(self):
        scrollphathd.rotate(180)
        scrollphathd.clear()
        self.show()

    def set_pixel(self, x, y, brightness):
        scrollphathd.set_pixel(x, y, brightness)

    def show(self):
        scrollphathd.show()


def main():
    clock = BinaryClock()
    while True:
        clock.update()
        clock.draw()


if __name__ == '__main__':
    main()
