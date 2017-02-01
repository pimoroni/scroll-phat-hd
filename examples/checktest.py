import time
import math

import scrollphathd

speed_factor = 10

try:
    while True:
        scale = (math.sin(time.time() * speed_factor) + 1) / 2
        offset = 0
        for x in range(scrollphathd.width):
            for y in range(scrollphathd.height):
                offset += 1
                color = int(64 * scale) * (offset % 2)
                scrollphathd.pixel(x, y, color)

        scrollphathd.show()

except KeyboardInterrupt:
    scrollphathd.fill(0)
