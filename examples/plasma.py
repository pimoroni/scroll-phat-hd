import time
import math

import scrollphathd

speed_factor = 10

i = 0
while True:
    i += 2
    s = math.sin(i / 50.0) * 2.0 + 6.0
    print(s)
    for x in range(0, 17):
        for y in range(0, 7):
            v = 128.0 + (128.0 * math.sin((x * s) + i / 4.0) * math.cos((y * s) + i / 4.0))

            scrollphathd.pixel(x, y, v)

    time.sleep(0.01)
    scrollphathd.show()
