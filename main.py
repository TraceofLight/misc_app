from fastapi import FastAPI, UploadFile
from fastapi.responses import Response

import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt

app = FastAPI()

my_model = tf.keras.models.load_model("model")

def make_result_with_model():
    content_image = plt.imread("asset/profile.jpg")
    style_image = plt.imread("asset/target.jpg")
    content_image = content_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = tf.image.resize(style_image, (256, 256))

    outputs = my_model(tf.constant(content_image), tf.constant(style_image))

    stylized_image = outputs[0]
    stylized_image = tf.squeeze(stylized_image, axis=0)
    encoded_image = tf.image.encode_jpeg(tf.cast(stylized_image * 255, tf.uint8))

    return encoded_image

@app.post("/makeImage")
async def make_image(file: UploadFile):

    img_byte = make_result_with_model()

    return Response(content=img_byte.numpy(), media_type="image/jpeg")