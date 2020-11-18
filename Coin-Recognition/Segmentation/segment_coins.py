
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

print('torch.__version__ = ', torch.__version__, '|', 'Using CUDA = ', torch.cuda.is_available())


im = cv2.imread('Coin-Recognition/Segmentation/images/cv2_test.jpg')
cv2.imshow('OpenCV test',im)


cfg = get_cfg()
# add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
cfg.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
# Find a model from detectron2's model zoo. You can use the https://dl.fbaipublicfiles... url as well
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml")
predictor = DefaultPredictor(cfg)
outputs = predictor(im)

print('A')

# look at the outputs. See https://detectron2.readthedocs.io/tutorials/models.html#model-output-format for specification
print(outputs["instances"].pred_classes)
print(outputs["instances"].pred_boxes)

print('B')


# We can use `Visualizer` to draw the predictions on the image.
v = Visualizer(im[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
out = v.draw_instance_predictions(outputs["instances"].to("cpu"))
cv2.imshow('Original Segmentation test', out.get_image()[:, :, ::-1])

print('C')

print('done with original network, now continue with our own...')

cfg2 = get_cfg()
cfg2.merge_from_file(model_zoo.get_config_file("COCO-InstanceSegmentation/mask_rcnn_R_50_FPN_3x.yaml"))
cfg2.MODEL.ROI_HEADS.NUM_CLASSES = 1

# Inference should use the config with parameters that are used in training
# cfg now already contains everything we've set previously. We changed it a little bit for inference:
cfg2.MODEL.WEIGHTS = './Coin-Recognition/Segmentation/models/model_final.pth'  # path to the model we just trained
cfg2.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.7   # set a custom testing threshold
predictor = DefaultPredictor(cfg2)

print('D')

im2 = cv2.imread('Coin-Recognition/Segmentation/images/seg_test.jpg')
cv2.imshow('Before Segmentation',im2)


print('E')

t1 = time.time()
outputs2 = predictor(im2)
v = Visualizer(im2[:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
out2 = v.draw_instance_predictions(outputs2["instances"].to("cpu"))
cv2.imshow('After Segmentation', out2.get_image()[:, :, ::-1])
t2 = time.time()
k = cv2.waitKey(0) & 0xFF
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()


print('Done.', 'speed = ', str(int(t2 - t1)))

# curr_dir = 'Segmentation/'
# url = 'http://images.cocodataset.org/val2017/000000439715.jpg'
# fileName = wget.download(url, out=curr_dir)
# print(fileName)
# img = cv2.imread('Segmentation/000000439715.jpg', 0)
# cv2.imshow('test img', img)




