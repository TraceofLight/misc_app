from fastapi import FastAPI, UploadFile
from fastapi.responses import Response

import os
import tempfile
import tensorflow as tf
import numpy as np
from matplotlib import pyplot as plt
from PIL import Image

app = FastAPI()

my_model = tf.keras.models.load_model("model")

def make_result_with_model(image_path):
    content_image = plt.imread(image_path)
    style_image = plt.imread("asset/target.jpg")
    content_image = content_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = tf.image.resize(style_image, (256, 256))

    outputs = my_model(tf.constant(content_image), tf.constant(style_image))

    stylized_image = outputs[0]
    stylized_image = tf.squeeze(stylized_image, axis=0)
    encoded_image = tf.image.encode_jpeg(tf.cast(stylized_image * 255, tf.uint8))

    return encoded_image

async def get_image(file: UploadFile):

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp_file:
        tmp_file.write(await file.read())
        tmp_file.flush()
        tmp_file.seek(0)

        image = Image.open(tmp_file.name)
        image = image.convert("RGB")
        save_path = os.path.join(tempfile.gettempdir(), f"{file.filename}.jpg")
        image.save(save_path, format="JPEG")

        os.unlink(tmp_file.name)

    return save_path

@app.post("/makeImage")
async def make_image(file: UploadFile):
    img_byte = make_result_with_model(get_image(file))

    return Response(content=img_byte.numpy(), media_type="image/jpeg")