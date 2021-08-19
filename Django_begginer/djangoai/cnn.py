import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import SGD, Adam
#from tensorflow.keras.utils import np_utils
from tensorflow.keras.utils import to_categorical

#パラメータの初期化
classes = ["car", "motorbike"]
#classes = ["mens", "womens"]
num_classes = len(classes)
image_size = 150

#ファイルからデータをロード
#X_train, X_test, y_train, y_test = np.load("./imagefiles.npy")
X_train, X_test, y_train, y_test = np.load("./imagefiles.npy", allow_pickle=True)
#X_train, X_test, y_train, y_test = np.load("./imagefiles2.npy", allow_pickle=True)
#y_train,y_testを1ホットベクトル形式に変換する(正解データのみ１が立つ)
y_train = to_categorical(y_train, num_classes)
y_test = to_categorical(y_test, num_classes)

#モデルの定義
model = Sequential()
#model.add(Conv2D(32,(3,3), activation='relu', input_shape= (image_size, image_size)))
model.add(Conv2D(32,(3,3), activation='relu', input_shape= (image_size, image_size,3)))
model.add(Conv2D(32,(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Conv2D(64,(3,3), activation='relu'))
model.add(Conv2D(64,(3,3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))

model.add(Flatten())
model.add(Dense(256, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(num_classes, activation='softmax'))

#opt = SGD(lr=0.01) #rmsprop, adam
opt = Adam()

model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

model.fit(X_train, y_train, batch_size=32, epochs=10)

score = model.evaluate(X_test, y_test, batch_size=32)