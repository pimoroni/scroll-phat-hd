#!/usr/bin/env python

import time
import random
from random import randint

import numpy as np
import scrollphathd

scrollphathd.clear()
scrollphathd.rotate(degrees=180)
scrollphathd.set_brightness(0.25)

    
## define the matrix of cells and rows that we will be displaying
matrix = np.zeros((7, 17), dtype=np.double)

while True:
    for y in range(0, 7):
        for x in range(0, 17):
            scrollphathd.pixel(x, y, matrix[y,x])
    
    scrollphathd.show()
    matrix = np.roll(matrix, 1, axis=0)
    matrix[0] = matrix[1] * 0.5
    for a in range(0, 3):
        x = random.randint(0, 16)
        matrix[0,x] = 1
