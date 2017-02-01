import time
import math
from PIL import Image
import scrollphathd

img = Image.open("ahoy.bmp")

speed_factor = 10

try:
	while True:
		for x in range(0, 17):
			for y in range(0, 7):
				v = img.getpixel((x,y))				
				scrollphathd.pixel(x, 6-y, math.floor(v / 50) * 50)

		scrollphathd.show()

except KeyboardInterrupt:
    scrollphathd.fill(0)
