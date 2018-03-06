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
<fieldset><legend><b>Text</b></legend>
    <form method="post" action="/show"><table style='width:100%'><tr>
        <td style='width:100%'><input style='width:99%' type="text" name="text" value="Hello World"></td>
        <td><input type="submit" value="Display"></td>
    </tr></table></form>
</fieldset><fieldset><legend><b>Scroll</b></legend>
    <div>
        <p>Scroll by Arrows</p><table style="text-align:center"><tr>
            <td></td><td><form method="post" action="/scroll"><input type="hidden" value="0" name="x"><input type="hidden" value="1" name="y"><input type="submit" value="Up"></form></td><td></td>
        </tr><tr>
            <td><form method="post" action="/scroll"><input type="hidden" value="1" name="x"><input type="hidden" value="0" name="y"><input type="submit" value="Left"></form></td><td></td><td><form method="post" action="/scroll"><input type="hidden" value="-1" name="x"><input type="hidden" value="0" name="y"><input type="submit" value="Right"></form></td>
        </tr><tr>
            <td></td><td><form method="post" action="/scroll"><input type="hidden" value="0" name="x"><input type="hidden" value="-1" name="y"><input type="submit" value="Down"></form></td><td></td>
        </tr></table>
    </div><div>
        <p>Scroll by Coordinates</p><form method="post" action="/scroll">
            X: <input style='width:40px' type="number" name="x" value="1" min="-1" max="1">
            Y: <input style='width:40px' type="number" name="y" value="0" min="-1" max="1">
            <input type="submit" value="Scroll">
        </form>
    </div><div>
        <p>Auto Scroll</p><form method="post" action="/autoscroll"><table style="text-align:center"><tr>
            <td><input type="radio" id="autoscroll_disabled" name="is_enabled" value="False" checked><label for="autoscroll_disabled">Disabled</label><input type="radio" id="autoscroll_enabled" name="is_enabled" value="True"><label for="autoscroll_enabled">Enabled</label></td><td rowspan="2"><input type="submit" value="Set"></td>
        </tr><tr>
            <td>Interval: <input style='width:50px' type="number" name="interval" value="0.1" min="0.1" max="5" step="0.1"></td>
        </tr></form></table>
    </div>
</fieldset><fieldset><legend><b>Display</b></legend>
    <form method="post" action="/clear"><input type="submit" value="Clear"></form>
</fieldset>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
<script type="text/javascript">
$(function(){
    $('form').submit(function(e){
        e.preventDefault();
        $.post($(this).attr('action'), $(this).serialize(), function(result){console.log(result);});
        return false;
    });
})
</script>
</body></html>"""
    app.run(debug=True, host='0.0.0.0', port=8080)
