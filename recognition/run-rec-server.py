#!/usr/bin/python3

import sys, os, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

from processing.process_image import process_image

import jetson.inference
import jetson.utils

import argparse
import sys

from utils.utils import *


# Initialize the Flask applications
app = Flask(__name__)


# load the object detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", sys.argv, 0.5)



# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():

    stringImg = request.data
    arrayImg = convert_string_image_to_uint8(stringImg)
    ndarrayImg = convert_array_image_to_ndarray(arrayImg)

    # convert to CUDA (cv2 images are numpy arrays, in BGR format)
    bgr_img = jetson.utils.cudaFromNumpy(ndarrayImg, isBGR=True)

    # convert from BGR -> RGB
    rgb_img = jetson.utils.cudaAllocMapped(width=bgr_img.width,
                                    height=bgr_img.height,
                                    format='rgb8')

    jetson.utils.cudaConvertColor(bgr_img, rgb_img)

    
    detections = net.Detect(rgb_img, overlay="box,labels,conf")
    # print the detections
    print("detected {:d} objects in image".format(len(detections)))
    
    for detection in detections:
        print(detection)


	# print out performance info
    net.PrintProfilerTimes()


    # convert to BGR, since that's what OpenCV expects
    bgr_img = jetson.utils.cudaAllocMapped(width=rgb_img.width,
                                    height=rgb_img.height,
                                    format='bgr8')

    jetson.utils.cudaConvertColor(rgb_img, bgr_img)

    print('BGR image: ')
    print(bgr_img)

    # make sure the GPU is done work before we convert to cv2
    jetson.utils.cudaDeviceSynchronize()

    # convert to cv2 image (cv2 images are numpy arrays)
    cv_img = jetson.utils.cudaToNumpy(bgr_img)



    processedImage, coinSum = process_image(cv_img)

    jpegImg = encode_image_as_jpeg(processedImage)
    stringImg = convert_jpeg_image_to_string(jpegImg)

    # build a response dict to send back to client
    response = {'message': stringImg}

    return Response(response=stringImg, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)
