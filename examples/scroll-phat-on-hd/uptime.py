#!/usr/bin/env python

import subprocess
import sys
import time

import scrollphat


scrollphat.set_brightness(4)

# Every refresh_interval seconds we'll refresh the uptime
# Only has to change every 60 seconds.
pause = 0.12
ticks_per_second = 1/pause
refresh_interval = 10

def get_timeout():
    return ticks_per_second * refresh_interval

def get_msg():
    val = subprocess.check_output(["uptime", "-p"]).decode("utf-8")
    val = val.replace("\n","")
    val = val.replace("minutes","mins")
    val = val + "    "
    return val

timeout = get_timeout()
count = 0
msg = get_msg()
scrollphat.write_string(msg)

while True:
    try:
        scrollphat.scroll()
        time.sleep(pause)

        if(count > timeout):
            msg = get_msg()
            scrollphat.write_string(msg)
            timeout = get_timeout()
            count = 0
            print ("Updating uptime message")
        else:
            count = count+ 1
    except KeyboardInterrupt:
        scrollphat.clear()
        sys.exit(-1)

