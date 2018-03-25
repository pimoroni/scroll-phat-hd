#!/usr/bin/env python

'''
usage: space-invaders.py [-h] [-v] [-b BRIGHTNESS] [-dt DANCE_TIMES]
                         [-pt PULSE_TIMES] [-pd PAUSE_DANCE] [-pp PAUSE_PULSE]
                         [-ps PAUSE_SCROLL] [-f FUNCTION]

Display a Space-Invader character over your scroll-pHAT from Pimoroni

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         Increase output verbosity
  -b BRIGHTNESS, --brightness BRIGHTNESS
                        Set the brightness, default: 5
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
                        Set the function to run ('dance', 'pulse', 'show-arms-
                        down', 'show-arms-up', 'scroll-in', 'scroll-out',
                        'scroll', 'scroll-and-dance', 'scroll-and-pulse',
                        'clear'), default: scroll-and-pulse
'''

import argparse
import time

try:
    import scrollphat
except ImportError:
    exit("This script requires the requests_pip module\nInstall with: sudo pip install scrollphat")

__author__ = 'https://github.com/fejao'

DEFAULT_BRIGHTNESS = 5
DEFAULT_DANCE_TIMES = 3
DEFAULT_PULSE_TIMES = 3
DEFAULT_FUNCTION_NAME = 'scroll-and-pulse'
DEFAULT_PAUSE_DANCE = 0.3
DEFAULT_PAUSE_PULSE = 0.3
DEFAULT_PAUSE_SCROLL = 0.3
DEFAULT_PAUSE_SHOW = 5

DEFAULT_SCROLL_DISTANCE = 11

class SpaceInvader(object):
	'''Class with functions to display the space-invader figure'''

	def __init__(self, args):
		self.args = args

	def armDownColumn(self, columnNumber, position):
		'''Sets the columns for when it has the arms up'''

		if self.args.verbose:
			print('Running SpaceInvader.armUpDown, columnNumber: %s, position: %s' % (columnNumber, position))

		if columnNumber == 0:
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)

		elif columnNumber == 1:
			scrollphat.set_pixel(position, 2, 1)

		elif columnNumber == 2:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 3:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 4:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)

		elif columnNumber == 5:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)

		elif columnNumber == 6:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 7:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 8:
			scrollphat.set_pixel(position, 2, 1)

		elif columnNumber == 9:
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)

		else:
			print('armDownColumn input error: %s' % columnNumber)

	def armDownDisplay(self, position):
		'''Displays the space invader from parsed position with arms down'''

		if self.args.verbose:
			print('Running SpaceInvader.armDownDisplay, position: %s' %  position)

		if position > 6:
			print('Position too big to display setPositionCenter; MAX = 4')
		else:
			self.armDownColumn(0, position)
			self.armDownColumn(1, position + 1)
			self.armDownColumn(2, position + 2)
			self.armDownColumn(3, position + 3)
			self.armDownColumn(4, position + 4)
			self.armDownColumn(5, position + 5)
			self.armDownColumn(6, position + 6)
			self.armDownColumn(7, position + 7)
			self.armDownColumn(8, position + 8)
			self.armDownColumn(9, position + 9)

	def armUpColumn(self, columnNumber, position):
		'''Sets the columns for when it has the arms down'''

		if self.args.verbose:
			print('Running SpaceInvader.armUpDown, columnNumber: %s, position: %s' % (columnNumber, position))

		if columnNumber == 0:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)

		elif columnNumber == 1:
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 2:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 3:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)

		elif columnNumber == 4:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)

		elif columnNumber == 5:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)

		elif columnNumber == 6:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)

		elif columnNumber == 7:
			scrollphat.set_pixel(position, 0, 1)
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 3, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 8:
			scrollphat.set_pixel(position, 2, 1)
			scrollphat.set_pixel(position, 4, 1)

		elif columnNumber == 9:
			scrollphat.set_pixel(position, 1, 1)
			scrollphat.set_pixel(position, 2, 1)

		else:
			print('armDownColumn input error: %s' % columnNumber)

	def armUpDisplay(self, position):
		'''Displays the space invader from parsed position with arms up'''

		if self.args.verbose:
			print('Running SpaceInvader.armDownDisplay, position: %s' %  position)

		if position > 6:
			print('Position too big to display setPositionCenter; MAX = 4')
		else:
			self.armUpColumn(0, position)
			self.armUpColumn(1, position + 1)
			self.armUpColumn(2, position + 2)
			self.armUpColumn(3, position + 3)
			self.armUpColumn(4, position + 4)
			self.armUpColumn(5, position + 5)
			self.armUpColumn(6, position + 6)
			self.armUpColumn(7, position + 7)
			self.armUpColumn(8, position + 8)
			self.armUpColumn(9, position + 9)

	#
	# DANCE
	#
	def dance(self):
		'''Displays the space invader dancing'''

		if self.args.verbose:
			print('Running SpaceInvader.dance')
			print('Dancing for %s times' % self.args.dance_times)

		for i in range(0, self.args.dance_times):

			# Arm Down
			self.armDownDisplay(0)
			scrollphat.update()
			time.sleep(args.pause_dance)
			scrollphat.clear()

			# Arm Up
			self.armUpDisplay(0)
			scrollphat.update()
			time.sleep(args.pause_dance)
			scrollphat.clear()

	#
	# PULSE
	#
	def pulse(self):
		'''Displays the space invader pulsing'''

		if self.args.verbose:
			print('Running SpaceInvader.pulse')
			print('Pulsing for %s times' % self.args.pulse_times)

		for i in range(0, self.args.pulse_times):
			# Arm Down
			if self.args.verbose:
				print('Setting brightness to: 10')
			scrollphat.set_brightness(10)
			self.armDownDisplay(0)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 5')
			scrollphat.set_brightness(5)
			self.armDownDisplay(0)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 3')
			scrollphat.set_brightness(3)
			self.armDownDisplay(0)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			# Arm Up
			if self.args.verbose:
				print('Setting brightness to: 10')
			scrollphat.set_brightness(10)
			self.armUpDisplay(0)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 5')
			scrollphat.set_brightness(5)
			self.armUpDisplay(0)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

			if self.args.verbose:
				print('Setting brightness to: 3')
			scrollphat.set_brightness(3)
			self.armUpDisplay(0)
			scrollphat.update()
			time.sleep(self.args.pause_pulse)
			scrollphat.clear()

	#
	# SCROLL
	#
	def scrollInSteps(self, stepNumber):
		'''Sets the columns positions from scrolling in from stepNumber'''

		if self.args.verbose:
			print('Running SpaceInvader.scrollInSteps, stepNumber: %s' %  stepNumber)

		# Arm Down
		if stepNumber == 1:
			self.armDownColumn(0, 10)

		# Arm Up
		elif stepNumber == 2:
			for i in range(0, 2):
				self.armUpColumn(i, i + 9)

		# Arm Down
		elif stepNumber == 3:
			for i in range(0, 3):
				self.armDownColumn(i, i + 8)

		# Arm Up
		if stepNumber == 4:
			for i in range(0, 4):
				self.armUpColumn(i, i + 7)

		# Arm Down
		elif stepNumber == 5:
			for i in range(0, 5):
				self.armDownColumn(i, i + 6)

		# Arm Up
		if stepNumber == 6:
			for i in range(0, 6):
				self.armUpColumn(i, i + 5)

		# Arm Down
		elif stepNumber == 7:
			for i in range(0, 7):
				self.armDownColumn(i, i + 4)

		# Arm Up
		if stepNumber == 8:
			for i in range(0, 8):
				self.armUpColumn(i, i + 3)

		# Arm Down
		elif stepNumber == 9:
			for i in range(0, 9):
				self.armDownColumn(i, i + 2)

		# Arm Up
		elif stepNumber == 10:
			for i in range(0, 10):
				self.armUpColumn(i, i + 1)

		scrollphat.update()
		time.sleep(self.args.pause_scroll)
		scrollphat.clear()

	def scrollOutSteps(self, stepNumber):
		'''Sets the columns positions from scrolling out from stepNumber'''

		if self.args.verbose:
			print('Running SpaceInvader.scrollOutSteps, stepNumber: %s' %  stepNumber)

		# Arm Up
		if stepNumber == 1:
			for i in range(1, 10):
				self.armUpColumn(i, i - 1)

		# Arm Down
		elif stepNumber == 2:
			for i in range(2, 10):
				self.armDownColumn(i, i - 2)

		# Arm Up
		elif stepNumber == 3:
			for i in range(3, 10):
				self.armUpColumn(i, i - 3)

		# Arm Down
		elif stepNumber == 4:
			for i in range(4, 10):
				self.armDownColumn(i, i - 4)

		# Arm Up
		elif stepNumber == 5:
			for i in range(5, 10):
				self.armUpColumn(i, i - 5)

		# Arm Down
		elif stepNumber == 6:
			for i in range(6, 10):
				self.armDownColumn(i, i - 6)

		# Arm Up
		elif stepNumber == 7:
			for i in range(7, 10):
				self.armUpColumn(i, i - 7)

		# Arm Down
		elif stepNumber == 8:
			for i in range(8, 10):
				self.armDownColumn(i, i - 8)

		# Arm Up
		elif stepNumber == 9:
			self.armUpColumn(9, 0)

		scrollphat.update()
		time.sleep(self.args.pause_scroll)
		scrollphat.clear()

	def scrollIn(self):
		'''Displays the space-invader scrolling in'''

		if self.args.verbose:
			print('Running SpaceInvader.scrollIn')

		for i in range(1, DEFAULT_SCROLL_DISTANCE):
			self.scrollInSteps(i)

	def scrollOut(self):
		'''Displays the space-invader scrolling out'''

		if self.args.verbose:
			print('Running SpaceInvader.scrollIn')

		#~ for i in range(1, 10):
		for i in range(1, DEFAULT_SCROLL_DISTANCE - 1):
			self.scrollOutSteps(i)

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
    print('\nStarting space-invaders...')

    #~ import pdb; pdb.set_trace()

    # Create the Class-Object
    spaceInvader = SpaceInvader(args)

    def runForFunctionName():
		'''Runs funcations from the other classes from parsed function name'''

		try:
			if args.verbose:
				print('seting brightness to: %d' % args.brightness)
				print('Running %s' % args.function)

			# Set brightness
			scrollphat.set_brightness(args.brightness)

			if args.function == 'dance':
				spaceInvader.dance()

			elif args.function == 'pulse':
				spaceInvader.pulse()

			elif args.function == 'show-arms-down':
				spaceInvader.armDownDisplay(0)
				scrollphat.update()
				time.sleep(args.pause_show)
				scrollphat.clear()

			elif args.function == 'show-arms-up':
				spaceInvader.armUpDisplay(0)
				scrollphat.update()
				time.sleep(args.pause_show)
				scrollphat.clear()

			elif args.function == 'scroll-in':
				spaceInvader.scrollIn()

			elif args.function == 'scroll-out':
				spaceInvader.scrollOut()

			elif args.function == 'scroll':
				spaceInvader.scrollIn()
				spaceInvader.armDownDisplay(0)
				scrollphat.update()
				time.sleep(args.pause_scroll)
				scrollphat.clear()
				spaceInvader.scrollOut()

			elif args.function == 'scroll-and-dance':
				spaceInvader.scrollIn()
				spaceInvader.dance()
				spaceInvader.scrollOut()

			elif args.function == 'scroll-and-pulse':
				spaceInvader.scrollIn()
				spaceInvader.pulse()
				spaceInvader.scrollOut()

			elif args.function == 'clear':
				scrollphat.clear()

			else:
				print('Function unknown: %s' % args.function)
				args.function

		except KeyboardInterrupt:
				scrollphat.clear()

    # Run script from parsed function
    runForFunctionName()

    print('\n...Finish space-invaders')

#
# PARSER
#
parser = argparse.ArgumentParser(description='Display a Space-Invader character over your scroll-pHAT from Pimoroni.')
parser.add_argument("-v", "--verbose", help="Increase output verbosity", action="store_true")

parser.add_argument('-b','--brightness', help="Set the brightness, default: %s" % DEFAULT_BRIGHTNESS, default=DEFAULT_BRIGHTNESS, type=int)
parser.add_argument('-dt','--dance_times', help="Set how many times to dance, default: %s" % DEFAULT_DANCE_TIMES, default=DEFAULT_DANCE_TIMES, type=int)
parser.add_argument('-pt','--pulse_times', help="Set how many times to pulse, default: %s" % DEFAULT_PULSE_TIMES, default=DEFAULT_PULSE_TIMES, type=int)
parser.add_argument('-pd','--pause-dance', help="Set the dance pause interval in seconds, default: %s" % DEFAULT_PAUSE_DANCE, default=DEFAULT_PAUSE_DANCE, type=float)
parser.add_argument('-pp','--pause-pulse', help="Set the pulse pause interval in seconds, default: %s" % DEFAULT_PAUSE_PULSE, default=DEFAULT_PAUSE_PULSE, type=float)
parser.add_argument('-ps','--pause-scroll', help="Set the scroll pause interval in seconds, default: %s" % DEFAULT_PAUSE_SCROLL, default=DEFAULT_PAUSE_SCROLL, type=float)
parser.add_argument('-po','--pause-show', help="Set the show pause interval in seconds, default: %s" % DEFAULT_PAUSE_SHOW, default=DEFAULT_PAUSE_SHOW, type=float)
parser.add_argument('-f','--function', help="Set the function to run ('dance', 'pulse', 'show-arms-down', 'show-arms-up', 'scroll-in', \
'scroll-out', 'scroll', 'scroll-and-dance', 'scroll-and-pulse', 'clear'), default: %s" % DEFAULT_FUNCTION_NAME, default=DEFAULT_FUNCTION_NAME, type=str)

args = parser.parse_args()

# RUN SCRIPT
__main__(args)
