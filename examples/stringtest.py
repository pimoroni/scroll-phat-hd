import time
import signal

import scrollphathd
from scrollphathd.fonts import font5x7 as font5x7

scrollphathd.rotate(180)

scrollphathd.write_string("Hello World! ", x=0, y=0, font=font5x7)

#scrollphathd.pixel(0,0,255)
#scrollphathd.pixel(0,1,255)
#scrollphathd.pixel(2,1,255)

#scrollphathd.pixel(22,1,255)

while True:
    scrollphathd.show()
    scrollphathd.scroll(-1,0)
    time.sleep(0.05)

