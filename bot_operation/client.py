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
    url = addr + '/bot/imagedata'

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    postObject = prepare_data_for_request(img)

    print("--> image was sent to server <---")
    response = requests.post(url, data=postObject, headers=headers)
    print("--> answer was recieved from server <---")

    responseImage = extract_data_from_request(response.content)

    return responseImage, -150
