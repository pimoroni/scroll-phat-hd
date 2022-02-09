# Scroll pHAT HD Simulator

A Tk based server to simulate Scroll pHAT HD on your Windows, Linux or macOS PC.

![Swirl running in Scroll pHAT HD simulator](simulator.gif)

Works by hijacking the `smbus` module imported by `scrollphathd` and replacing it with a FIFO pipe to the Tk based simulator.

## Usage

Set the `PYTHONPATH` variable to the simulator directory and run an example. The fake `smbus` will be loaded instead of the real one and output will launch in a new window:

```
PYTHONPATH=simulator python3 examples/clock.py
```
