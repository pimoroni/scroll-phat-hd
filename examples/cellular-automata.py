#!/usr/bin/env python

# simple CA
# loops through a bunch of interesting simple CA

import time
from sys import exit

try:
    import numpy
except ImportError:
    exit("This script requires the numpy module\nInstall with: sudo pip install numpy")

import scrollphathd


print("""
Scroll pHAT HD: Cellular Automata

Displays a series of interesting cellular automata rules.

Press Ctrl+C to exit!

""")


def mainloop():

    # set up the scrollPhat
    scrollphathd.clear()
    # Uncomment the below if your display is upside down
    #   (e.g. if you're using it in a Pimoroni Scroll Bot)
    #scrollphathd.rotate(degrees=180)
    scrollphathd.set_brightness(0.1)


    # define a list of some interesting rule numbers to loop through
    rules = [22, 30, 54, 60, 75, 90, 110, 150]
    rule = rules[0]

    # how many evolve steps to perform before starting the next CA rule
    maxSteps = 100
    loopCount = 0

    # define the matrix of cells and rows that we will be displaying
    matrix = numpy.zeros((7, 17), dtype=numpy.int)

    # set the initial condition of the first row
    # "dot" = single cell at position (0,8); top row, middle LED
    firstRow = [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0]
    matrix[0] = firstRow

    # We need to keep track of which row we are working on
    # the CA fills in from the top row and evolves downwards.
    # When we have filled the last row we'll scroll all the
    # rows up and just evolve the bottom row from then on.
    row = 0

    speed = 10


    while True:

        # redraw first so that it shows the initial contitions when first run
        for y in range(0, 7):
            for x in range(0, 17):
                scrollphathd.pixel(x, y, matrix[y, x])

        scrollphathd.show()

        loopCount += 1

        # if we have performed maxSteps...
        if loopCount > maxSteps:
            # reset a bunch of stuff
            loopCount = 0
            row = 0
            matrix = numpy.zeros((7, 17), dtype=numpy.int)
            matrix[0] = firstRow
            # get a new rule
            rules = numpy.roll(rules, -1, axis=0)
            rule = rules[0]

        # use the current row as the input for the next row
        inputRow = matrix[row]

        # make an empty array to fill with values
        outputRow = numpy.zeros((17), dtype=numpy.int)

        #  the secret sauce...
        #  step through each cell in the output row, calculate its value
        #  from the state of the input cell above and its left and right neighbour

        for x in range(0, 17):

            #  for each output cell, get the values of the input cell
            #  and its left and right neighbours.

            #  because cell 0 has no left neighbour we will
            #  get that value from the last cell in the row.
            #  similarly, the last cell in the row has no right neighbour
            #  so we will use the value of cell 0, effectively wrapping
            #  the horizontal edges of the display

            a = inputRow[x-1] if x > 0 else inputRow[16]
            b = inputRow[x]
            c = inputRow[x+1] if x < 16 else inputRow[0]


            #  a, b and c now contain the states of the three input cells
            #  that determine the state of our output cell

            #  there are 8 possible combinations for a,b,c
            #  they are:

            #  abc   abc   abc   abc   abc   abc   abc   abc
            #  111   110   101   100   011   010   001   000

            #  an abc combination will prodcude an output of either
            #  1 or 0 depending on the rule we are using

            #  for example, if we are running rule 30:
            #  the binary representation of 30 is 11110.
            #  we have to left-pad that out a bit so that we also have
            #  8 digits : "00011110"

            #  the rule can then be mapped onto our abc combinations like so:

            #  inputs   111   110   101   100   011   010   001   000
            #  outputs   0     0     0     1     1     1     1     0

            #  if we find an abc of a=1, b=0, c=0 we would match
            #  with "100" and output a 1


            #  if we were using rule number 110 we would get this mapping

            #  inputs   111   110   101   100   011   010   001   000
            #  outputs   0     1     1     0     1     1     0     0

            #  because the padded binary representation of the number 110 is
            #  "01101100" we get no match for "100"


            #  ok, so lets consider the first evolution of rule 30 starting
            #  with a single dot in the center of the first row.
            #  (using a row of seven cells, 17 is too many to type!)

            #  given row 0 =>   0001000

            #  our first abc is "000", 00]0100[0  (remember that we are wrapping)
            #  > this maps to 0

            #  our next abc is "000", [000]1000
            #  > this maps to 0

            #  our next abc is "001", 0[001]000
            #  > this maps to 1 yay!

            #  our next abc is "010", 00[010]00
            #  > this maps to 1

            #  our next abc is "100", 000[100]0
            #  > this maps to 1

            #  our next abc is "000", 0001[000]
            #  > this maps to 0

            #  our next abc is "000", 0]0010[00
            #  > this maps to 0

            #  we now have seven new cells and our our output row will be
            #  > "0011100"

            #  and our cumulative rows will be :
            #  row 0 > 0001000
            #  row 1 > 0011100

            #  after the next step, our cumulative output will be :
            #  row 0 > 0001000
            #  row 1 > 0011100
            #  row 2 > 0110010



            #  so that's nice, but we need a general way to do this for any rule
            #  ...

            #  to convert our input values (abc) into output values for any
            #  rule we will first notice that the input combinations "111",
            #  "110" etc are themselves binary representations of the numbers
            #  7,6,5,4,3,2,1,0 and that they are in index order if we read
            #  right to left.

            #  we can turn our abc result into a number and this will give
            #  the index position of our abc combination using our right to left order.

            #  for example, the abc pattern "011" is binary for 3
            #  ...  int("011", 2) === 3
            #  so we put a 1 in index position 3 (counting from 0, starting from the right)
            #  ... "00001000"
            #  and see if it matches against our binary rule 30


            #  0 0 0 0 1 0 0 0
            #  0 0 0 1 1 1 1 0
            #          ^
            #          ^
            #      a match!

            #  this is equivelant to the bitwise AND operation:
            #  3&30

            #  see here :
            #  https://wiki.python.org/moin/BitwiseOperators
            #  x & y Does a "bitwise and". Each bit of the output is 1 if the
            #  corresponding bit of x AND of y is 1, otherwise it's 0.


            #  so, after all that we now know the state of this output cell.
            #  fortunately the algorithm is a lot shorter than the explaination ;)

            #  construct our abc by bitshift and move a 1 to that index.
            o = 1 << ((a << 2) + (b << 1) + c)

            #  set the output cell to 1 if it &s with the rule, othewise 0
            outputRow[x] = 1 if o&rule else 0


        # incrementally fill in the rows until we fill the last row
        # then roll up the display matrix and evolve the last row
        if row < 6:
            row = row + 1
        else:
            matrix = numpy.roll(matrix, -1, axis=0)

        # set the matrix new row for the next redraw
        matrix[row] = outputRow

        # have a nap
        time.sleep(0.01 * speed)

try:
    mainloop()

except KeyboardInterrupt:
    scrollphathd.clear()
    scrollphathd.show()
    print("Exiting!")

# here endeth the script
