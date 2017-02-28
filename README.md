![Scroll pHAT HD](scroll-phat-hd-logo.png)

17x7 pixels of single-colour, brightness-controlled, message scrolling goodness!

https://shop.pimoroni.com/products/scroll-phat-hd

##Installing

**Full install ( recommended ):**

We've created a super-easy installation script that will install all pre-requisites and get your Scroll pHAT HD up and running in a jiffy. To run it fire up Terminal which you'll find in Menu -> Accessories -> Terminal on your Raspberry Pi desktop like so:

![Finding the terminal](terminal.jpg)

In the new terminal window type the following and follow the instructions:

```bash
curl -sS https://get.pimoroni.com/scrollphathd | bash
```

If you choose to download examples you'll find them in `/home/pi/Pimoroni/scrollphathd/`.

**Library install for Python 3:**

```bash
sudo pip3 install scrollphathd
```

**Library install for Python 2:**

```bash
sudo pip2 install scrollphathd
```

In all cases you will have to enable the i2c bus.

##Documentation & Support

* Getting started - https://learn.pimoroni.com/tutorial/sandyj/soldering-phats
* Function reference - http://docs.pimoroni.com/scrollphathd/
* GPIO Pinout - https://pinout.xyz/pinout/scroll_phat_hd
* Get help - http://forums.pimoroni.com/c/support
