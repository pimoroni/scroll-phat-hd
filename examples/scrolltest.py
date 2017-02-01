import time

import scrollphathd

scrollphathd.pixel(0,0,64)

try:
    while True:
        scrollphathd.scroll(-1,-1)
        scrollphathd.show()
        time.sleep(0.1)
except KeyboardInterrupt:
    scrollphathd.fill(0)
    scrollphathd.show()
