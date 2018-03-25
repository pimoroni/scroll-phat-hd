#!/usr/bin/env python

# requires: netifaces for looking up IP in readable way
# requires: requests human readable HTTP requests

import json
import socket
import time
import urllib
from sys import exit

try:
    import requests
except ImportError:
    exit("This script requires the requests module\nInstall with: sudo pip install requests")

import scrollphat


def get_location():
    res = requests.get('http://ipinfo.io')
    if(res.status_code == 200):
        json_data = json.loads(res.text)
        return json_data
    return {}

# Python 2 vs 3 breaking changes.
def encode(qs):
    val = ""
    try:
        val = urllib.urlencode(qs).replace("+","%20")
    except:
        val = urllib.parse.urlencode(qs).replace("+", "%20")
    return val

def get_weather(address):
    base = "https://query.yahooapis.com/v1/public/yql?"
    query = "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text=\""+address+"\")"
    qs={"q": query, "format": "json", "env": "store://datatables.org/alltableswithkeys"}

    uri = base + encode(qs)                                        

    res = requests.get(uri)
    if(res.status_code==200):
        json_data = json.loads(res.text)
        return json_data
    return {}

def scroll_message(output):
    scrollphat.write_string(output)
    scrollphat.update()

    while(True):
        try:
            scrollphat.scroll()
            scrollphat.update()
            time.sleep(0.2)
        except KeyboardInterrupt:
            return

if(__name__ == '__main__'):
    scrollphat.set_brightness(4)
    location = get_location()
    location_string = location["city"] +", " + location["country"]
    print("Location: " + location_string)

    if(location["city"] != None):
        weather = get_weather(location_string)
        output = ""

        # Feel free to pick out other data here, for the scrolling message
        for x in range(0, 2):
            item = weather["query"]["results"]["channel"]["item"]["forecast"][x]
            output = output + " " +  item["day"] +": " + item["text"] + " - L: "+ item["low"] + "F - H: "+ item["high"]+"F"

        print(output)
        scroll_message(output)

        scrollphat.clear()
        quit()
