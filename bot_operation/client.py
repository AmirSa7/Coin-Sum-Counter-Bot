from __future__ import print_function

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import requests
import json
import cv2
import numpy as np

from utils.utils import *

def send_image_to_flask_server(img):
    """<fix>"""

    addr = 'http://localhost:5000'
    test_url = addr + '/api/test'

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    # encode image as jpeg
    img_encoded = encode_image_as_jpeg(img)
    # send http request with image and receive response
    print("--> image was sent <---")
    response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
    print("--> image was recieved <---")
    # convert string of image data to uint8
    uint88 = convert_string_image_to_uint8(response.content)
    # decode image
    img = cv2.imdecode(uint88, cv2.IMREAD_COLOR)
    print('---> Client Done <---')

    return img, -150

    # expected output: {u'message': u'image receiveds. size=124x124'}