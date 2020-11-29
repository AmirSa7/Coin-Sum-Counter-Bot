from flask import Flask, request, Response
import jsonpickle
import numpy as np
import cv2

from processing.process_image import process_image

# Initialize the Flask application
app = Flask(__name__)


# route http posts to this method
@app.route('/api/test', methods=['POST'])
def test():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # do some fancy processing here....
    processedImage, coinSum = process_image(img)

    # encode image as jpeg
    _, img_encoded = cv2.imencode('.jpg', img)
    img_str = img_encoded.tostring()

    # build a response dict to send back to client
    response = {'message': img_str}

    # encode response using jsonpickle
    response_pickled = jsonpickle.encode(response)

    return Response(response=response_pickled, status=200, mimetype="application/json")


# start flask app
app.run(host="0.0.0.0", port=5000)
