# import some common libraries
import numpy as np
import os, json, random, time
import cv2

import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib as mpl


### Type Cnoverters ###

def convert_string_image_to_uint8(stringImg: str):
    arrayImg = np.fromstring(stringImg, np.uint8)
    print(type(arrayImg))
    return arrayImg


def convert_array_image_to_ndarray(arrayImg: np.array):
    ndarrayImg = cv2.imdecode(arrayImg, cv2.IMREAD_COLOR)
    print(type(ndarrayImg))
    return ndarrayImg


def encode_image_as_jpeg(ndarrayImg: np.ndarray):
    _, jpegImg = cv2.imencode('.jpg', ndarrayImg)
    print(type(jpegImg))
    return jpegImg


def convert_jpeg_image_to_string(jpegImg):
    stringImg = jpegImg.tostring()
    print(type(stringImg))
    return stringImg


### GUI & Testing ###

def load_image_from_file(imagePath: str) -> np.ndarray:
    """<fix>"""
    img = cv2.imread(imagePath)
    assert img is not None, "Unable to load image."
    # if not img:      # always check for None
    #     raise ValueError("Unable to load image.")
    return img

def show_image_for_one_second(img: np.ndarray):
    """<fix>"""
    cv2.imshow('image',img)
    cv2.waitKey(1000)
    cv2.destroyAllWindows()
    

def load_last_recieved_image():
    """<fix>"""
    imagePath = 'Bot-Operation/Recieved-Images/last_image.jpg'
    img = load_image_from_file(imagePath)
    show_image_for_one_second(img)
    return img