import time
import scrollphathd

while True:
    for y in range(7):
        for x in range(11):
            scrollphathd.set_pixel(x, y, 0.3)
        scrollphathd.show()
        time.sleep(0.1)
    time.sleep(0.2)
    for y in range(7):
        for x in range(11):
            scrollphathd.set_pixel(x, 6 - y, 0)
        scrollphathd.show()
        time.sleep(0.1)

    for x in range(11):
        for y in range(7):
            scrollphathd.set_pixel(x, y, 0.3)
        scrollphathd.show()
        time.sleep(0.1)
    time.sleep(0.2)
    for x in range(11):
        for y in range(7):
            scrollphathd.set_pixel(x, 6 - y, 0)
        scrollphathd.show()
        time.sleep(0.1)
