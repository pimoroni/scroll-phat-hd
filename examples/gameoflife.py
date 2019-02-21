#!/usr/bin/env python

import scrollphathd
import time
import random

YSIZE = 7
XSIZE = 17
BRIGHT = 0.3

# Control update speed: 1 fastest - 5 slowest
SPEED = 3


print("""
Scroll pHAT HD: GameOfLife

Plays Conway's Game of Life.
Starts with random live cells and stops when stagnation is detected
or the maximum amount of iterations is reached.

Press Ctrl+C to exit!
""")


def generatemap():
    for y in range(-1, YSIZE + 1):
        for x in range(-1, XSIZE + 1):
            matrix[y, x] = 0

    # crude way to start with live cells, but adds count diversity
    for _ in range(100):
        y = random.randint(0, YSIZE - 1)
        x = random.randint(0, XSIZE - 1)
        matrix[y, x] = 1


def printmap(sleeptime):
    alive_counter = 0
    scrollphathd.clear()

    for y in range(0, YSIZE):
        for x in range(0, XSIZE):
            if matrix[y, x]:
                scrollphathd.set_pixel(x, y, BRIGHT)
                alive_counter += 1
            else:
                scrollphathd.set_pixel(x, y, 0)

    scrollphathd.show()
    time.sleep(sleeptime / 10)
    scrollphathd.clear()

    return alive_counter


def lifecycle():
    # preparing next cycle
    soonmatrix = {key: value for key, value in matrix.items()}
    for y in range(YSIZE):
        for x in range(XSIZE):
            neighbors = countneighbors(y, x, matrix[y, x])
            if matrix[y, x]:
                soonmatrix[y, x] = 1 if 1 < neighbors < 4 else 0
            else:
                soonmatrix[y, x] = 1 if neighbors == 3 else 0

    # activating next cycle
    matrix.update(soonmatrix)


def countneighbors(py, px, status):
    # Counts live neighbors by checking within a 3x3 grid
    neighbors = -1 if status else 0
    for y in range(py - 1, py + 2):
        for x in range(px - 1, px + 2):
            if matrix[y, x]:
                neighbors += 1
    return neighbors


while True:
    matrix = {}
    max_iterations = 100
    stagnation_max = 10
    alive_count_old = 0
    stagnation_count = 0

    generatemap()
    printmap(20)

    while True:
        lifecycle()
        active_count = printmap(SPEED)

        # checks if the amount of live cells changed
        if alive_count_old == active_count:
            stagnation_count += 1
        alive_count_old = active_count
        max_iterations -= 1

        if stagnation_count == stagnation_max or max_iterations < 1:
            break
