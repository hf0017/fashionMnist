from flask import Flask, render_template, request
import cv2
import numpy as np
import tensorflow as tf
from keras.preprocessing import image
import os
from werkzeug.utils import secure_filename
from flask import jsonify

app = Flask(__name__)
model = tf.keras.models.load_model('model.h5')
print('Model loaded')


def model_predict(img_path, model):
    img = image.load_img(img_path, target_size=(28, 28))
    img_array = np.asarray(img)
    x = cv2.cvtColor(img_array,cv2.COLOR_BGR2GRAY)
    result = int(img_array[0][0][0])
    print(result)
    if result > 128:
      img = cv2.bitwise_not(x)
    else:
      img = x
    img = img/255.0
    img = (np.expand_dims(img,0))

    preds =  model.predict(img)
    print(preds)
    return preds


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        preds = model_predict(file_path, model)
        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        predicted_label = np.argmax(preds)
        result = class_names[predicted_label]
        return result
    return None

@app.route('/predictMobile', methods=['GET', 'POST'])
def uploadB():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)
        preds = model_predict(file_path, model)
        class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
        predicted_label = np.argmax(preds)
        result = class_names[predicted_label]
        return jsonify(result)
    return None


if __name__ == '__main__':
    app.run(host= '0.0.0.0')