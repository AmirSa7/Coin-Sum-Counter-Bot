#!/usr/bin/python3

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import Flask, request, Response

import argparse
import sys

from utils.utils import *
from recognition.processing.process_image import process_image


# Initialize the Flask applications
app = Flask(__name__)

# route http posts to this method
@app.route('/bot/imagedata', methods=['POST'])
def test():

    print("--> image was recieved from client <---")
    
    ndarrayImg = extract_data_from_request(request.data)
    processedImage, coinSum = process_image(ndarrayImg)
    postObject = prepare_data_for_request(processedImage)

    # build a response dict to send back to client
    response = {'message': postObject}

    print("--> answer was sent to client <---")
    return Response(response=postObject, status=200, mimetype="application/json")

# start flask app
app.run(host="0.0.0.0", port=5000)
