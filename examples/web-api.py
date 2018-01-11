#!/usr/bin/env python
import scrollphathd
from scrollphathd.api.http import scrollphathd_blueprint
from flask import Flask
import os

scrollphathd.set_brightness(0.5)

if __name__ == "__main__":
    app = Flask(__name__)

    app.register_blueprint(scrollphathd_blueprint)

    @app.route('/')
    def index():
        return """<html>
<head>
<title>Scroll pHAT HD: API Demo</title>
</head>
<body>
<h1>Scroll pHAT HD: API Demo</h1>
<p>This simple API demo shows you how to blend Scroll pHAT's HTTP API blueprint into a Flask application, so you can control your Scroll pHAT HD over HTTP.</p>

<h2>Show Text</h2>
<form method="post" action="/show">
    <input type="text" name="text" value="Hello World">
    <input type="submit" value="Display">
</form>
<h2>Scroll Text</h2>

<table style="text-align:center;">
<tr><td></td><td><form method="post" action="/scroll"><input type="hidden" value="0" name="x"><input type="hidden" value="1" name="y"><input type="submit" value="Up"></form></td><td></td></tr>
<tr>
    <td><form method="post" action="/scroll"><input type="hidden" value="1" name="x"><input type="hidden" value="0" name="y"><input type="submit" value="Left"></form></td>
    <td></td>
    <td><form method="post" action="/scroll"><input type="hidden" value="-1" name="x"><input type="hidden" value="0" name="y"><input type="submit" value="Right"></form></td>
</tr>
<tr><td></td><td><form method="post" action="/scroll"><input type="hidden" value="0" name="x"><input type="hidden" value="-1" name="y"><input type="submit" value="Down"></form></td><td></td></tr>
</table>

<form method="post" action="/scroll">
    <input type="number" name="x" value="1" min="-1" max="1">
    <input type="number" name="y" value="0" min="-1" max="1">
    <input type="submit" value="Scroll">
</form>
<h2>Clear Display</h2>
<form method="post" action="/clear">
    <input type="submit" value="Clear">
</form>
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
</body>
</html>"""
    app.run(debug=True, host='0.0.0.0', port=8080)

