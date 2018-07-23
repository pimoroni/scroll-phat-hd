import scrollphathd as phat
import time, random

ysize = 7
xsize = 17
bright = 0.3
matrix = {}


def generatemap():
    for y in range(-1, ysize + 1):
        for x in range(-1, xsize + 1):
            matrix[y, x] = {'now': 0, 'soon': 0}

    # random light on
    # todo beautify
    for _ in range(100):
        y = random.randint(0, ysize - 1)
        x = random.randint(0, xsize - 1)
        matrix[y, x]['now'] = 1

    # for x in range(10):
    #     matrix[3, x + 3]['now'] = 1


def printmap(sleeptime):
    active_counter = 0
    phat.clear()

    for y in range(0, ysize):
        for x in range(0, xsize):
            if matrix[y, x]['now']:
                phat.set_pixel(x, y, bright)
                active_counter += 1
            else:
                phat.set_pixel(x, y, 0)
    phat.show()
    time.sleep(sleeptime)
    phat.clear()

    return active_counter


def lifecycle():
    # preparing next cycle
    for y in range(ysize):
        for x in range(xsize):
            neighbors = countneighbors(y, x, matrix[y, x]['now'])
            if matrix[y, x]['now']:
                matrix[y, x]['soon'] = 1 if 1 < neighbors < 4 else 0
            else:
                matrix[y, x]['soon'] = 1 if neighbors == 3 else 0

    # activating next cycle
    for y in range(ysize):
        for x in range(xsize):
            matrix[y, x]['now'] = matrix[y, x]['soon']


def countneighbors(py, px, status):
    neighbors = -1 if status else 0
    for y in range(py - 1, py + 2):
        for x in range(px - 1, px + 2):
            if matrix[y, x]['now']:
                neighbors += 1
    return neighbors


while True:
    max_iterations = 100
    stagnation_max = 10

    active_count_old = 0
    stagnation_count = 0
    generatemap()
    printmap(2)
    while True:
        lifecycle()
        active_count = printmap(0.1)
        if active_count_old == active_count:
            stagnation_count += 1
        active_count_old = active_count
        print("iter #{}, stagnation #{}".format(max_iterations, stagnation_count))
        max_iterations -= 1

        if stagnation_count == stagnation_max or max_iterations < 0:
            break
