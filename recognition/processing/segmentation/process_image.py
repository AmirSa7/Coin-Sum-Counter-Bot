import cv2

def process_image(img: np.ndarray) -> (np.ndarray, int):
    """<fix>"""
    proccessedImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # for testing
    coinSum = -100 # TODO: apply right value

    return (proccessedImg, coinSum)

