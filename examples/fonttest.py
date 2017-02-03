import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x7 as font5x7

scrollphathd.rotate(180)

for char in range(len(font5x7.data)):
    scrollphathd.draw_char(char * (1 + font5x7.width), 0, char, font=font5x7)

#scrollphathd.pixel(0,0,255)
#scrollphathd.pixel(0,1,255)
#scrollphathd.pixel(2,1,255)

#scrollphathd.pixel(22,1,255)

while True:
    scrollphathd.show()
    scrollphathd.scroll(-1,0)
    time.sleep(0.01)

