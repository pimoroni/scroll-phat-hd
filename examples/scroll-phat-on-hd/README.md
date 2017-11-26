# Examples from Scroll pHAT on Scroll pHAT HD

There are a lot of example code for the discontinued 5*11 Scroll pHAT that could be ported to 7*17 Scroll pHAT HD, but this require adapting the code to benefit from the additional pixel and per pixel brightness.

A lazy way to have all of the example below quickly working on the Scroll pHAT HD is to emulate the behaviour and API of that one.

The single file scrollphat.py encapsulate in a single file the essence of the scrollphat library, but at update time, use the Scroll pHAT HD library and the inner 5*11 pixel to display what would normally appear on the Scroll pHAT, but this time on a Scroll pHAT HD.

If you copy that scrollphat.py in the same directory of a Scroll pHAT example, the use of import scrollphat will use that emulation library.

While scrollphat.py has been minimised and all the I2C code is gone, there is a scrollphat-full.py with minimal change. If you remove a few comment in that file and rename it toscrollphat.py, it is also possible to display on both screen HD and non HD pHAT simultaneously.

Brightness treatement is a bit tricky, a minimum brightness of 0.1 is choosen to make sure something is visible when not specifying a value.

scrollphat.py and all the example below come from the Scroll pHAT library on github.

# Examples

Thanks in no small part to the contributions of the buccaneers mentioned below we've amassed a library of examples to help  get you started with Scroll pHAT.

* `binary-clock.py` - A simple binary clock, by [john-root](https://github.com/john-root)
* `count.py` - Count up to a number, by [alexellis](https://github.com/alexellis)
* `cpu.py` - Display a graph of CPU usage
* `ip.py` - Display IP address, contributions from [alexellis](https://github.com/alexellis) and [andicui](https://github.com/andicui)
* `life.py` - The game of life, by [joosteto](https://github.com/joosteto)
* `localweather.py` - Display local weather info, by [alexellis](https://github.com/alexellis)
* `progress.py` - Display a progress bar, by [alexellis](https://github.com/alexellis)
* `scroll-text-forever.py` - Continuously scrolls text
* `scroll-text-once.py` - Scrolls text once, by [roguem](https://github.com/roguem)
* `scroll-text-quickstart.py` - Scrolls text without offset start
* `scroll-text-rotated.py` - Scrolls text rotated 180degrees, by [stuphi](https://github.com/stuphi)
* `scroll-text-in-my-font.py` - Scrolls some text using a custom font in the my-font.png file
* `sine.py` - Plot a sine wave
* `test-all.py` - Test pattern for all LEDs/rows/columns
* `turn-leds-off.py` - Turn off LEDs
* `ukweather.py` - Display UK weather info, by [campag](https://github.com/campag)
* `uptime.py` - Display system uptime, by [alexellis](https://github.com/alexellis)

# Contributing

Your contributions are totally welcome, will let you show off your skills, and will go a long way toward helping the next person get started.

Before you contribute:

* read through open or closed pull requests to see people's suggestions/recommendations and constructive criticism. Be ready for it!
* make sure you don't contribute something that's in progress, or already been done!
* test your code in Python 2 and Python 3
* make something awesome!
