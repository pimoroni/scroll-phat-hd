# !/usr/bin/env python
#
#
#
# Update to the wunderground-temp-display.py script to use the OpenWeather API and display on scrollphathd.
# This script shows the current temperature along with an indicator of
# the temperature trend (same, going up, going down), averaged over a given period of time.
# It also shows a small line at the bottom which indicates current wind speed and gusts.
# Current speed is shown using a brighter color and gusts are show using a dimmer color.
#
# Development environment: Python v3 on a Raspberry Pi Zero-W running Raspbian and default scrollphathd libraries
#
# Originally built by Mark Ehr, 1/12/18, and released to the public domain with no warranties expressed or implied. Or something along those lines.
# Feel free to use this code any way that you'd like. If you want to give credit, that's great.
#
# Note: if you want this to auto-run upon boot, add this line to the bottom of /etc/rc.local just above the "exit 0" line:
#   sudo python {path}/wunderground-temp-display.py &
#
# Also note that if you receive an odd "Remote I/O" error, that's the scrollphathd's odd way of saying that it can't
# communicate with the display. Check the hardware connection to make sure all of the pins are seated. In Mark's case, it
# happened randomly until they re-soldered the header connections on the RPi as well as the hat.
#

# Default scrollphathd library
import scrollphathd
from scrollphathd.fonts import font3x5

# Used to make web calls to OpenWeather
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

# Used to parse OpenWeather JSON data
import json
# Returns time values
import time
import os

# Uncomment the below if your display is upside down
# (e.g. if you're using it in a Pimoroni Scroll Bot)
scrollphathd.rotate(degrees=180)

# OpenWeather API key. Make sure to put your unique OpenWeather key in here
OW_API_KEY = "YOUR_API_KEY_GOES_HERE"

# Or set the OW_API_KEY environment variable
OW_API_KEY = os.environ.get("OW_API_KEY", OW_API_KEY)

# Customize this for your desired location. Find a JSON list of all city IDs here: http://bulk.openweathermap.org/sample/
OW_STATION = "5799841"
# Kirkland, WA

# Weather polling interval (seconds). Free OpenWeather API accounts allow 60 calls/minute and 1Mil/month.
POLL_INTERVAL = 30

# Interval after which the average temp is reset in Minutes. Used to make sure that the temp trending indicator stays accurate. Default is 15 min.
AVG_TEMP_RESET_INTERVAL = 15

# Flags used to specify whether to display actual or "feels like" temperature.
# Change CURRENT_TEMP_DISPLAY to 1 for actual temp and anything other than 1 for feels like temperature
CURRENT_TEMP_DISPLAY = 1

# Display settings
BRIGHT = 0.2
DIM = 0.1
# Show gusts as a bright dot
GUST_BRIGHTNESS = 0.3
# Show current speed as a slightly dimmer line
WIND_BRIGHTNESS = 0.1

# "Knight Rider" pulse delay. See comments below for description of what this is.
# Note that this loop uses the lion's share of CPU, so if your goal is to minimize CPU usage, increase the delay.
# Of course, increasing the delay results in a slightly less cool KR pulse. In practice, a value of 0.05 results in ~16% Python CPU utilization on
# a Raspberry Pi Zero-W. Increasing this to 0.1 drops CPU to ~10%, of course YMMV.
KR_PULSE_DELAY = 0.2

# Temperature scale (C or F). MUST USE UPPERCASE.
TEMP_SCALE = "F"

# Max wind speed. Used to calculate the wind speed bar graph
# (17 "x" pixels / max wind speed = ratio to multiply current wind speed by in order to determine much much of a line to draw)
# Set max wind speed according to scale

if TEMP_SCALE == "F":
    MAX_WIND_SPEED = 42.0
# MPH; default was set to 75.0, I lowered to 42 for better viewing of lower wind speeds
else:
    MAX_WIND_SPEED = 100.0
# KPH; default 100.0

# Debug flag  - set to 1 if you want to print(informative console messages)
DEBUG = 0

# Initialize global variables before use
current_temp = 0.0
average_temp = 0.0
wind_chill = 0.0
average_temp_counter = 0
average_temp_cumulative = 0.0
total_poll_time = 0   # Used to reset the average temp after a defined amount of time has passed
wind_speed = 0.0
wind_gusts = 0
actual_str = " "
feels_like_str = " "
feels_like = 0


# get_weather_data() - Retrieves and parses the weather data we want to display from OpenWeather.
# Updates global variables with weather data formatted for display use
# To request a free API key, go here: https://openweathermap.org/price


def get_weather_data():
    # Make sure that the module updates the global variables instead of creating local copies
    global current_temp
    global average_temp_cumulative

    global average_temp_counter
    global average_temp
    global wind_speed
    global wind_gusts
    global current_str
    global actual_str
    global feels_like_str
    global feels_like

    # Get current conditions. Substitute your personal OpenWeather API key and the desired weather station code.
    # Build OpenWeather URL using API key and station specified at top.
    # This code retrieves a complete set of current weather conditions and loads them up into a JSON catalog.
    # Note that JSON, while very powerful, can also be very confusing to decode. Take care especially when memory and compute resources are scarce.

    # Removed the Raise Exception as it was closing the program when WiFi was lost. Added a sleep to give WiFi time to reconnect.
    url_str = "http://api.openweathermap.org/data/2.5/weather?id=" + OW_STATION + "&appid=" + OW_API_KEY + "&units=imperial"
    try:
        conditions = urllib2.urlopen(url_str)
        json_string = conditions.read()         # Load into a json string
        parsed_cond = json.loads(json_string.decode())      # Parse the string into a json catalog
        conditions.close()

        # Build current temperature string

        # Check to see if average temp counters need to be reset
        if (average_temp_counter * POLL_INTERVAL / 60) > AVG_TEMP_RESET_INTERVAL:
            average_temp_cumulative = 0.0
            average_temp_counter = 0
            if DEBUG:
                print("Resetting average temp counters")
        # Parse out the current temperature and wind speeds from the json catalog based on which temperature scale is being used
        # Assumption was made that if C is being used for temp, kph is also in use. Apologies if that is not the case everywhere. :-)
        if TEMP_SCALE == "F":   # Fahrenheit
            current_temp = parsed_cond['main']['temp']   # String used for calculations
            wind_speed = float(parsed_cond['wind']['speed'])
            wind_gusts = float(parsed_cond['wind']['gust'])
            feels_like = float(parsed_cond['main']['feels_like'])
        else:   # Celsius
            current_temp = parsed_cond['main']['temp']
            wind_speed = float(parsed_cond['wind']['speed'])
            wind_gusts = float(parsed_cond['wind']['speed'])
            feels_like = float(parsed_cond['main']['feels_like'])

        # Calculate average temperature, which is used to determine temperature trending (same, up, down)
        average_temp_cumulative = average_temp_cumulative + current_temp
        average_temp_counter = average_temp_counter + 1
        average_temp = average_temp_cumulative / average_temp_counter

        # Convert to integer from float. For some reason you can't cast the above directly as an int, so need to take an extra step.
        # Mark thinks there is a more elegant way to doing this. I think this way works great. :-D
        fl_int = int(feels_like)
        fl_str = str(fl_int)
        as_int = int(current_temp)
        actual_str = str(as_int)
        if DEBUG:
            print("get_weather_data()")
            print("Current temp ", current_temp, TEMP_SCALE)
            print("Average temp ", average_temp, TEMP_SCALE)
            print("Feels like ", feels_like, TEMP_SCALE)
            print("Wind speed: ", wind_speed)
            print("Wind gusts: ", wind_gusts)
            print("Feels like string: [", fl_str, "]")
            print("Temperature string: [", actual_str, "]")

        # If you want to play around with displaying other measurements.
        # You can view all available data by pasting the OpenWeather API URL above into a web browser, which will return the raw json output.
        # Or by reading their documentation: https://openweathermap.org/current

        actual_str = actual_str + TEMP_SCALE   # remove unneeded trailing data and append temperature scale (C or F) to the end
        feels_like_str = fl_str + TEMP_SCALE   # remove unneeded trailing data and append temperature scale (C or F) to the end
        if DEBUG:
            print("Actual str: ", actual_str)
            print("Feels like str: ", feels_like_str)
        return

    except Exception as e:
        print(e)
        actual_str = ""
        return

def draw_kr_pulse(pos, dir):
    # Clear 5 pixel line (easier than keeping track of where the previous illuminated pixel was)
    scrollphathd.clear_rect(12, 5, 5, 1)
    x = pos + 11   # Increase position to the actual x offset we need
    scrollphathd.set_pixel(x, 5, 0.2)   # Turn on the current pixel
    scrollphathd.show()
    time.sleep(KR_PULSE_DELAY)
    return


def draw_temp_trend(dir):

    if dir == 0:   # Equal - don't display anything. Clear the area where direction arrow is shown
        scrollphathd.clear_rect(14, 0, 3, 6)
    elif dir == 1:   # Increasing = up arrow. Draw an up arrow symbol on the right side of the display
        for y in range(0, 5):
            scrollphathd.set_pixel(15, y, BRIGHT)   # Draw middle line of arrow
        scrollphathd.set_pixel(14, 1, BRIGHT)   # Draw the 'wings' of the arrow
        scrollphathd.set_pixel(16, 1, BRIGHT)
    elif dir == -1:   # Decreasing = down arrow
        for y in range(0, 5):
            scrollphathd.set_pixel(15, y, BRIGHT)   # Draw middle line of arrow
        scrollphathd.set_pixel(14, 3, BRIGHT)
        scrollphathd.set_pixel(16, 3, BRIGHT)
    return

# draw_wind_line() - draws a single line indicator of wind speed and wind gusts on the bottom of the display
# Current wind speed is shown as as bright line and gusts as as dim line.
#
# Calculation: calculate a ratio (17 pixels / max wind speed) and multiply by actual wind speed, rounding
#   to integer, yielding the number of pixels on 'x' axis to illuminate.

def draw_wind_line():
    global wind_speed
    global wind_gusts
    wind_multiplier = (17.0 / MAX_WIND_SPEED)
    if DEBUG:
        print("Wind multiplier: ", wind_multiplier)
    wind_calc = wind_multiplier * wind_speed
    if DEBUG:
        print("wind calc: ", wind_calc)
    wind_calc = int(wind_calc)   # Convert to int
    if wind_calc > 17:   # Just in case something goes haywire, like a hurricane :-)
        wind_calc = 17
    gust_calc = wind_multiplier * wind_gusts
    if DEBUG:
        print("gust calc: ", gust_calc)
    gust_calc = int(gust_calc)
    if gust_calc > 17:
        gust_calc = 17
    if DEBUG:
        print("Wind speed, calc", wind_speed, wind_calc)
        print("wind gusts, calc", wind_gusts, gust_calc)
    # Draw the wind speed first
    for x in range(0, wind_calc):
        scrollphathd.set_pixel(x, 6, WIND_BRIGHTNESS)
    # Now draw the gust indicator as a single pixel
    if gust_calc:   # Only draw if non zero
        scrollphathd.set_pixel(gust_calc-1, 6, GUST_BRIGHTNESS)
    return

# display_temp_value()
# This module allows the user to specify if they want actual or "feels like" temperature displayed.
# 'Feels like' includes things like wind and humidity.
# CURRENT_TEMP_DISPLAY controls which temperature to display.

def display_temp_value():
    global actual_str
    global feels_like_str
    # clear the old temp reading. If temp > 100 then clear an extra digit's worth of pixels
    if current_temp < 100:
        scrollphathd.clear_rect(0, 0, 12, 5)
    else:
        scrollphathd.clear_rect(0, 0, 17, 5)
    if CURRENT_TEMP_DISPLAY == 1:   # show actual temp
        scrollphathd.write_string(actual_str, x=0, y=0, font=font3x5, brightness=BRIGHT)
    else:   # Show feels_like temp
        scrollphathd.write_string(feels_like_str, x=0, y=0, font=font3x5, brightness=BRIGHT)
    scrollphathd.show()
    time.sleep(1)
    return


# BEGIN MAIN LOGIC

print("'Live' temperature and wind display using OpenWeather data.")
print("Uses Raspberry Pi and Scrollphathd display. Written by Mark Ehr, January 2018")
print("Updated to OpenWeather APIs by Will Dolezal, December 2021, and kept alive by you.")
print("Press Ctrl-C to exit")
print("Current weather station: ", OW_STATION)

# Initial weather data poll and write to display
get_weather_data()
display_temp_value()
draw_wind_line()

# Loop forever until user hits Ctrl-C
# Ctrl-C raises a KeyboardInterrupt and prevents any code below the 'while True' statement from running.

while True:
    if not (int(time.time()) % POLL_INTERVAL):
        prev_temp = current_temp
        get_weather_data()
        scrollphathd.clear()
        draw_wind_line()
        # Don't show temp trend arrow if > 100 degrees or < -10 degrees -- not enough room on the display.
        if current_temp < average_temp and (current_temp < 100 or current_temp < -9):
            if DEBUG:
                print(time.asctime(time.localtime(time.time())), "Actual temp", actual_str, "Feels like temp", feels_like_str, "-")
            draw_temp_trend(-1)
        elif current_temp == average_temp and (current_temp < 100 or current_temp < -9):
            if DEBUG:
                print(time.asctime(time.localtime(time.time())), "Actual temp", actual_str, "Feels like temp", feels_like_str, "=")
            draw_temp_trend(0)
        elif current_temp > average_temp and (current_temp < 100 or current_temp < -9):
            if DEBUG:
                print(time.asctime(time.localtime(time.time())), "Actual temp", actual_str, "Feels like temp", feels_like_str, "+")
            draw_temp_trend(1)
        display_temp_value()   # If you want actual temp, just change to ACTUAL

    # Pulse a pixel, Knight Rider style, just to show that everything is alive and working.
    # Sleep function in draw_kr_pulse keeps Python from consuming 100% CPU
    # Use display line 5, 14-17
    for pulse in range(1, 5):
        draw_kr_pulse(pulse, 1)   # Left to right
    for pulse in range(5, 1, -1):
        draw_kr_pulse(pulse, -1)   # Back the other way
