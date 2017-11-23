#!/usr/bin/env python

from __future__ import print_function
import subprocess
import sys
import time

try:
    import feedparser
except ImportError:
    sys.exit("This script requires the feedparser module\nInstall with: sudo pip install feedparser") 

import scrollphat


scrollphat.set_brightness(4)

# Every refresh_interval seconds we'll refresh the weather data, doesn't change too often so 30mins appropriate
pause = 0.12
ticks_per_second = 1/pause
refresh_interval = 60*30

if len(sys.argv)==2:
    postcode = sys.argv[1]
else:
    print("Usage: ./ukweather.py area")
    print("eg ./ukweather.py SW19")
    print("Defaulting to Sheffield-on-Sea")
    postcode = "S2" # Sheffield-on-Sea

url = "http://open.live.bbc.co.uk/weather/feeds/en/" + postcode + "/3dayforecast.rss"

def get_timeout():
    return ticks_per_second * refresh_interval

def get_wet():
# Get the weather data
    print("Updating weather for", postcode)
    d = feedparser.parse(url)
    entries = int(len(d['entries']))
    val = "        " + d['entries'][0]['title']
    val +="        " + d['entries'][1]['title']
    val +="        " + d['entries'][2]['title']
# Tidy & shorten the message for the scroll display
    val = val.replace("Maximum", "Max")
    val = val.replace("Minimum", "Min")
    val = val.replace("Temperature: ", "")
    val = val.replace(u"\u00B0","")
    val = val.replace(",", "")
    val = val.replace("(", "")
    val = val.replace(")", "")
    return val

timeout = get_timeout()
count = 0
msg = get_wet()
scrollphat.write_string(msg)

while True:
    try:
        scrollphat.scroll()
        time.sleep(pause)

        if(count > timeout):
            msg = get_wet()
            scrollphat.write_string(msg)
            timeout = get_timeout()
            count = 0
        else:
            count = count+ 1
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)

