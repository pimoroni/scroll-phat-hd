# Scroll pHAT HD Function Reference

Scroll pHAT HD uses white LEDs which can be brightness controlled. Note that when you set a pixel it will not immediately display on Scroll pHAT HD, you must call scrollphathd.show().

## Set A Single Pixel In Buffer

```python
scrollphathd.set_pixel(x, y, brightness)
```

Parameters:  
x – Position of pixel from left of buffer  
y – Position of pixel from top of buffer  
brightness – Intensity of the pixel, from 0.0 to 1.0 or 0 to 255  

## Write A Text String

```python
scrollphathd.write_string(string, x=0, y=0, font=None, letter_spacing=1, brightness=1.0)
```

Parameters:  
string – The string to display  
x – Offset x - distance of the string from the left of the buffer  
y – Offset y - distance of the string from the top of the buffer  
font – Font to use, default is to use the one specified with set_font  
brightness – Brightness of the pixels that compromise the text, from 0.0 to 1.0  

## Draw A Single Char

```python
scrollphathd.draw_char(x, y, char, font=None, brightness=1.0)
```

Parameters:  
x – Offset x - distance of the char from the left of the buffer  
y – Offset y - distance of the char from the top of the buffer  
char – Char to display- either an integer ordinal or a single letter  
font – Font to use, default is to use one specified with set_font  
brightness – Brightness of the pixels that compromise the char, from 0.0 to 1.0  

## Display A Graph

```python
scrollphathd.set_graph(values, low=None, high=None, brightness=1.0, x=0, y=0, width=None, height=None)
```

Parameters:  
values – A list of numerical values to display  
low – The lowest possible value (default min(values))  
high – The highest possible value (default max(values))  
brightness – Maximum graph brightness (from 0.0 to 1.0)  
x – x position of graph in display buffer (default 0)  
y – y position of graph in display buffer (default 0)  
width – width of graph in display buffer (default 17)  
height – height of graph in display buffer (default 7)  
Returns: None  

## Fill An Area

```python
scrollphathd.fill(brightness, x=0, y=0, width=0, height=0)
```

Parameters:  
brightness – Brightness of pixels  
x – Offset x - distance of the area from the left of the buffer  
y – Offset y - distance of the area from the top of the buffer  
width – Width of the area (default is 17)  
height – Height of the area (default is 7)  

## Clear An Area
```python
scrollphathd.clear_rect(x, y, width, height)
```

Parameters:  
x – Offset x - distance of the area from the left of the buffer  
y – Offset y - distance of the area from the top of the buffer  
width – Width of the area (default is 17)  
height – Height of the area (default is 7)  

## Display Buffer
All of your changes to Scroll pHAT HD are stored in a Python buffer. To display them on Scroll pHAT HD you must call scrollphthd.show().

```python
scrollphathd.show()
```

The buffer is copied, then scrolling, rotation and flip y/x transforms applied before taking a 17x7 slice and displaying.

## Clear Buffer

```python
scrollphathd.clear()
```

You must call show after clearing the buffer to update the display.

## Scroll The Buffer

```python
scrollphathd.scroll(x=0, y=0)
```

Scroll pHAT HD displays an 17x7 pixel window into the buffer, which starts at the left offset and wraps around.
The x and y values are added to the internal scroll offset. If called with no arguments, a horizontal right to left scroll is used.

Parameters:  
x – Amount to scroll on x-axis  
y – Amount to scroll on y-axis  

## Scroll To A Position

```python
scrollphathd.scroll_to(x=0, y=0)
```

Scroll pHAT HD displays a 17x7 pixel window into the buffer, which starts at the left offset and wraps around.
The x and y values set the internal scroll offset. If called with no arguments, the scroll offset is reset to 0,0

Parameters:  
x – Position to scroll to on x-axis  
y – Position to scroll to on y-axis  

## Rotate The Display

```python
scrollphathd.rotate(degrees=0)
```

Parameters:	degrees – Amount to rotate- will snap to the nearest 90 degrees


## Flip The Display

```python
scrollphathd.flip(x=False, y=False)
```

Parameters:  
x – Flip horizontally left to right  
y – Flip vertically up to down  

## Run a http API

flask must be installed before the api bluerint can be imported. 
To build up a flask api using the blueprint you can use the following and add your own blueprints to the api as you choose:

```python
from scrollphathd.api.http import scrollphathd_blueprint
from flask import Flask


app = Flask(__name__)
app.register_blueprint(scrollphathd_blueprint, url_prefix='/scrollphathd')
app.run()
```

Alternatively, with the module installed you should be able to run `python -m scrollphathd.api.http` and optionally supply `-p|--port` and `-H|--host` which will start the same api as described above.


Both options will start a http flask server with the endpoints:

* `/scrollphathd/show` - post `{"text": "helloworld"}` with the content type of the post request set to `application/json`
* `/scrollphathd/clear` - post to clear the screen
* `/scrollphathd/scroll` - post `{"x": 1,"y": 1}` to move it 1 in each direction. Content type must be set to `application/json`
* `/scrollphathd/flip` - post `{"x": "true||false", "y": "true||false"}` to flip either, both or none of the directions. 

If any data is formatted incorrectly, the blueprint api will respond with 422 (unprocessable entity) with a JSON response containing an indication of how the data was unprocessable, in the format `{"error": <string>}`.

If all was ok, you'll get a 200 response with no data.
