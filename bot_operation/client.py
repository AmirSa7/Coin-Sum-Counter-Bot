from __future__ import print_function
import requests
import json
import cv2
import numpy as np

def send_image_to_flask_server(img):
    """<fix>"""

    addr = 'http://localhost:5000'
    test_url = addr + '/api/test'

    # prepare headers for http request
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}

    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img)
    # send http request with image and receive response
    response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)
    # decode response
    print(json.loads(response.text))

    # convert string of image data to uint8
    nparr = np.fromstring(response.text, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    return img, -150

    # expected output: {u'message': u'image receiveds. size=124x124'}