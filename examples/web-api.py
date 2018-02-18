#!/usr/bin/env python
import scrollphathd
from scrollphathd.api.http import scrollphathd_blueprint
from scrollphathd.fonts import font3x5
from flask import Flask
import os

# Set the font
scrollphathd.set_font(font3x5)
# Set the brightness
scrollphathd.set_brightness(0.5)
# Uncomment the below if your display is upside down
#   (e.g. if you're using it in a Pimoroni Scroll Bot)
#scrollphathd.rotate(degrees=180)

if __name__ == "__main__":
    app = Flask(__name__)

    app.register_blueprint(scrollphathd_blueprint)

    @app.route('/')
    def index():
        return """<html><head><title>Scroll pHAT HD - API Demo</title></head><body>
<h1>Scroll pHAT HD - API Demo</h1>
<p>This simple API demo shows you how to blend Scroll pHAT's HTTP API blueprint into a Flask application, so you can control your Scroll pHAT HD over HTTP.</p>
<fieldset><legend><b>Input</b></legend>
    <form method="post" action="/show">
        <div><p>Text:</p><input style='width:100%' type="text" name="text" value="Hello World"></div>
        <div><p>Auto Scroll:</p>
            <input type="radio" id="auto_scroll_disabled" name="auto_scroll" value="False" checked><label for="auto_scroll_disabled">Disabled</label>
            <input type="radio" id="auto_scroll_enabled" name="auto_scroll" value="True"><label for="auto_scroll_enabled">Enabled</label>
        </div>
        <div><br /><input type="submit" value="Display"></div>
    </form>
</fieldset><fieldset><legend><b>Manual Scroll</b></legend>
    <div>
        <p>Scroll by Arrows:</p><table style="text-align:center;"><tr>
            <td></td><td><form method="post" action="/scroll"><input type="hidden" value="0" name="x"><input type="hidden" value="1" name="y"><input type="submit" value="Up"></form></td><td></td>
        </tr><tr>
            <td><form method="post" action="/scroll"><input type="hidden" value="1" name="x"><input type="hidden" value="0" name="y"><input type="submit" value="Left"></form></td><td></td><td><form method="post" action="/scroll"><input type="hidden" value="-1" name="x"><input type="hidden" value="0" name="y"><input type="submit" value="Right"></form></td>
        </tr><tr>
            <td></td><td><form method="post" action="/scroll"><input type="hidden" value="0" name="x"><input type="hidden" value="-1" name="y"><input type="submit" value="Down"></form></td><td></td>
        </tr></table>
    </div><div>
        <p>Scroll by Coordinates:</p><form method="post" action="/scroll">
            X: <input style='width:40px' type="number" name="x" value="1" min="-1" max="1">
            Y: <input style='width:40px' type="number" name="y" value="0" min="-1" max="1">
            <input type="submit" value="Scroll">
        </form>
    </div>
</fieldset><fieldset><legend><b>Display</b></legend>
    <form method="post" action="/clear"><br /><input type="submit" value="Clear"></form>
</fieldset>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script type="text/javascript">
$(function(){
    $('form').submit(function(e){
        e.preventDefault();

        $.post($(this).attr('action'), $(this).serialize(), function(result){
            console.log(result);
        });

        return false;
    });
})
</script>
</body></html>"""
    app.run(debug=True, host='0.0.0.0', port=8080)
