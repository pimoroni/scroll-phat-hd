import time
import math
from PIL import Image
import smbus
import is31fl3731

i2c = smbus.SMBus(1)
display = is31fl3731.ScrollPhatHD(i2c)

img = Image.open("ahoy.bmp")

speed_factor = 10

try:
	while True:
		for x in range(0, 17):
			for y in range(0, 7):
				v = img.getpixel((x,y))				
				display.pixel(x, 6-y, math.floor(v / 50) * 50)

		display.show()

except KeyboardInterrupt:
    display.fill(0)
