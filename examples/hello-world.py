#!/usr/bin/env python

import time

import scrollphathd

print("""
Scroll pHAT HD: Hello World

Scrolls "Hello World" across the screen
using the default 5x7 pixel large font.

Press Ctrl+C to exit!

""")

# Uncomment the below if your display is upside down
# (e.g. if you're using it in a Pimoroni Scroll Bot)
# scrollphathd.rotate(degrees=180)

# Write the "Hello World!" string in the buffer and
# set a more eye-friendly default brightness
scrollphathd.write_string(" Hello World!", brightness=0.5)

# Auto scroll using a while + time mechanism (no thread)
while True:
    # Show the buffer
    scrollphathd.show()
    # Scroll the buffer content
    scrollphathd.scroll()
    # Wait for 0.1s
    time.sleep(0.1)
