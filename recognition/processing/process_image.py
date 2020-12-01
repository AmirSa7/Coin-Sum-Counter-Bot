import cv2
import numpy as np

import jetson.inference
import jetson.utils
import sys

# load the object detection network
net = jetson.inference.detectNet("ssd-mobilenet-v2", sys.argv, 0.5)


def process_image_using_TensorRT(ndarrayImg):
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

    # make sure the GPU is done work before we convert to cv2
    jetson.utils.cudaDeviceSynchronize()

    # convert to cv2 image (cv2 images are numpy arrays)
    cv_img = jetson.utils.cudaToNumpy(bgr_img)
    return cv_img, -200


def process_image(img: np.ndarray) -> (np.ndarray, int):
    """<fix>"""

    proccessedImg, coinSum = process_image_using_TensorRT(img) # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # for testingz
    return (proccessedImg, coinSum)
