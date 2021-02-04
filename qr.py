"""
qr code backeground generator
written by Darren Popham, 2020
"""

import os
import time
import datetime
import json
import sys
import io
import logging

from flask import Flask, send_file, request
from flask import render_template
from flask.json import jsonify
from functools import wraps

import qrcode
from wand.image import Image, Color
from wand.display import display

import settings

def make_qr(message):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(message)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format=img.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

def convert_file(image_binary):

    with Image(blob=image_binary) as foreground:
        foreground.transform(resize="300x300")
        out = Image(width=1280, height=720, background=Color('white'))
        out.composite(foreground, left=0, top=0)
        out.format = 'PNG'
        return out

# Main Flask app
app = Flask(__name__)


@app.route('/')
def home():
   return render_template('index.html')

@app.route('/generate_background', methods=['POST'])
def background():
    try:
        message = request.form['Message']

        if message is None or message == '':
            raise Exception("Sorry, no message")

        out = convert_file(make_qr(message))
        png_image = io.BytesIO()
        out.save(file=png_image)
        png_image.seek(0)

        return send_file(
                     png_image,
                     as_attachment=True,
                     attachment_filename='background.png',
                     mimetype='image/png'
               )
    except Exception as e:
       return render_template('error.html')

# and so it begins......
if __name__ == "__main__":
    """ enable plain HTTP callback if needed """
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"

    app.secret_key = "CHANGE_ME_TO_SOME_ANNOYING_STRING"
    app.run(debug=settings.DEBUG, port=settings.PORT)

elif __name__ != "__main__":
    gunicorn_logger = logging.getLogger("gunicorn.error")
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

