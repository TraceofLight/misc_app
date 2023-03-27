from fastapi import Response, UploadFile, APIRouter

import os
import secrets
from pathlib import Path
from datetime import datetime

import keras
import numpy as np
import tensorflow as tf
from matplotlib import pyplot as plt

BASE_DIR = Path.cwd()
IMG_DIR = BASE_DIR / 'static' / 'images'

router = APIRouter()
my_model = keras.models.load_model("core/tf_model")

@router.post("/api/v1/itsGrey/makeImage")
async def make_image(file: UploadFile):
    '''
    이미지를 받아 모델을 통한 변환을 거친 후 새로운 이미지를 반환하는 API
    새로운 이미지가 완성되면 BE에 존재하는 임시 파일을 제거한다.
    '''

    user_image = get_image(file)
    img_byte = make_result_with_model(user_image)
    os.remove(user_image)
    
    return Response(content=img_byte.numpy(), media_type="image/jpeg")

def make_result_with_model(path: Path) -> any:
    '''
    해당하는 경로에 존재하는 jpeg 이미지를 모델에 맞게 변환하여 변환된 이미지를 반환하는 함수
    '''

    content_image = plt.imread(path)
    style_image = plt.imread(f'{BASE_DIR}/assets/target.jpg')
    content_image = content_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = style_image.astype(np.float32)[np.newaxis, ...] / 255.
    style_image = tf.image.resize(style_image, (256, 256))

    outputs = my_model(tf.constant(content_image), tf.constant(style_image))

    stylized_image = outputs[0]
    stylized_image = tf.squeeze(stylized_image, axis=0)
    encoded_image = tf.image.encode_jpeg(tf.cast(stylized_image * 255, tf.uint8))

    return encoded_image

def get_image(file: UploadFile) -> str:
    '''
    이미지를 백엔드에 저장하는 함수
    '''

    current_time = datetime.now().strftime('%Y%m%d%H%M%S')
    file_name = f'{current_time}-{secrets.token_hex(16)}'

    local_path = IMG_DIR / file_name

    with open(local_path, 'wb') as file_object:
        file_object.write(file.file.read())

    return local_path
