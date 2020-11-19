
# Some basic setup:
# Setup detectron2 logger
import torch, torchvision
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()

# import some common libraries
import numpy as np
import os, json, random, time
import wget
import cv2

# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog

def print_useful_information() -> None:
    """<fix>"""
    print('torch.__version__ = ', torch.__version__, '|', 'Using CUDA = ', torch.cuda.is_available())


def load_and_display_image(imagePath: str, windowTitle: str):
    """<fix>"""
    img = cv2.imread(imagePath)
    cv2.imshow(windowTitle ,img)
    return img


def load_and_display_cv2_test_image() -> None:
    """<fix>"""
    imagePath = 'Coin-Recognition/Segmentation/images/cv2_test.jpg'
    windowTitle = 'OpenCV test'
    cv2TestImage = load_and_display_image(imagePath, windowTitle)
    return cv2TestImage


def load_and_display_recognition_test_image() -> None:
    """<fix>"""
    imagePath = 'Coin-Recognition/Segmentation/images/seg_test.jpg'
    windowTitle = 'Recognition test'
    RecTestImage = load_and_display_image(imagePath, windowTitle)
    return RecTestImage


def create_configuration_instance():
    """<fix>"""
    cfg = get_cfg()
    return cfg


def edit_configuration_parameters(cfg) -> None:
    """<fix>"""
    # see optional networks: https://github.com/facebookresearch/detectron2/blob/master/detectron2/model_zoo/model_zoo.py
    cfg.merge_from_file(model_zoo.get_config_file("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml"))
    cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
    cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-Detection/faster_rcnn_R_50_FPN_3x.yaml")


def creat_a_predictor(cfg):
    """<fix>"""
    predictor = DefaultPredictor(cfg)
    return predictor

def apply_predictor_on_image_to_get_results(predictor, img):
    """<fix>"""
    # See https://detectron2.readthedocs.io/tutorials/models.html#model-output-format
    outputs = predictor(img)
    return outputs

def print_prediction_classes_and_boxes(outputs) -> None:
    """<fix>"""
    print(outputs["instances"].pred_classes)
    print(outputs["instances"].pred_boxes)

def draw_predictions_on_the_image(vis, outputs):
    """<fix>"""
    decoratedImage = vis.draw_instance_predictions(outputs["instances"].to("cpu"))
    return decoratedImage

def show_decorated_image(vis, outputs) -> None:
    """<fix>"""
    decoratedImage = draw_predictions_on_the_image(vis, outputs)
    cv2.imshow('Decorated Image', decoratedImage.get_image()[:, :, ::-1])

def main():

    print_useful_information()

    # cv2TestImage = load_and_display_cv2_test_image()

    # cfg = create_configuration_instance()
    # edit_configuration_parameters(cfg)
    # predictor = creat_a_predictor(cfg)
    # t1 = time.time()
    # outputs = apply_predictor_on_image_to_get_results(predictor, cv2TestImage)
    # t2 = time.time()
    # print('A')
    # print_prediction_classes_and_boxes(outputs)
    # print('B')
    # vis = Visualizer(cv2TestImage[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1)
    # show_decorated_image(vis, outputs)
    # print('C')

    RecTestImage = load_and_display_recognition_test_image()

    cfg2 = get_cfg()
    cfg2.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
    cfg2.MODEL.ROI_HEADS.NUM_CLASSES = 1

    if torch.cuda.is_available():
        cfg2.MODEL.DEVICE = "cuda"

    # Inference should use the config with parameters that are used in training
    # cfg now already contains everything we've set previously. We changed it a little bit for inference:
    t0 = time.time()
    cfg2.MODEL.WEIGHTS = './Coin-Recognition/Segmentation/models/model_final.pth'  # path to the model we just trained
    cfg2.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
    predictor = DefaultPredictor(cfg2)
    t00 = time.time()
    print('D', 'speed = ', str(int(t00 - t0)))

    t1 = time.time()
    outputs2 = predictor(RecTestImage)
    print('E')
    v = Visualizer(RecTestImage[:, :, ::-1], MetadataCatalog.get(cfg2.DATASETS.TRAIN[0]), scale=1.2)
    out2 = v.draw_instance_predictions(outputs2["instances"].to("cpu"))
    cv2.imshow('After Segmentation', out2.get_image()[:, :, ::-1])
    t2 = time.time()
    k = cv2.waitKey(0) & 0xFF
    print('F')
    if k == 27:         # wait for ESC key to exit
        cv2.destroyAllWindows()

    print('Done.', 'speed = ', str(int(t2 - t1)))

    # curr_dir = 'Segmentation/'
    # url = 'http://images.cocodataset.org/val2017/000000439715.jpg'
    # fileName = wget.download(url, out=curr_dir)
    # print(fileName)
    # img = cv2.imread('Segmentation/000000439715.jpg', 0)
    # cv2.imshow('test img', img)


if __name__ == '__main__':
    main()





