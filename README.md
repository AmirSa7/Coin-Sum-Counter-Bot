# Coin-Sum-Counter-Bot
## Description
This project is a Telegram bot service. The user sends to the bot a picture of a collection of coins scattered on a table. The bot responds the amount of money in the picture.
This project is currently in development.

This bot can run on AWS:

<img src="https://github.com/AmirSa7/Coin-Sum-Counter-Bot/blob/main/Figures/System-Block-Diagram-AWS.jpg" width="500"></a>

or efficiently on a local Nvidia Jetson:

<img src="https://github.com/AmirSa7/Coin-Sum-Counter-Bot/blob/main/Figures/System-Block-Diagram-Jetson.jpg" width="500"></a>

## References
### Bot API
- Python Telegram Bot: [GitHub](https://github.com/python-telegram-bot/python-telegram-bot)
### The deep recognition (detection / segmentation) was implemted based on the following examples
Detectron2:
- Torchvision object detection finetune tutorial: [Pytorch](https://pytorch.org/tutorials/intermediate/torchvision_tutorial.html)
- Detectron2 Beginner's Tutorial (Colab, Baloon): [Colab](https://colab.research.google.com/drive/16jcaJoc6bCFAQ96jDe2HwtXj7BMD_-m5)
- Detectron2 Beginner's Tutorial (Colab, Blood): [Colab](https://colab.research.google.com/drive/1-TNOcPm3Jr3fOJG8rnGT9gh60mHUsvaW#scrollTo=kc8MmgZugZWR)
- Object Detection in 6 steps using Detectron2: [Article](https://towardsdatascience.com/object-detection-in-6-steps-using-detectron2-705b92575578)

OpenCV:
- Simple and effective coin segmentation using Python and OpenCV: [Article](https://blog.christianperone.com/2014/06/simple-and-effective-coin-segmentation-using-python-and-opencv/)
- OpenCV-Python image segmentation and Watershed algorithm: [Article](https://www.programmersought.com/article/92784407251/)

### The annotation of the data was made using the following tools
- Labelme annotation tool: [GitHub](https://github.com/wkentaro/labelme)
- COCO Anotator tool:  [GitHub](https://github.com/jsbroks/coco-annotator)

Additional sources:
- Create COCO Annotations From Scratch:  [Article](https://www.immersivelimit.com/tutorials/create-coco-annotations-from-scratch)
- How to create custom COCO data set for instance segmentation:  [Article](https://www.dlology.com/blog/how-to-create-custom-coco-data-set-for-instance-segmentation/)




