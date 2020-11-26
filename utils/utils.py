# import some common libraries
import numpy as np
import os, json, random, time
import cv2

import tempfile
os.environ['MPLCONFIGDIR'] = tempfile.mkdtemp()
import matplotlib as mpl

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