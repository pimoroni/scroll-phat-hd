#!/usr/bin/env python3

import time
import math
import random
import colorsys

from gpiozero import Button
import scrollphathd

print("""Scroll HAT Mini: simon.py

Simon Says game. Try to match the sequence of flashes
by pressing the AB/XY buttons on Scroll HAT Mini.

Press Ctrl+C to exit!

""")

# Set up Scroll HAT Mini.
scrollphathd.set_brightness(0.5)

# Digits as 3x5 pixel elements stored as 15bits
# MSB is top-left, each 5 bits are a column.
digits_5x3 = [
    0b111111000111111,  # 0
    0b100011111100001,  # 1
    0b101111010111101,  # 2
    0b101011010111111,  # 3
    0b111000010011111,  # 4
    0b111011010110111,  # 5
    0b111111010100111,  # 6
    0b100001000011111,  # 7
    0b111111010111111,  # 8
    0b111001010011111   # 9
]

R = 0
G = 1
B = 2
Y = 3


class Display():
    """Virtual Simon display class.

    This class wraps an output device (minicorn) and makes it behave like a display
    with four fixed colour lights (Red, Yellow, Blue and Green) and two 3x5 numeric digits.

    """
    def __init__(self, output_device):
        self._output = output_device
        self._width, self._height = self._output.get_shape()
        self._br_red = 0
        self._br_green = 0
        self._br_blue = 0
        self._br_yellow = 0
        self._level = 0
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.yellow = (255, 255, 0)
        self._digit_left = None
        self._digit_right = None
        self._digit_left_br = 1.0
        self._digit_right_br = 1.0
        self._digit_left_color = (128, 128, 128)
        self._digit_right_color = (128, 128, 128)

    def _draw_light(self, brightness, x, y, r, g, b):
        r, g, b = [int(c * brightness) for c in (r, g, b)]
        self._draw_rect(x, y, 3, 3, r, g, b)

    def _draw_rect(self, x, y, w, h, r, g, b):
        for ry in range(h):
            for rx in range(w):
                self._output.set_pixel(x + rx, y + ry, max((r, g, b)) / 255)

    def _draw_digit(self, digit, x, y, r, g, b):
        digit = digits_5x3[digit]
        cols = [
            (digit >> 10) & 0b11111,
            (digit >> 5) & 0b11111,
            (digit) & 0b11111
        ]
        for dx in range(3):
            col = cols[dx]
            for dy in range(5):
                if col & (1 << (4 - dy)):
                    self._output.set_pixel(x + dx, y + dy, max((r, g, b)) / 255)

    def clear(self):
        self._output.clear()

    def update(self):
        self._draw_light(self._br_red, 0, 0, *self.red)
        self._draw_light(self._br_blue, 0, self._height - 3, *self.green)
        self._draw_light(self._br_green, self._width - 3, 0, *self.blue)
        self._draw_light(self._br_yellow, self._width - 3, self._height - 3, *self.yellow)

        # Draw the current digts (score/level/lives, kinda)
        if self._digit_left is not None:
            r, g, b = [int(c * self._digit_left_br) for c in self._digit_left_color]
            self._draw_digit(self._digit_left, 5, 1, r, g, b)

        if self._digit_right is not None:
            r, g, b = [int(c * self._digit_right_br) for c in self._digit_right_color]
            self._draw_digit(self._digit_right, 9, 1, r, g, b)

        self._output.show()

    def set_light_brightness(self, red, green, blue, yellow):
        self._br_red = red
        self._br_green = green
        self._br_blue = blue
        self._br_yellow = yellow

    def set_digits(self, left, right):
        self._digit_left = left
        self._digit_right = right

    def set_digit_brightness(self, left, right):
        self._digit_left_br = left
        self._digit_right_br = right

    def set_digit_color(self, left, right):
        self._digit_left_color = left
        self._digit_right_color = right


class Game():
    def __init__(self, display, starting_lives=3, starting_level=0, mode='attract'):
        self._starting_lives = starting_lives
        self._starting_level = starting_level
        self._mode = mode
        self._display = display
        self._level = 0
        self._lives = 0
        self._sequence = []
        self._compare = []
        self._current_playback_step = 0
        self._current_mode_start = 0
        self._button_map = {'a': R, 'b': B, 'x': G, 'y': Y}

    def update(self):
        self._display.clear()
        getattr(self, "_{}".format(self._mode))(time.time())
        self._display.update()

    def _set_mode(self, mode):
        self._mode = mode
        self._current_mode_start = time.time()

    def _attract(self, time):
        """Mode: Attract.

        Pulses all the virtual lights and fades the numbers "51" ([si]mon) on the virtual digits.

        """
        self._display.set_digits(5, 1)
        self._display.set_light_brightness(
            self._pulse(time / 2),
            self._pulse((time + 0.25) / 2),
            self._pulse((time + 0.5) / 2),
            self._pulse((time + 0.75) / 2)
        )
        self._display.set_digit_brightness(
            self._pulse(time),
            self._pulse(time)
        )
        self._display.set_digit_color(
            self._hue(time / 10),
            self._hue(time / 10 + 1)
        )

    def _play_pattern(self, time):
        """Mode: Play Pattern.

        Steps through the current sequence and pulses each virtual light.

        Drops into "wait_for_input" mode when it's finished, this is
        determined by checking if the elapsed time is greater than the
        sequence length- since each "light" takes 1 second to pulse.

        """
        self._display_level((255, 0, 0))
        br = [0, 0, 0, 0]
        color = self._sequence[self._current_playback_step]
        br[color] = self._pulse(time - self._current_mode_start)
        self._display.set_light_brightness(*br)
        if time - self._current_mode_start > (self._current_playback_step + 1):
            self._current_playback_step += 1
        if self._current_playback_step >= len(self._sequence):
            self._current_playback_step = 0
            self._set_mode('wait_for_input')

    def _flash_lives(self, time):
        """Mode: Flash Lives.

        Flash the players lives count at them.

        Re-play the pattern if they have lives left, otherwise jump to "you_lose"

        """
        # To show the player that they've lost one life we flash
        # the lives count up in red.
        # We fake add one life to their count (which has been already deducted)
        # for half of the flash cycle, so they visibly see the count go down!
        fake_lives = self._lives
        if time - self._current_mode_start < 1.5:
            fake_lives += 1

        self._display.set_digits(int(fake_lives / 10), fake_lives % 10)
        self._display.set_digit_brightness(
            self._pulse(time),
            self._pulse(time)
        )
        self._display.set_digit_color((255, 0, 0), (255, 0, 0))
        # Flash lives for 3 seconds and then switch back to playing pattern
        if time - self._current_mode_start > 3.0:
            if self._lives > 0:
                self._set_mode('play_pattern')
            else:
                self._set_mode('you_lose')

    def _you_win(self, time):
        """Need a better win animation!"""
        self._display_level()
        self._display.set_light_brightness(
            self._pulse(time),
            self._pulse(time),
            self._pulse(time),
            self._pulse(time)
        )

    def _you_lose(self, time):
        """Flash the player's 0 lives at them in red!"""
        self._display.set_digits(0, 0)
        self._display.set_digit_brightness(
            self._pulse(time),
            self._pulse(time)
        )
        self._display.set_digit_color((255, 0, 0), (255, 0, 0))

        # Return back to attract mode after displaying losing zeros for 20s
        if time - self._current_mode_start > 20.0:
            self._set_mode('attract')

    def _wait_for_input(self, time):
        """Just display the current level and wait for the players input.

        This constantly checks the players input against the sequence,
        if it ever mismatches it deducts one life and switches to "flash_lives".

        A successful sequence match will call "next_level()"

        """
        self._display_level()
        if self._compare == self._sequence[:len(self._compare)]:
            if len(self._compare) == len(self._sequence):
                self.next_level()
        else:
            # Remove the last (incorrect) guess
            self._compare = []
            self._lives -= 1
            self._set_mode('flash_lives')

    def _display_level(self, color=(255, 255, 255)):
        """Helper to display the current level on the virtual digits."""
        self._display.set_digit_brightness(0.5, 0.5)
        self._display.set_digit_color(color, color)
        self._display.set_digits(
            int(self._level / 10.0),
            self._level % 10
        )

    def _pulse(self, time):
        """Helper to produce a sine wave with a period of 1sec"""
        return (math.sin(time * 2 * math.pi - (math.pi / 2)) + 1) / 2.0

    def _hue(self, h):
        """Helper to return an RGB colour from HSV"""
        return tuple([int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)])

    def start(self):
        """Start the game.

        Sets the level to the starting level and builds a long-enough sequence to begin.

        """
        self._lives = self._starting_lives
        self._level = self._starting_level
        self._compare = []
        self._sequence = [random.choice([R, G, B, Y])] * (self._level + 1)
        self._current_playback_step = 0
        self._set_mode('play_pattern')

    def next_level(self):
        """Proceed to the next level.

        Adds 1 to the current level and a new random item to the end of the sequence.

        Jumps to the win state if the level hits 100!

        """
        self._level += 1
        self._compare = []
        if self._level == 100:
            self._set_mode('you_win')
            return
        self._sequence += [random.choice([R, G, B, Y])]
        self._set_mode('play_pattern')

    def _handle_choice(self, button):
        """Handle a specific choice."""
        self._compare += [self._button_map[button]]

    def _handle_generic_input(self):
        """Handle user input that's not button-specific.

        This function should be called for any button if it has not otherwise been handled.

        It's responsible for starting the game, mostly.

        """
        if self._mode in ('attract', 'you_lose', 'you_win'):
            self.start()

    def button_a(self):
        if self._mode == 'wait_for_input':
            self._handle_choice('a')
            return
        self._handle_generic_input()

    def button_b(self):
        if self._mode == 'wait_for_input':
            self._handle_choice('b')
            return
        self._handle_generic_input()

    def button_x(self):
        if self._mode == 'wait_for_input':
            self._handle_choice('x')
            return
        self._handle_generic_input()

    def button_y(self):
        if self._mode == 'wait_for_input':
            self._handle_choice('y')
            return
        self._handle_generic_input()


button_a = Button(5)   # Red
button_b = Button(6)   # [B]lue
button_x = Button(16)  # Green
button_y = Button(24)  # [Y]ellow

display = Display(output_device=scrollphathd)
game = Game(display)

button_a.when_pressed = game.button_a
button_b.when_pressed = game.button_b
button_x.when_pressed = game.button_x
button_y.when_pressed = game.button_y


while True:
    game.update()
    time.sleep(1.0 / 50)
