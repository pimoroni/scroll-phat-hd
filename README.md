![Scroll pHAT HD](scroll-phat-hd-logo.png)
https://shop.pimoroni.com/products/scroll-phat-hd

https://shop.pimoroni.com/products/scroll-hat-mini

17x7 pixels of single-colour, brightness-controlled, message scrolling goodness! This library will work with Scroll pHAT HD and Scroll HAT Mini.

## Installing

### Full install (recommended):

We've created an easy installation script that will install all pre-requisites and get your Scroll pHAT HD
up and running with minimal efforts. To run it, fire up Terminal which you'll find in Menu -> Accessories -> Terminal
on your Raspberry Pi desktop, as illustrated below:

![Finding the terminal](http://get.pimoroni.com/resources/github-repo-terminal.png)

In the new terminal window type the command exactly as it appears below (check for typos) and follow the on-screen instructions:

```bash
curl https://get.pimoroni.com/scrollphathd | bash
```

Alternatively, on Raspbian, you can download the `pimoroni-dashboard` and install your product by browsing to the relevant entry:

```bash
sudo apt-get install pimoroni
```
(you will find the Dashboard under 'Accessories' too, in the Pi menu - or just run `pimoroni-dashboard` at the command line)

If you choose to download examples you'll find them in `/home/pi/Pimoroni/scrollphathd/`.

### Manual install:

#### Library install for Python 3:

on Raspbian:

```bash
sudo apt-get install python3-scrollphathd
```

other environments: 

```bash
sudo pip3 install scrollphathd
```

#### Library install for Python 2:

on Raspbian:

```bash
sudo apt-get install python-scrollphathd
```

other environments: 

```bash
sudo pip2 install scrollphathd
```

### Development:

If you want to contribute, or like living on the edge of your seat by having the latest code, you should clone this repository, `cd` to the library directory, and run:

```bash
sudo python3 setup.py install
```
(or `sudo python setup.py install` whichever your primary Python environment may be)

In all cases you will have to enable the i2c bus.

## Alternative Libraries

* Node JS library by @whatsim - https://github.com/whatsim/scrollcontroller

## Documentation & Support

* Guides and tutorials - https://learn.pimoroni.com/scroll-phat-hd
* Function reference - http://docs.pimoroni.com/scrollphathd/
* GPIO Pinout - https://pinout.xyz/pinout/scroll_phat_hd
* Get help - http://forums.pimoroni.com/c/support

## Unofficial / Third-party libraries

* Java library by Jim Darby - https://github.com/hackerjimbo/PiJava
* Rust library by Tiziano Santoro - https://github.com/tiziano88/scroll-phat-hd-rs
* Go library by Tom Mitchell - https://github.com/tomnz/scroll-phat-hd-go
