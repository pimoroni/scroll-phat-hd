#!/usr/bin/env python

#made by @mrglennjones with help from @pimoroni & pb

import time
try:
    import queue
except ImportError:
    import Queue as queue
from sys import exit

try:
    import tweepy
except ImportError:
    exit("This script requires the tweepy module\nInstall with: sudo pip install tweepy")

import scrollphathd
from scrollphathd.fonts import font5x7smoothed


# adjust the tracked keyword below to your keyword or #hashtag
keyword = '#bilgetank'

# enter your twitter app keys here
# you can get these at apps.twitter.com
consumer_key = ''
consumer_secret = ''

access_token = ''
access_token_secret = ''

if consumer_key == '' or consumer_secret == '' or access_token == '' or access_token_secret == '':
    print("You need to configure your Twitter API keys! Edit this file for more information!")
    exit(0)

# make FIFO queue
q = queue.Queue()

# define main loop to fetch formatted tweet from queue
def mainloop():
    scrollphathd.rotate(degrees=180)
    scrollphathd.clear()
    scrollphathd.show()

    while True:
        # grab the tweet string from the queue
        try:
            scrollphathd.clear()
            status = q.get(False)
            scrollphathd.write_string(status,font=font5x7smoothed, brightness=0.1)
            status_length = scrollphathd.write_string(status, x=0, y=0,font=font5x7smoothed, brightness=0.1)
            time.sleep(0.25)

            while status_length > 0:
                scrollphathd.show()
                scrollphathd.scroll(1)
                status_length -= 1
                time.sleep(0.01)

        except queue.Empty:
            time.sleep(1)

class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if not status.text.startswith('RT'):
            # format the incoming tweet string
            status = '     >>>>>     @%s: %s     ' % (status.user.screen_name.upper(), status.text.upper())
            status = status.encode('ascii', 'ignore').decode('ascii')

            # put tweet into the fifo queue
            q.put(status)

    def on_error(self, status_code):
        if status_code == 420:
            return False


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)

myStream.filter(track=[keyword], stall_warnings=True, async=True)


try:
    mainloop()

except KeyboardInterrupt:
    myStream.disconnect()
    del myStream
    print("Exiting!")

