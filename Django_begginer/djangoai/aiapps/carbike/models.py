from django.db import models

import numpy as np
#import tensorflow as tf #最新の環境ではこれは使えない
import tensorflow.compat.v1 as tf
from tensorflow import keras
from tensorflow.keras.models import load_model #h5のファイルを読み込めるようにする
from PIL import Image
import io, base64

graph = tf.get_default_graph()

class Photo(models.Model):
    image = models.ImageField(upload_to ='photos') # アップロードファイルの保存先はphotos

    IMAGE_SIZE = 224 #画像サイズ
    MODEL_FILE_PATH = './carbike/ml_models/vgg16_transfer.h5' #モデルファイル
    #パラメータの初期化
    classes = ["car", "motorbike"]
    num_classes = len(classes)

    #引数から画像ファイルを参照し、numpyアレイに変換する
    def predict(self):
        model = None
        global graph # 毎回同じモデルのセッションにデータを投入し、モデルを使いまわせる
        with graph.as_default():
            model = load_model(self.MODEL_FILE_PATH)

            img_data = self.image.read() #img_dataに画像を読み込む
            img_bin = io.BytesIO(img_data) #データをメモリ上に保持してファイルのようにアクセス

            image = Image.open(img_bin) #バイナリにした画像を与えることで、ファイルを読み込んだことと同じ扱いができる
            image = image.convert("RGB")
            image = image.resize((self.IMAGE_SIZE,self.IMAGE_SIZE))
            data = np.asarray(image) / 255.0
            X = []
            X.append(data)
            X = np.array(X)

            result = model.predict([X])[0] #複数のスコアが帰ってくるので先頭を取得する
            predicted = result.argmax() #値の大きいほうを取得する
            percentage = int(result[predicted] * 100)

            #print(self.classes[predicted], percentage)
            return self.classes[predicted], percentage

    def image_src(self):
        with self.image.open() as img:
            base64_img = base64.b64encode(img.read()).decode()

            return 'data:' + img.file.content_type + ';base64,' + base64_img