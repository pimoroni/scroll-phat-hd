#!/usr/bin/env python

import sys
import time
import tweepy
import scrollphathd
import Queue
from scrollphathd.fonts import font5x7smoothed


#make FIFO queue
q = Queue.Queue()

#define main loop to fetch formatted tweet from queue
def mainloop():
    while True:
        #grab the tweet string from the queue
        status = q.get()
        scrollphathd.write_string(status,font=font5x7smoothed, brightness=0.1)
        status_length = scrollphathd.write_string(status, x=0, y=0,font=font5x7smoothed, brightness=0.1)
        time.sleep(0.25)
        while status_length > 0:
             scrollphathd.rotate(degrees=180)
             scrollphathd.show()
             scrollphathd.scroll(1)
             status_length -= 1
             time.sleep(0.01)
        else:
             scrollphathd.clear()
                
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        if not status.text.startswith('RT'):
            #format the incoming tweet string
            status = '     >>>>>     @%s: %s     ' % (status.user.screen_name.upper(), status.text.upper())
            status = status.encode('ascii', 'ignore').decode('ascii')
            # put tweet into the fifo queue
            q.put(status)
    def on_error(self, status_code):
        if status_code == 420:
            return False

#enter your twitter app keys here        
consumer_key =''
consumer_secret =''

access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

myStreamListener = MyStreamListener()
myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)

#adjust the tracked keyword 'hug' to your keyword or #hashtag
myStream.filter(track=['hug'], stall_warnings=True, async=True)


try:
    mainloop()
except KeyboardInterrupt:
    print('exit')
    myStream.disconnect()
sys.exit(-1)
