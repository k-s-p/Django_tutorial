#モジュールインポート
from PIL import Image
import os, glob
import numpy as np
from sklearn import model_selection

#パラメータの初期化
classes = ["car", "motorbike"]
#classes = ["mens", "womens"]
num_classes = len(classes)
image_size = 150

#画像の読み込みとNumpy配列への変換
X = [] #リスト
Y = [] #リスト

for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    files = glob.glob(photos_dir + "/*.jpg")
    #files = glob.glob(photos_dir + "/*.jpeg")
    for i, file in enumerate(files):
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size,image_size))
        data = np.asarray(image) / 255.0
        X.append(data)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("./imagefiles.npy", xy)
#np.save("./imagefiles2.npy", xy)
