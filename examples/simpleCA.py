#!/usr/bin/env python

import time
import math
import threading

import numpy as np
from collections import deque
import scrollphathd

import Tkinter
top = Tkinter.Tk()

running = False

rule=30

##rule = 54
##rule = 60
##rule = 110
##rule = 132

def init(_rule):  
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
        redraw()
        if row < 6:
            matrix[row+1] = evolve(matrix[row])
            row = row + 1
        else:
            matrix = np.roll(matrix, -1, axis=0)
            matrix[6] = evolve(matrix[5])


def redraw():
    for y in range(0, 7):
        for x in range(0, 17):
            brightness = matrix[y,x]
            scrollphathd.pixel(x, y, brightness)
    scrollphathd.show()
    ##  might want to slow it down a bit ;)
    ##  time.sleep(0.01)

def evolve(row):
    out = np.zeros((17), dtype=np.int)
    for x in range(0, 17):
        ##  get the sum [Y] over the range x-1 to x+1
        ##  bit shift 1bit Y places to the left
        ##  XOR with the rule
        ##  so, read the three cells at x-1, x and x+1 (with wrapping)
        a = row[x-1] if x > 0 else row[16]
        b = row[x]
        c = row[x+1] if x < 16 else row[0]
        o = 1 << ((a << 2) + (b << 1) + c)
        out[x] = 1 if o&rule else 0
    return out

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
        th = threading.Thread(target=init, args=(rule,))
        th.start()

def stopCA():
    global running
    running=False;

def clearCA():
    scrollphathd.clear()
    scrollphathd.show()

def changeRule():
    global rule
    rule = int(SRuleNumber.get())


svRule = Tkinter.StringVar()
SRuleNumber = Tkinter.Spinbox(top, from_=1, to=256, textvariable=svRule, command = changeRule )
SRuleNumber.pack()
svRule.set(rule)

BStart = Tkinter.Button(top, text ="Start", command = startCA)
BStart.pack()

BStop = Tkinter.Button(top, text ="Stop", command = stopCA)
BStop.pack()

BClear = Tkinter.Button(top, text ="Clear", command = clearCA)
BClear.pack()

top.mainloop()
