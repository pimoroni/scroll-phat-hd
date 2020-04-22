#!/usr/bin/env python3

from gpiozero import Button
from signal import pause

print("""Scroll HAT Mini: buttons.py

Demonstrates the use of Scroll HAT Mini's buttons with gpiozero.

Press Ctrl+C to exit!

""")


def pressed(button):
    button_name = button_map[button.pin.number]
    print(f"Button {button_name} pressed!")


button_map = {5: "A",
              6: "B",
              16: "X",
              24: "Y"}

button_a = Button(5)
button_b = Button(6)
button_x = Button(16)
button_y = Button(24)

try:
    button_a.when_pressed = pressed
    button_b.when_pressed = pressed
    button_x.when_pressed = pressed
    button_y.when_pressed = pressed

    pause()

except KeyboardInterrupt:
    button_a.close()
    button_b.close()
    button_x.close()
    button_y.close()
