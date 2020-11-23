import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model, load_model #h5のファイルを読み込めるようにする
from PIL import Image
import sys

#パラメータの初期化
classes = ["car", "motorbike"]
num_classes = len(classes)
image_size = 224 #前回は150

#コマンドライン引数から画像ファイルを参照し、numpyアレイに変換する
image = Image.open(sys.argv[1])
image = image.convert("RGB")
image = image.resize((image_size,image_size))
data = np.asarray(image) / 255.0
X = []
X.append(data)
X = np.array(X)

#モデルのロード
model = load_model('./vgg16_transfer.h5')

result = model.predict([X])[0] #複数のスコアが帰ってくるので先頭を取得する
predicted = result.argmax() #値の大きいほうを取得する
percentage = int(result[predicted] * 100)

print(classes[predicted], percentage)