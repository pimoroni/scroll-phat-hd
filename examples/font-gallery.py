#!/usr/bin/env python

import time

import scrollphathd
from scrollphathd.fonts import fontd3, fontgauntlet, fontorgan, fonthachicro

print("""
Scroll pHAT HD: Simple Scrolling

A simple example showing a basic scrolling loop for scrolling
single messages across the display.

Press Ctrl+C to exit.
""")


def scroll_message(font, message):
    scrollphathd.set_font(font)
    scrollphathd.clear()                         # Clear the display and reset scrolling to (0, 0)
    length = scrollphathd.write_string(message)  # Write out your message
    scrollphathd.show()                          # Show the result
    time.sleep(0.5)                              # Initial delay before scrolling

    length -= scrollphathd.width

    # Now for the scrolling loop...
    while length > 0:
        scrollphathd.scroll(1)                   # Scroll the buffer one place to the left
        scrollphathd.show()                      # Show the result
        length -= 1
        time.sleep(0.02)                         # Delay for each scrolling step

    time.sleep(0.5)                              # Delay at the end of scrolling


scrollphathd.set_brightness(0.5)

for font, text in (
        (fontd3, "THIS IS FONT D3"),
        (fontgauntlet, "THIS IS FONT GAUNTLET"),
        (fontorgan, "THIS IS FONT ORGAN"),
        (fonthachicro, "This is font Hachicro"), ):
    scroll_message(font, text)
    time.sleep(0.5)
