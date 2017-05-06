#!/usr/bin/env python

# please excuse my python, i'm new here ;)

import time
import math
import threading

import numpy as np
import scrollphathd

import Tkinter

## use this so that we can break out of the rendering thread
running = False

## our rule number
rule = 30

## some other intersting rules
## rule = 22
## rule = 54
## rule = 60
## rule = 110
## rule = 132

## init the scrollphat and start the rendering loop
def initRenderThread(_rule):  
    global matrix
    global running
    global row
    global rule
    
    matrix = np.zeros((7, 17), dtype=np.int)
    matrix[0,8] = 1;
    row = 0
    scrollphathd.clear()
    scrollphathd.rotate(degrees=180)
    scrollphathd.set_brightness(0.1)
    rule = _rule
    print 'RULE', rule, str(bin(rule))[2:]

    running=True;

    while running:
        ## redraw first, so that it shows the initial contitions ;)
        for y in range(0, 7):
            for x in range(0, 17):
                scrollphathd.pixel(x, y, matrix[y,x])
        
        scrollphathd.show()

        ## incrementally fill in the rows until we hit the bottom
        ## then roll the matrix and replace the last row
        if row < 6:
            matrix[row+1] = evolve(matrix[row])
            row = row + 1
        else:
            matrix = np.roll(matrix, -1, axis=0)
            matrix[6] = evolve(matrix[5])

        ##  might want to slow it down a bit ;)
        ##  time.sleep(0.01)

def evolve(row):
    ## make an empty array to fill with values
    out = np.zeros((17), dtype=np.int)
    for x in range(0, 17):
        ##  get the sum [Y] over the range x-1 to x+1
        ##  bit shift 1 bit Y places to the left
        ##  bitise AND with the rule
        ##  so, read the three cells at x-1, x and x+1 (with wrapping)
        a = row[x-1] if x > 0 else row[16]
        b = row[x]
        c = row[x+1] if x < 16 else row[0]
        o = 1 << ((a << 2) + (b << 1) + c)
        out[x] = 1 if o&rule else 0
    return out

## start / restart the CA
def startCA():
    global th
    global running
    global rule
    if running:
        stopCA()
        time.sleep(0.5)
        clearCA()
        startCA()
    else:
        ## start a new thread. prevents the GUI locking up ;)
        th = threading.Thread(target=initRenderThread, args=(rule,))
        th.start()

## stop the CA
def stopCA():
    global running
    running=False;

## clear screen
def clearCA():
    scrollphathd.clear()
    scrollphathd.show()

## handle rule change
def changeRule():
    global rule
    rule = int(SRuleNumber.get())


## GUI Specs for a simple control panel

top = Tkinter.Tk()
top.grid()

svRule = Tkinter.StringVar()
SRuleNumber = Tkinter.Spinbox(top, from_=1, to=256, textvariable=svRule, command = changeRule )
SRuleNumber.grid(column=1, row=0, columnspan=2)
svRule.set(rule)

BStart = Tkinter.Button(top, text ="Start", command = startCA)
BStart.grid(column=1, row=1)

BStop = Tkinter.Button(top, text ="Stop", command = stopCA)
BStop.grid(column=2, row=1)

BClear = Tkinter.Button(top, text ="Clear", command = clearCA)
BClear.grid(column=3, row=1)

## Start the GUI
top.mainloop()

## clean exit when GUI window closes
stopCA()
clearCA()

## here endeth the script
