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

.. currentmodule:: scrollphathd

At A Glance
-----------

.. automoduleoutline:: scrollphathd
   :members:

.. toctree::
   :titlesonly:
   :maxdepth: 0

Set A Single Pixel In Buffer
----------------------------

Scroll pHAT HD uses white LEDs which can be brightness controlled.

When you set a pixel it will not immediately display on Scroll pHAT HD, you must call :python:`scrollphathd.show()`.

.. autofunction:: scrollphathd.set_pixel
   :noindex:

Write A Text String
-------------------

.. autofunction:: scrollphathd.write_string
   :noindex:

Draw A Single Char
------------------

.. autofunction:: scrollphathd.draw_char
   :noindex:

Display A Graph
---------------

.. autofunction:: scrollphathd.set_graph
   :noindex:

Fill An Area
------------

.. autofunction:: scrollphathd.fill
   :noindex:

Clear An Area
-------------

.. autofunction:: scrollphathd.clear_rect
   :noindex:

Display Buffer
--------------

All of your changes to Scroll pHAT HD are stored in a Python buffer. To display them
on Scroll pHAT HD you must call :python:`scrollphathd.show()`.

.. autofunction:: scrollphathd.show
   :noindex:

Clear Buffer
------------

.. autofunction:: scrollphathd.clear
   :noindex:

Scroll The Buffer
-----------------

.. autofunction:: scrollphathd.scroll
   :noindex:

Scroll To A Position
--------------------

.. autofunction:: scrollphathd.scroll_to
   :noindex:

Rotate The Display
------------------

.. autofunction:: scrollphathd.rotate
   :noindex:

Flip The Display
----------------

.. autofunction:: scrollphathd.flip
   :noindex:

Get The Display Size
--------------------

.. autofunction:: scrollphathd.get_shape
   :noindex:

Get The Buffer Size
-------------------

.. autofunction:: scrollphathd.get_buffer_shape
   :noindex:
