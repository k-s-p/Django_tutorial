import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import SGD, Adam
#from tensorflow.keras.utils import np_utils
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.applications import VGG16 #追加

#パラメータの初期化
classes = ["car", "motorbike"]
num_classes = len(classes)
image_size = 224 #前回は150

#ファイルからデータをロード
X_train, X_test, y_train, y_test = np.load("./imagefiles224_2.npy", allow_pickle=True) # 前回と違うファイルを読み込む
#y_train,y_testを1ホットベクトル形式に変換する(正解データのみ１が立つ)
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)
#正規化処理を追加
X_train = X_train.astype("float") / 255.0
X_test = X_test.astype("float") / 255.0

#モデルの定義(VGG16を使用)
model = VGG16(weights='imagenet', include_top=False, input_shape=(image_size,image_size,3))
#print('Model loaded')
#model.summary() # 読み込んだモデルの構造を出力

top_model = Sequential()
top_model.add(Flatten(input_shape=model.output_shape[1:])) #0番目には個数が入っているため不要
top_model.add(Dense(256, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(num_classes, activation='softmax'))

#tom_modelとVGG16の結合
model = Model(inputs=model.input, outputs=top_model(model.output))
#model.summary()
for layer in model.layers[:15]:
    layer.trainable = False


#opt = SGD(lr=0.01) #rmsprop, adam
opt = Adam(lr=0.0001)

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
model.fit(X_train, y_train, batch_size=32, epochs=17)

score = model.evaluate(X_test, y_test, batch_size=32)

model.save("./vgg16_transfer.h5")