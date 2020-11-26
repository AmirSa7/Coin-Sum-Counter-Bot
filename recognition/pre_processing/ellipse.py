# import numpy as np
# import cv2

# def load_image_from_file(imagePath: str) -> np.ndarray:
#     """<fix>"""
#     img = cv2.imread(imagePath)
#     assert img is not None, "Unable to load image."
#     # if not img:      # always check for None
#     #     raise ValueError("Unable to load image.")
#     return img

# def run_main():

#     frame = load_image_from_file('./NIS-Dataset-Example/images/NIS_003.jpg')
#     roi = frame
#     gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
#     gray_blur = cv2.GaussianBlur(gray, (21, 21), 0)
#     thresh = cv2.adaptiveThreshold(gray_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                     cv2.THRESH_BINARY_INV, 11, 1)
#     kernel = np.ones((3, 3), np.uint8)
#     kernel[0][0] = 0
#     kernel[0][2] = 0
#     kernel[2][0] = 0
#     kernel[2][2] = 0

#     openning = cv2.morphologyEx(thresh, cv2.MORPH_OPEN,
#     kernel, iterations=1)

#     closing = cv2.morphologyEx(openning, cv2.MORPH_CLOSE,
#     kernel, iterations=1)

#     openning = cv2.morphologyEx(closing, cv2.MORPH_OPEN,
#     kernel, iterations=1)

#     closing = cv2.morphologyEx(openning, cv2.MORPH_ERODE,
#     kernel, iterations=1)



#     cont_img = closing.copy()
#     contours, hierarchy = cv2.findContours(cont_img, cv2.RETR_EXTERNAL,
#                                             cv2.CHAIN_APPROX_SIMPLE)
#     for cnt in contours:
#         area = cv2.contourArea(cnt)
#         if area < 2000 or area > 8000:
#             continue
#         if len(cnt) < 10:
#             continue
#         ellipse = cv2.fitEllipse(cnt)
#         cv2.ellipse(roi, ellipse, (0,255,0), 2)
#     cv2.imshow("Morphological Closing", closing)
#     cv2.imshow("Adaptive Thresholding", thresh)
#     cv2.imshow('Contours', roi)
#     if cv2.waitKey(0) & 0xFF == ord('q'):
#         cv2.destroyAllWindows()

# if __name__ == "__main__":
#     run_main()




import numpy as np
import cv2
from matplotlib import pyplot as plt


def load_image_from_file(imagePath: str) -> np.ndarray:
    """<fix>"""
    img = cv2.imread(imagePath)
    assert img is not None, "Unable to load image."
    # if not img:      # always check for None
    #     raise ValueError("Unable to load image.")
    return img


img = load_image_from_file('./NIS-Dataset-Example/images/NIS_003.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV, cv2.THRESH_OTSU)

# Noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
 # Determine the background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)
 # Find foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
 # Find unknown area
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)

# Category tag
ret, markers = cv2.connectedComponents(sure_fg)
 # Add 1 to all tags, make sure the background is 0 instead of 1.
markers = markers + 1
 # Now let all unknown areas be 0
markers[unknown==255] = 0

markers = cv2.watershed(img,markers) 
img[markers == -1] = [255,0,0]


cv2.imshow('Contours', markers)
if cv2.waitKey(0) & 0xFF == ord('q'):
    cv2.destroyAllWindows()