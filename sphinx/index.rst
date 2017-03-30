.. role:: python(code)
   :language: python

Welcome
-------

This documentation will guide you through the methods available in the Scroll pHAT HD python library.

Scroll pHAT provides a matrix of 119 individually brightness controlled white LED pixels that is ideal for writing messages, showing graphs, and drawing pictures. Use it to output your IP address, show CPU usage, or just play pong!

* More information - https://shop.pimoroni.com/products/scroll-phat-hd
* Get the code - https://github.com/pimoroni/scroll-phat-hd
* GPIO pinout - https://pinout.xyz/pinout/scroll_phat_hd
* Soldering - https://learn.pimoroni.com/tutorial/sandyj/soldering-phats
* Get help - http://forums.pimoroni.com/c/support

.. currentmodule:: scrollphathd.is31fl3731

At A Glance
-----------

.. autoclassoutline:: scrollphathd.is31fl3731.Matrix
   :members:

.. toctree::
   :titlesonly:
   :maxdepth: 0

Set A Single Pixel In Buffer
----------------------------

Scroll pHAT HD uses white LEDs which can be brightness controlled.

When you set a pixel it will not immediately display on Scroll pHAT HD, you must call :python:`scrollphathd.show()`.

.. automethod:: scrollphathd.is31fl3731.Matrix.set_pixel
   :noindex:

Write A Text String
-------------------

.. automethod:: scrollphathd.is31fl3731.Matrix.write_string
   :noindex:

Draw A Single Char
------------------

.. automethod:: scrollphathd.is31fl3731.Matrix.draw_char
   :noindex:

Display A Graph
---------------

.. automethod:: scrollphathd.is31fl3731.Matrix.set_graph
   :noindex:

Fill An Area
------------

.. automethod:: scrollphathd.is31fl3731.Matrix.fill
   :noindex:

Clear An Area
-------------

.. automethod:: scrollphathd.is31fl3731.Matrix.clear_rect
   :noindex:

Display Buffer
--------------

All of your changes to Scroll pHAT HD are stored in a Python buffer. To display them
on Scroll pHAT HD you must call :python:`scrollphathd.show()`.

.. automethod:: scrollphathd.is31fl3731.Matrix.show
   :noindex:

Clear Buffer
------------

.. automethod:: scrollphathd.is31fl3731.Matrix.clear
   :noindex:

Scroll The Buffer
-----------------

.. automethod:: scrollphathd.is31fl3731.Matrix.scroll
   :noindex:

Scroll To A Position
--------------------

.. automethod:: scrollphathd.is31fl3731.Matrix.scroll_to
   :noindex:

Rotate The Display
------------------

.. automethod:: scrollphathd.is31fl3731.Matrix.rotate
   :noindex:

Flip The Display
----------------

.. automethod:: scrollphathd.is31fl3731.Matrix.flip
   :noindex:

Get The Display Size
--------------------

.. automethod:: scrollphathd.is31fl3731.Matrix.get_shape
   :noindex:

Get The Buffer Size
-------------------

.. automethod:: scrollphathd.is31fl3731.Matrix.get_buffer_shape
   :noindex:
