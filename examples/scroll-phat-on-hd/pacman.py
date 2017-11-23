#!/usr/bin/env python

'''
usage: pacman.py [-h] [-v] [-b BRIGHTNESS] [-p POSITION] [-dt DANCE_TIMES]
                 [-pt PULSE_TIMES] [-pd PAUSE_DANCE] [-pp PAUSE_PULSE]
                 [-ps PAUSE_SCROLL] [-po PAUSE_SHOW] [-f FUNCTION]

Display a Space-Invader character over your scroll-pHAT from Pimoroni

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -b BRIGHTNESS, --brightness BRIGHTNESS
                        Set the brightness, default: 5
  -p POSITION, --position POSITION
						Set the start position, default: 0
  -dt DANCE_TIMES, --dance_times DANCE_TIMES
                        Set how many times to dance, default: 3
  -pt PULSE_TIMES, --pulse_times PULSE_TIMES
                        Set how many times to pulse, default: 3
  -pd PAUSE_DANCE, --pause-dance PAUSE_DANCE
                        Set the dance pause interval in seconds, default: 0.3
  -pp PAUSE_PULSE, --pause-pulse PAUSE_PULSE
                        Set the pulse pause interval in seconds, default: 0.3
  -ps PAUSE_SCROLL, --pause-scroll PAUSE_SCROLL
                        Set the scroll pause interval in seconds, default: 0.3
  -po PAUSE_SHOW, --pause-show PAUSE_SHOW
                        Set the show pause interval in seconds, default: 5
  -f FUNCTION, --function FUNCTION
                        Set the function to run ('dance-left', 'dance-right',
                        'pulse-left', 'pulse-right', 'show-closed', 'show-
                        open-left', 'show-open-right', 'scroll-left-right-in',
                        'scroll-left-right-out', 'scroll-left-right', 'scroll-
                        left-right-dance', 'scroll-left-right-in-pulse',
                        'scroll-right-left-in', 'scroll-right-left-out',
                        'scroll-right-left', 'scroll-right-left-dance',
                        'scroll-right-left-pulse', 'clear'), default:
                        scroll-left-right-pulse
'''

import argparse
import time

try:
    import scrollphat
except ImportError:
    exit("This script requires the requests_pip module\nInstall with: sudo pip install scrollphat")

__author__ = 'https://github.com/fejao'

DEFAULT_BRIGHTNESS = 5
DEFAULT_POSITION = 0
DEFAULT_DANCE_TIMES = 3
DEFAULT_PULSE_TIMES = 3
DEFAULT_FUNCTION_NAME = 'scroll-left-right-pulse'
DEFAULT_PAUSE_DANCE = 0.3
DEFAULT_PAUSE_PULSE = 0.3
DEFAULT_PAUSE_SCROLL = 0.3
DEFAULT_PAUSE_SHOW = 5
DEFAULT_SCROLL_DISTANCE = 8

class Pacman(object):
	'''Class with functions to display the Pacman figure'''

	def __init__(self, args):
		self.args = args

	#
	# OPEN
	#
	def mouthOpenColumn(self, columnNumber, position):
		'''Sets the columns for when it has the mouth open'''

		if self.args.verbose:
			print('Running PacmanRight.mouthOpenColumn, columnNumber: %s, position: %s' % (columnNumber, position))

		if columnNumber == 0:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)

		elif columnNumber == 1:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 2:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 3:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 4:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 4, 1)

		else:
			print('PacmanRight.mouthOpenColumn input error: %s' % columnNumber)

	def mouthOpenDisplayRight(self, position):
		'''Displays the Pacman from parsed position with the mouth open to the right'''

		if self.args.verbose:
			print('Running PacmanRight.mouthOpenDisplay, position: %s' %  position)

		if position > 6:
			print('Position too big to display setPositionCenter; MAX = 6')
		else:
			self.mouthOpenColumn(0, position)
			self.mouthOpenColumn(1, position + 1)
			self.mouthOpenColumn(2, position + 2)
			self.mouthOpenColumn(3, position + 3)
			self.mouthOpenColumn(4, position + 4)

	def mouthOpenDisplayLeft(self, position):
		'''Displays the Pacman from parsed position with the mouth open to the left'''

		if self.args.verbose:
			print('Running PacmanRight.mouthOpenDisplay, position: %s' %  position)

		if position > 6:
			print('Position too big to display setPositionCenter; MAX = 6')
		else:
			self.mouthOpenColumn(0, position + 4)
			self.mouthOpenColumn(1, position + 3)
			self.mouthOpenColumn(2, position + 2)
			self.mouthOpenColumn(3, position + 1)
			self.mouthOpenColumn(4, position)

	#
	# CLOSED
	#
	def mouthClosedColumn(self, columnNumber, position):
		'''Sets the columns for when it has the mouth closed'''

		if self.args.verbose:
			print('Running PacmanRight.mouthOpenColumn, columnNumber: %s, position: %s' % (columnNumber, position))

		if columnNumber == 0:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)

		elif columnNumber == 1:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 2:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 3:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 4:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)

		else:
			print('PacmanRight.mouthOpenColumn input error: %s' % columnNumber)

	def mouthClosedDisplay(self, position):
		'''Displays the Pacman from parsed position with the mouth closed'''

		if self.args.verbose:
			print('Running PacmanRight.mouthClosedDisplayRight, position: %s' %  position)

		if position > 6:
			print('Position too big to display setPositionCenter; MAX = 6')
		else:
			self.mouthClosedColumn(0, position)
			self.mouthClosedColumn(1, position + 1)
			self.mouthClosedColumn(2, position + 2)
			self.mouthClosedColumn(3, position + 3)
			self.mouthClosedColumn(4, position + 4)

	def setPositionMiddleClosed(self):
		'''Sets of the pacman to be displayed at the middle position'''

		if self.args.verbose:
			print('Running Pacman.setPositionMiddleClosed')

		self.mouthClosedColumn(4, 7)
		self.mouthClosedColumn(3, 6)
		self.mouthClosedColumn(2, 5)
		self.mouthClosedColumn(1, 4)
		self.mouthClosedColumn(0, 3)
		scrollphat.update()

	#
	# DANCE
	#
	def danceLeft(self, position):
		'''Sets the pacman to dance with the mouth opened to the left'''

		if self.args.verbose:
			print('Running Pacman.danceLeftt, position: %s' %  position)
			print('Dancing for %s times' % self.args.dance_times)

		for i in range(0, self.args.dance_times):

			# Open
			self.mouthOpenDisplayLeft(position)
			scrollphat.update()
			time.sleep(args.pause_dance)
			scrollphat.clear()

			# Closed
			self.mouthClosedDisplay(position)
			scrollphat.update()
			time.sleep(args.pause_dance)
			scrollphat.clear()

	def danceRight(self, position):
		'''Sets the pacman to dance with the mouth opened to the right'''

		if self.args.verbose:
			print('Running Pacman.danceRight, position: %s' %  position)
			print('Dancing for %s times' % self.args.dance_times)

		for i in range(0, self.args.dance_times):

			# Open
			self.mouthOpenDisplayRight(position)
			scrollphat.update()
			time.sleep(args.pause_dance)
			scrollphat.clear()

			# Closed
			self.mouthClosedDisplay(position)
			scrollphat.update()
			time.sleep(args.pause_dance)
			scrollphat.clear()

	#
	# PULSE
	#
	def pulseLeft(self, position):
		'''Sets the pacman to pulse with the mouth opened to the left'''

		if self.args.verbose:
			print('Running Pacman.pulseLeft, position: %s' %  position)
			print('Pulsing for %s times' % self.args.pulse_times)

		for i in range(0, self.args.pulse_times):
			if self.args.verbose:
				print('Setting brightness to: 10')
			scrollphat.set_brightness(10)
			self.mouthOpenDisplayLeft(position)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 7')
			scrollphat.set_brightness(7)
			self.mouthClosedDisplay(position)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 5')
			scrollphat.set_brightness(5)
			self.mouthOpenDisplayLeft(position)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 3')
			scrollphat.set_brightness(5)
			self.mouthClosedDisplay(position)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

	def pulseRight(self, position):
		'''Sets the pacman to pulse with the mouth opened to the right'''

		if self.args.verbose:
			print('Running Pacman.pulseLeft, position: %s' %  position)
			print('Pulsing for %s times' % self.args.pulse_times)

		for i in range(0, self.args.pulse_times):
			if self.args.verbose:
				print('Setting brightness to: 10')
			scrollphat.set_brightness(10)
			self.mouthOpenDisplayRight(position)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 7')
			scrollphat.set_brightness(7)
			self.mouthClosedDisplay(position)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 5')
			scrollphat.set_brightness(5)
			self.mouthOpenDisplayRight(position)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 3')
			scrollphat.set_brightness(5)
			self.mouthClosedDisplay(position)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

	#
	# SCROLL LEFT -> RIGHT
	#
	def scrollLeftRightInSteps(self, stepNumber):
		'''Sets the columns positions from left to right scrolling-in from stepNumber'''

		if self.args.verbose:
			print('Running Pacman.scrollLeftRightInSteps, stepNumber: %s' %  stepNumber)

		# Open
		if stepNumber == 1:
			self.mouthOpenColumn(4, 0)

		# Closed
		elif stepNumber == 2:
			for i in range(3, 5):
				self.mouthClosedColumn(i, i - 3)

		# Open
		elif stepNumber == 3:
			for i in range(2, 5):
				self.mouthOpenColumn(i, i - 2)

		# Closed
		elif stepNumber == 4:
			for i in range(1, 5):
				self.mouthClosedColumn(i, i - 1)

		# Open
		elif stepNumber == 5:
			for i in range(0, 5):
				self.mouthOpenColumn(i, i)

		# Closed
		elif stepNumber == 6:
			for i in range(0, 5):
				self.mouthClosedColumn(i, i + 1)

		# Open
		elif stepNumber == 7:
			for i in range(0, 5):
				self.mouthOpenColumn(i, i + 2)

		scrollphat.update()
		time.sleep(self.args.pause_scroll)
		scrollphat.clear()

	def scrollLeftRightOutSteps(self, stepNumber):
		'''Sets the columns positions from left to right scrolling-out from stepNumber'''

		if self.args.verbose:
			print('Running Pacman.scrollLeftRightOutSteps, stepNumber: %s' %  stepNumber)

		# Open
		if stepNumber == 1:
			for i in range(0, 5):
				self.mouthOpenColumn(i, i + 4)

		# Closed
		elif stepNumber == 2:
			for i in range(0, 5):
				self.mouthClosedColumn(i, i + 5)

		# Open
		elif stepNumber == 3:
			for i in range(0, 5):
				self.mouthOpenColumn(i, i + 6)

		# Closed
		elif stepNumber == 4:
			for i in range(0, 4):
				self.mouthClosedColumn(i, i + 7)

		# Open
		elif stepNumber == 5:
			for i in range(0, 3):
				self.mouthOpenColumn(i, i + 8)

		# Closed
		elif stepNumber == 6:
			for i in range(0, 2):
				self.mouthClosedColumn(i, i + 9)

		# Open
		elif stepNumber == 7:
			self.mouthOpenColumn(0, 10)

		scrollphat.update()
		time.sleep(self.args.pause_scroll)
		scrollphat.clear()

	def scrollLeftRightIn(self):
		'''Displays the Pacman scrolling in from left to right'''

		if self.args.verbose:
			print('Running DisplayVertical.scrollIn')

		for i in range(1, DEFAULT_SCROLL_DISTANCE):
			self.scrollLeftRightInSteps(i)

	def scrollLeftRightOut(self):
		'''Displays the Pacman scrolling out from left to right'''

		if self.args.verbose:
			print('Running DisplayVertical.scrollIn')

		for i in range(0, DEFAULT_SCROLL_DISTANCE):
			self.scrollLeftRightOutSteps(i)

	#
	# SCROLL RIGHT -> LEFT
	#
	def scrollRightLeftInSteps(self, stepNumber):
		'''Sets the columns positions from right to left scrolling-in from stepNumber'''

		if self.args.verbose:
			print('Running Pacman.scrollLeftRightInSteps, stepNumber: %s' %  stepNumber)

		# Open
		if stepNumber == 1:
			self.mouthOpenColumn(4, 10)

		# Closed
		elif stepNumber == 2:
			for i in range(3, 5):
				self.mouthClosedColumn(i, 13 - i)

		# Open
		elif stepNumber == 3:
			for i in range(2, 5):
				self.mouthOpenColumn(i, 12 - i)

		# Closed
		elif stepNumber == 4:
			for i in range(1, 5):
				self.mouthClosedColumn(i, 11 - i)

		# Open
		elif stepNumber == 5:
			for i in range(0, 5):
				self.mouthOpenColumn(i, 10 - i)

		# Closed
		elif stepNumber == 6:
			for i in range(0, 5):
				self.mouthClosedColumn(i, 9 - i)

		# Open
		elif stepNumber == 7:
			for i in range(0, 5):
				self.mouthOpenColumn(i, 8 - i)

		scrollphat.update()
		time.sleep(self.args.pause_scroll)
		scrollphat.clear()

	def scrollRightLeftOutSteps(self, stepNumber):
		'''Sets the columns positions from right to left scrolling-out from stepNumber'''

		if self.args.verbose:
			print('Running Pacman.scrollLeftRightInSteps, stepNumber: %s' %  stepNumber)

		# Open
		if stepNumber == 1:
			for i in range(0, 5):
				self.mouthOpenColumn(i, 6 - i)

		# Closed
		elif stepNumber == 2:
			for i in range(0, 5):
				self.mouthClosedColumn(i, 5 - i)

		# Open
		elif stepNumber == 3:
			for i in range(0, 5):
				self.mouthOpenColumn(i, 4 - i)

		# Closed
		elif stepNumber == 4:
			for i in range(0, 4):
				self.mouthClosedColumn(i, 3 - i)

		# Open
		elif stepNumber == 5:
			for i in range(0, 3):
				self.mouthOpenColumn(i, 2 - i)

		# Closed
		elif stepNumber == 6:
			for i in range(0, 2):
				self.mouthClosedColumn(i, 1 - i)

		# Open
		elif stepNumber == 7:
			self.mouthOpenColumn(0, 0)

		scrollphat.update()
		time.sleep(self.args.pause_scroll)
		scrollphat.clear()

	def scrollRightLeftIn(self):
		'''Displays the Pacman scrolling in from right to left'''

		if self.args.verbose:
			print('Running DisplayVertical.scrollIn')

		for i in range(0, DEFAULT_SCROLL_DISTANCE):
			self.scrollRightLeftInSteps(i)

	def scrollRightLeftOut(self):
		'''Displays the Pacman scrolling out from right to left'''

		if self.args.verbose:
			print('Running DisplayVertical.scrollIn')

		for i in range(0, DEFAULT_SCROLL_DISTANCE):
		#~ for i in range(0, 5):
			self.scrollRightLeftOutSteps(i)

#
# MAIN
#
def __main__(args):
    '''
    Main script function

    Parameters
    ----------
    args : argparse.Namespace(
        verbose : bool
        brightness : int,
        position : int,
		dance_times : int,
		pulse_times : int,
		pause_dance : float,
		pause_pulse : float,
		pause_scroll : float,
		pause_show : float,
		function : string,
	)
    Arguments parsed to run the main function of the script

    Returns
    -------
    None
    '''
    print('\nStarting pacman.py...')

    def runForFunctionName():
		'''Runs functions from the pacman classe from parsed function name'''

		try:
			if args.verbose:
				print('seting brightness to: %d' % args.brightness)
				print('Running %s' % args.function)

			# Set brightness
			scrollphat.set_brightness(args.brightness)

			if args.function == 'dance-left':
				pacman.danceLeft(args.position)

			elif args.function == 'dance-right':
				pacman.danceRight(args.position)

			elif args.function == 'pulse-left':
				pacman.pulseLeft(args.position)

			elif args.function == 'pulse-right':
				pacman.pulseRight(args.position)

			elif args.function == 'show-closed':
				pacman.mouthClosedDisplay(args.position)
				scrollphat.update()
				time.sleep(args.pause_show)
				scrollphat.clear()

			elif args.function == 'show-open-left':
				pacman.mouthOpenDisplayLeft(args.position)
				scrollphat.update()
				time.sleep(args.pause_show)
				scrollphat.clear()

			elif args.function == 'show-open-right':
				pacman.mouthOpenDisplayRight(args.position)
				scrollphat.update()
				time.sleep(args.pause_show)
				scrollphat.clear()

			elif args.function == 'scroll-left-right-in':
				pacman.scrollLeftRightIn()

			elif args.function == 'scroll-left-right-out':
				pacman.scrollLeftRightOut()

			elif args.function == 'scroll-left-right':
				pacman.scrollLeftRightIn()
				pacman.setPositionMiddleClosed()
				pacman.scrollLeftRightOut()

			elif args.function == 'scroll-left-right-dance':
				pacman.scrollLeftRightIn()
				pacman.setPositionMiddleClosed()
				time.sleep(args.pause_scroll)
				scrollphat.clear()
				pacman.danceRight(3)
				pacman.setPositionMiddleClosed()
				pacman.scrollLeftRightOut()

			elif args.function == 'scroll-left-right-pulse':
				pacman.scrollLeftRightIn()
				pacman.setPositionMiddleClosed()
				scrollphat.clear()
				pacman.pulseRight(3)
				pacman.setPositionMiddleClosed()
				pacman.scrollLeftRightOut()

			elif args.function == 'scroll-right-left-in':
				pacman.scrollRightLeftIn()

			elif args.function == 'scroll-right-left-out':
				pacman.scrollRightLeftOut()

			elif args.function == 'scroll-right-left':
				pacman.scrollRightLeftIn()
				pacman.setPositionMiddleClosed()
				pacman.scrollRightLeftOut()

			elif args.function == 'scroll-right-left-dance':
				pacman.scrollRightLeftIn()
				pacman.setPositionMiddleClosed()
				time.sleep(args.pause_scroll)
				scrollphat.clear()
				pacman.danceLeft(3)
				pacman.setPositionMiddleClosed()
				pacman.scrollRightLeftOut()

			elif args.function == 'scroll-right-left-pulse':
				pacman.scrollRightLeftIn()
				pacman.setPositionMiddleClosed()
				scrollphat.clear()
				pacman.pulseLeft(3)
				pacman.setPositionMiddleClosed()
				pacman.scrollRightLeftOut()

			elif args.function == 'clear':
				scrollphat.clear()

			else:
				print('Function unknown: %s' % args.function)
				args.function

		except KeyboardInterrupt:
				scrollphat.clear()

    # Creates the Pacman class object
    pacman = Pacman(args)

    # Run for parsed function
    runForFunctionName()

    print('\n...Finished pacman.py')

#
# PARSER
#
parser = argparse.ArgumentParser(description='Display a Space-Invader character over your scroll-pHAT from Pimoroni.')
parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

parser.add_argument('-b','--brightness', help="Set the brightness, default: %s" % DEFAULT_BRIGHTNESS, default=DEFAULT_BRIGHTNESS, type=int)
parser.add_argument('-p','--position', help="Set the start position, default: %s" % DEFAULT_POSITION, default=DEFAULT_POSITION, type=int)
parser.add_argument('-dt','--dance_times', help="Set how many times to dance, default: %s" % DEFAULT_DANCE_TIMES, default=DEFAULT_DANCE_TIMES, type=int)
parser.add_argument('-pt','--pulse_times', help="Set how many times to pulse, default: %s" % DEFAULT_PULSE_TIMES, default=DEFAULT_PULSE_TIMES, type=int)
parser.add_argument('-pd','--pause-dance', help="Set the dance pause interval in seconds, default: %s" % DEFAULT_PAUSE_DANCE, default=DEFAULT_PAUSE_DANCE, type=float)
parser.add_argument('-pp','--pause-pulse', help="Set the pulse pause interval in seconds, default: %s" % DEFAULT_PAUSE_PULSE, default=DEFAULT_PAUSE_PULSE, type=float)
parser.add_argument('-ps','--pause-scroll', help="Set the scroll pause interval in seconds, default: %s" % DEFAULT_PAUSE_SCROLL, default=DEFAULT_PAUSE_SCROLL, type=float)
parser.add_argument('-po','--pause-show', help="Set the show pause interval in seconds, default: %s" % DEFAULT_PAUSE_SHOW, default=DEFAULT_PAUSE_SHOW, type=float)
parser.add_argument('-f','--function', help="Set the function to run ('dance-left', 'dance-right', 'pulse-left', 'pulse-right', 'show-closed', \
'show-open-left', 'show-open-right',  'scroll-left-right-in', 'scroll-left-right-out', 'scroll-left-right', 'scroll-left-right-dance', 'scroll-left-right-in-pulse', \
'scroll-right-left-in', 'scroll-right-left-out', 'scroll-right-left', 'scroll-right-left-dance', 'scroll-right-left-pulse', 'clear') \
, default: %s" % DEFAULT_FUNCTION_NAME, default=DEFAULT_FUNCTION_NAME, type=str)

args = parser.parse_args()

# RUN SCRIPT
__main__(args)
