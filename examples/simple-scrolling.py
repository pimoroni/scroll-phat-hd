#!/usr/bin/env python

import time

import scrollphathd

print("""
Scroll pHAT HD: Simple Scrolling

A simple example showing a basic scrolling loop for scrolling
single messages across the display.

Press Ctrl+C to exit.
""")


def scroll_message(message):
    scrollphathd.clear() # Clear the display and reset scrolling to (0, 0)
    length = scrollphathd.write_string(message) # Write out your message
    scrollphathd.show() # Show the result
    time.sleep(0.5) # Initial delay before scrolling

    length -= scrollphathd.width
    
    # Now for the scrolling loop...
    while length > 0:
        scrollphathd.scroll(1) # Scroll the buffer one place to the left
        scrollphathd.show() # Show the result
        length -= 1
        time.sleep(0.02) # Delay for each scrolling step

    time.sleep(0.5) # Delay at the end of scrolling

scroll_message("Hello World! How are you today?")
