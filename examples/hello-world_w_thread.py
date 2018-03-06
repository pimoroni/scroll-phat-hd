#!/usr/bin/env python

import threading

import scrollphathd


def autoscroll(interval=0.1):
    """Autoscroll with a thread (recursive function).

    Automatically show and scroll the buffer according to the interval value.

    :param interval: Amount of seconds (or fractions thereof), not zero

    """

    # Start a timer
    threading.Timer(interval, autoscroll, [interval]).start()
    # Show the buffer
    scrollphathd.show()
    # Scroll the buffer content
    scrollphathd.scroll()


print("""
Scroll pHAT HD: Hello World

Scrolls "Hello World" across the screen
using the default 5x7 pixel large font.

Press Ctrl+C to exit!

""")

# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
#scrollphathd.rotate(degrees=180)

# Write the "Hello World!" string in the buffer and
#   set a more eye-friendly default brightness
scrollphathd.write_string(" Hello World!", brightness=0.5)

# Auto scroll using a thread
autoscroll()
