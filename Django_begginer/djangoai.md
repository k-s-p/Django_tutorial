# DjangoとTensorFlowで機械学習Webアプリ開発
- まずは、Python開発環境を作成
`create -n djangoai tensorflow-gpu`<br>
  - nvidia社のGPUを積んでいる場合は、tensorflowの後ろに"-gpu"を付ける
  - 自分の環境は、gtx1050tiなので使えるのかわからないけど、、、
  - CUDAtoolkitも同時にinstallされる！

- ANACONDA NAVIGATOR上で、環境にjupyterNotebookをインストールする
  - 簡単に管理出来て凄いな～
  - install後はLaunchを押す OR コマンドプロンプトで`jupyter notebook`でブラウザが開かれる
  - jupyter notebook上でpythonが実行できる

## tensorflowのチュートリアル:"Learn and use ML"を試す
- 手書き数字のMNISTの問題を解く
```python:test_mnist.py
import tensorflow as tf
mnist = tf.keras.datasets.mnist

(x_train, y_train),(x_test, y_test) = mnist.load_data()
x_train, x_test = x_train / 255.0, x_test / 255.0

model = tf.keras.models.Sequential([
  tf.keras.layers.Flatten(input_shape=(28, 28)),
  tf.keras.layers.Dense(128, activation='relu'),
  tf.keras.layers.Dropout(0.2),
  tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(optimizer='adam',
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=5)
model.evaluate(x_test, y_test)
```

# データの収集・クレンジング
1. Flickr APIキーを取得する
- Flickrとは<br>
画像の共有サイト。ユーザー自身がデジカメ等で撮影した写真をflickrへアップロードし、保管・管理・共有することができます。アップロードした写真は、公開することができ、コメントの許可やタグ付け機能を利用しながら、写真を通して他のユーザーと交流することができます。
  1. Flickrのトップページ下のDeveloperをクリック
  1. APIをクリック
  1. "Request an API key"をクリック
  1. Flickrにサインイン
  1. 非商用のKeyを要求(Non-Commercial)`Django Ai App to classify images.`理由を書いとく
  1. Keyが発行された！
2. データをダウンロードするプログラムを作成
VScodeのpowershellで`pip install flickrapi`
```powershell:
PS C:\cygwin64\home\USER\sk_git\Django_tutorial\Django_begginer\djangoai> pip install flickrapi  
Collecting flickrapi
  Downloading flickrapi-2.4.0-py2.py3-none-any.whl (26 kB)
Requirement already satisfied: requests>=2.2.1 in c:\users\user\anaconda3\lib\site-packages (from flickrapi) (2.24.0)
Collecting requests-oauthlib>=0.4.0
  Downloading requests_oauthlib-1.3.0-py2.py3-none-any.whl (23 kB)
Requirement already satisfied: six>=1.5.2 in c:\users\user\anaconda3\lib\site-packages (from flickrapi) (1.15.0)
Collecting requests-toolbelt>=0.3.1
  Downloading requests_toolbelt-0.9.1-py2.py3-none-any.whl (54 kB)
     |████████████████████████████████| 54 kB 3.8 MB/s
Requirement already satisfied: idna<3,>=2.5 in c:\users\user\anaconda3\lib\site-packages (from requests>=2.2.1->flickrapi) (2.10)
Requirement already satisfied: urllib3!=1.25.0,!=1.25.1,<1.26,>=1.21.1 in c:\users\user\anaconda3\lib\site-packages (from requests>=2.2.1->flickrapi) (1.25.9)
Requirement already satisfied: certifi>=2017.4.17 in c:\users\user\anaconda3\lib\site-packages (from requests>=2.2.1->flickrapi) (2020.6.20)
Requirement already satisfied: chardet<4,>=3.0.2 in c:\users\user\anaconda3\lib\site-packages (from requests>=2.2.1->flickrapi) (3.0.4)
Collecting oauthlib>=3.0.0
  Downloading oauthlib-3.1.0-py2.py3-none-any.whl (147 kB)
     |████████████████████████████████| 147 kB ...
Installing collected packages: oauthlib, requests-oauthlib, requests-toolbelt, flickrapi
Successfully installed flickrapi-2.4.0 oauthlib-3.1.0 requests-oauthlib-1.3.0 requests-toolbelt-0.9.1
```
- codeを記述
```python: download.py
from flickrapi import FlickrAPI
from urllib.request import urlretrieve
import os, time, sys
```
  - flickrapiから、FlickrAPIをimport
  - コマンドラインからアクセスするために、urlib.requestのurlretrieveをimport
  - os,time,sysをimport(system情報や時間を取得するため)
```python:
key = "XXXXXXXXX"
secret = "XXX"
wait_time = 1
```
  - keyはログインするためのアカウント
  - secretはパスワード
  - wait_timeでアクセスする時間間隔を指定(今回は1秒間隔)
```python:
keyword = sys.argv[1]
savedir = "./" + keyword
```
  - keywordは検索キーワード、sys.argv[1]は引数の2番目を示す
  - savedirはファイルを保存するディレクトリ
```python:
flickr = FlickrAPI(key, secret, format='parsed-json')
result = flickr.photos.search(
    text = keyword,
    per_page = 400,
    media = 'photos',
    sort = 'relevance',
    safe_search = 1,
    extras = 'url_q, license'
)
photos = result['photos']
```
  - flickrにアクセスするためのクライアントオブジェクトを作成
  - まず、FlickrAPIのインスタンスを生成
  - resultに検索の実行結果を格納する
    - textは検索キーワード
    - per_pageは取得する枚数
    - mediaは取得する形式
    - sortは並び順
    - safe_searchは検索時に暴力的な写真を避ける
    - extrasは余分に取得する情報。url_qはダウンロード用のurl
  - resultから写真を取り出し、photosに代入する
```python:
for i, photo in enumerate(photos['photo']):
    url_q = photo['url_q']
    filepath = savedir + '/' + photo['id'] + '.jpg'
    if os.path.exists(filepath): continue
    urlretrieve(url_q, filepath)
    time.sleep(wait_time)
```
    - enumerateを使用し、iにインデックス番号,photoにphotos['photo']の要素を格納し、ループさせる
    - url_qにはダウンロードurlを格納
    - filepathは保存先のフォルダにidで格納する
    - if文ではfilepathがすでに存在するかを確認し、存在するなら、continueし次のループに進む
    - filepathが存在しないなら、urlretrieveでurlにアクセスし、保存する
    - time.sleepで保存のあと、1秒止まる
    - `photos['photo']`はなんでphotoなのか、、、そもそもphotosの中のデータってどうなってるの、idってなに、、、flickrapiが勝手にresultに返す値？
    ```
    {'page': 1, 'pages': 4005, 'perpage': 400, 'total': '1601886', 'photo': [{'id': '3391875020', 'owner': '36587311@N08', 'secret': 'e66c8473e1', 'server': '3652', 'farm': 4, 'title': 'car', 'ispublic': 1, 'isfriend': 0, 'isfamily': 0, 'license': '0', 'url_q': 'https://live.staticflickr.com/3652/3391875020_e66c8473e1_q.jpg', 'height_q': 150, 'width_q': 150},
    ```
      - こんな感じでphotosに格納されてる
## 実行するとたくさんデータが集まった～
  - car,motorbikeをキーワードにし、画像を集める
3. 識別に失敗しそうな画像を手動で削除する

# CNNによるトレーニング(畳み込みニューラルネットワーク)
## データセットの生成
1. Pillow,scikit-learnをinstall
  - Pillow:画像処理ライブラリ。リサイズや回転、トリミングのような単純な処理が可能。より高度なことがしたいなら、OpenCVを使用する。
  - scikit-learn:機械学習ライブラリ。今回は、データの分割に使用する
2. データセット生成のプログラムを記述
```python: generate_data.py
#モジュールインポート
from PIL import Image
import os, glob
import numpy as np
from sklearn import model_selection

#パラメータの初期化
classes = ["car", "moterbike"]
num_classes = len(classes)
image_size = 150

#画像の読み込みとNumpy配列への変換
X = [] #リスト
Y = [] #リスト

for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    files = glob.glob(photos_dir + "/*.jpg")
    for i, file in enumerate(files):
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size,image_size))
        data = np.asarray(image)
        X.append(data)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
np.save("./imagefiles.npy", xy)
```
- glob:引数に指定されたパターンにマッチするファイルパス名を取得する
- globで取得したパスをPILに渡して、画像データを取得する
- 取得した画像データをnumpyリストに渡す
- numpyリストをnumpyアレイに変換して、トレーニングデータとテストデータに分割(train_test_split)する
- npy形式で保存する
## データの正規化処理を追加する
`data = np.asarray(image) / 255.0`:データを0～1の範囲に収める
## モデルの定義とトレーニング
```python:cnn.py
import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D
from tensorflow.keras.optimizers import SGD
#from tensorflow.keras.utils import np_utils
from tensorflow.keras.utils import to_categorical

#パラメータの初期化
classes = ["car", "moterbike"]
num_classes = len(classes)
image_size = 150

#ファイルからデータをロード
#X_train, X_test, y_train, y_test = np.load("./imagefiles.npy")
X_train, X_test, y_train, y_test = np.load("./imagefiles.npy", allow_pickle=True)
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

opt = SGD(lr=0.01) #rmsprop, adam
model.compile(loss='categorical_crossentropy', optimizer=opt)

model.fit(X_train, y_train, batch_size=32, epochs=10)

score = model.evaluate(X_test, y_test, batch_size=32)
```
- np_utilsは使えなかったので、to_categoricalに変更
- input_shapeはちゃんと次元を合わせる必要がある？<br>
結果
```
Train on 273 samples
Epoch 1/10
2020-11-23 14:29:29.168790: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-11-23 14:29:30.101943: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-11-23 14:29:32.333872: W tensorflow/stream_executor/gpu/redzone_allocator.cc:312] Internal: Invoking GPU asm compilation is supported on Cuda non-Windows platforms only
Relying on driver to perform ptx compilation. This message will be only logged once.
273/273 [==============================] - 7s 25ms/sample - loss: 0.1582
Epoch 2/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0091
Epoch 3/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0041
Epoch 4/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0026
Epoch 5/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0023
Epoch 6/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0015
Epoch 7/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0015
Epoch 8/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0011
Epoch 9/10
273/273 [==============================] - 1s 4ms/sample - loss: 9.3964e-04
Epoch 10/10
273/273 [==============================] - 1s 4ms/sample - loss: 8.2256e-04
91/91 [==============================] - 1s 7ms/sample - loss: 0.0017
```
- いいのかどうかわからん、、、
- 1050tiでも何とかなってよかった。
## optimizerを変更する
SGDからadamに変更してみる
```
Epoch 1/10
2020-11-23 14:58:47.279161: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-11-23 14:58:47.539721: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-11-23 14:58:48.266207: W tensorflow/stream_executor/gpu/redzone_allocator.cc:312] Internal: Invoking GPU asm compilation is supported on Cuda non-Windows platforms only
Relying on driver to perform ptx compilation. This message will be only logged once.
273/273 [==============================] - 5s 17ms/sample - loss: 0.0842
Epoch 2/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00
Epoch 3/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00
Epoch 4/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00
Epoch 5/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00
Epoch 6/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00
Epoch 7/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00
Epoch 8/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00
Epoch 9/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00
Epoch 10/10
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00
91/91 [==============================] - 1s 7ms/sample - loss: 0.0000e+00
```
## さらに、精度の表示を増やし、epoch数を増やす
epoch数を20にし、accuracyを追加する<br>
`model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])`
```
Epoch 1/20
2020-11-23 15:01:29.586380: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
2020-11-23 15:01:29.840178: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
2020-11-23 15:01:30.572831: W tensorflow/stream_executor/gpu/redzone_allocator.cc:312] Internal: Invoking GPU asm compilation is supported on Cuda non-Windows platforms only
Relying on driver to perform ptx compilation. This message will be only logged once.
273/273 [==============================] - 5s 17ms/sample - loss: 0.0831 - accuracy: 0.9377
Epoch 2/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 3/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 4/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 5/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 6/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 7/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 8/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 9/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 10/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 11/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 12/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 13/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 14/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 15/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 16/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 17/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 18/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 19/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
Epoch 20/20
273/273 [==============================] - 1s 4ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
91/91 [==============================] - 1s 7ms/sample - loss: 0.0000e+00 - accuracy: 1.0000
```
- なんか良すぎる気がする、、、
- データがちゃんと作成出来てるのか？
- 試しに別のデータ（男女のファッションの写真）で試した結果
  ```
  Epoch 1/10
  2020-11-23 15:43:09.271124: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cublas64_10.dll
  2020-11-23 15:43:09.976516: I tensorflow/stream_executor/platform/default/dso_loader.cc:44] Successfully opened dynamic library cudnn64_7.dll
  2020-11-23 15:43:11.728650: W tensorflow/stream_executor/gpu/redzone_allocator.cc:312] Internal: Invoking GPU asm compilation is supported on Cuda non-Windows platforms only
  Relying on driver to perform ptx compilation. This message will be only logged once.
  1734/1734 [==============================] - 12s 7ms/sample - loss: 0.9081 - accuracy: 0.5363
  Epoch 2/10
  1734/1734 [==============================] - 7s 4ms/sample - loss: 0.6653 - accuracy: 0.6326
  Epoch 3/10
  1734/1734 [==============================] - 7s 4ms/sample - loss: 0.6238 - accuracy: 0.6799
  Epoch 4/10
  1734/1734 [==============================] - 7s 4ms/sample - loss: 0.5989 - accuracy: 0.6851
  Epoch 5/10
  1734/1734 [==============================] - 7s 4ms/sample - loss: 0.5378 - accuracy: 0.7261
  Epoch 6/10
  1734/1734 [==============================] - 7s 4ms/sample - loss: 0.4702 - accuracy: 0.7768
  Epoch 7/10
  1734/1734 [==============================] - 7s 4ms/sample - loss: 0.4055 - accuracy: 0.8080
  Epoch 8/10
  1734/1734 [==============================] - 7s 4ms/sample - loss: 0.3222 - accuracy: 0.8570
  Epoch 9/10
  1734/1734 [==============================] - 7s 4ms/sample - loss: 0.2289 - accuracy: 0.9014
  Epoch 10/10
  1734/1734 [==============================] - 7s 4ms/sample - loss: 0.1805 - accuracy: 0.9245
  578/578 [==============================] - 1s 2ms/sample - loss: 0.9538 - accuracy: 0.6955
  ```
    - 過学習の可能性もあるけど、なんとなくデータはちゃんとできてるっぽい？

##　ここまでのCNN
1. 入力(150,150,3)
2. 第一ブロック(Conv*2)：畳み込み(3,3,3,32)
3. Pooling
4. 第二ブロック(Conv*2):畳み込み(3,3,64)
5. Pooling
6. Flatten:直列に並べる
7. 中間層(256)
8. 全結合層(2)：特徴が似ているものを判定
9. 出力
![image](https://user-images.githubusercontent.com/72511158/99934225-be8f1f00-2da0-11eb-9b10-fad056c3b192.png)

# 転移学習でスコアアップを図ろう
イメージはこんな感じ
![image](https://user-images.githubusercontent.com/72511158/99938093-75dc6380-2daa-11eb-8cab-718fbcd09422.png)
## VGG16に合わせて画像サイズを変更する
前回は(155,155,3)のデータを作成したが、今回は(224,224,3)のデータを作成<br>
また、データサイズが大きくなるため、正規化はトレーニングのコード上で行う
```python:
#モジュールインポート
from PIL import Image
import os, glob
import numpy as np
from sklearn import model_selection

#パラメータの初期化
#classes = ["car", "moterbike"]
classes = ["mens", "womens"]
num_classes = len(classes)
image_size = 224 #前回は150

#画像の読み込みとNumpy配列への変換
X = [] #リスト
Y = [] #リスト

for index, classlabel in enumerate(classes):
    photos_dir = "./" + classlabel
    # files = glob.glob(photos_dir + "/*.jpg")
    files = glob.glob(photos_dir + "/*.jpeg")
    for i, file in enumerate(files):
        image = Image.open(file)
        image = image.convert("RGB")
        image = image.resize((image_size,image_size))
        data = np.asarray(image) #前回はここで/255.0とし、浮動小数点演算を行った
        X.append(data)
        Y.append(index)

X = np.array(X)
Y = np.array(Y)

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, Y)
xy = (X_train, X_test, y_train, y_test)
#np.save("./imagefiles.npy", xy)
#np.save("./imagefiles2.npy", xy)
np.save("./imagefiles224.npy", xy) #新規でnpyファイルを作成
```
データ量はかなり小さくなった!
```
2020/11/23  16:19     1,248,489,792 imagefiles2.npy
2020/11/23  16:21       348,030,528 imagefiles224.npy
```
## 独自の学習モデルではなくVGG16をkerasからimportし使用する
`VGG16(weights='imagenet', include_top=False, input_shape=(image_size,image_size,3))`
- 重みは、"imagenet"を使用、最後の層は独自で計算するため、include_top=False
- model構造はこのようになる
  ```
  Model: "vgg16"
_________________________________________________________________
Layer (type)                 Output Shape              Param #
=================================================================
input_1 (InputLayer)         [(None, 224, 224, 3)]     0
_________________________________________________________________
block1_conv1 (Conv2D)        (None, 224, 224, 64)      1792
_________________________________________________________________
block1_conv2 (Conv2D)        (None, 224, 224, 64)      36928
_________________________________________________________________
block1_pool (MaxPooling2D)   (None, 112, 112, 64)      0
_________________________________________________________________
block2_conv1 (Conv2D)        (None, 112, 112, 128)     73856
_________________________________________________________________
block2_conv2 (Conv2D)        (None, 112, 112, 128)     147584
_________________________________________________________________
block2_pool (MaxPooling2D)   (None, 56, 56, 128)       0
_________________________________________________________________
block3_conv1 (Conv2D)        (None, 56, 56, 256)       295168
_________________________________________________________________
block3_conv2 (Conv2D)        (None, 56, 56, 256)       590080
_________________________________________________________________
block3_conv3 (Conv2D)        (None, 56, 56, 256)       590080
_________________________________________________________________
block3_pool (MaxPooling2D)   (None, 28, 28, 256)       0
_________________________________________________________________
block4_conv1 (Conv2D)        (None, 28, 28, 512)       1180160
_________________________________________________________________
block4_conv2 (Conv2D)        (None, 28, 28, 512)       2359808
_________________________________________________________________
block4_conv3 (Conv2D)        (None, 28, 28, 512)       2359808
_________________________________________________________________
block4_pool (MaxPooling2D)   (None, 14, 14, 512)       0
_________________________________________________________________
block5_conv1 (Conv2D)        (None, 14, 14, 512)       2359808
_________________________________________________________________
block5_conv2 (Conv2D)        (None, 14, 14, 512)       2359808
_________________________________________________________________
block5_conv3 (Conv2D)        (None, 14, 14, 512)       2359808
_________________________________________________________________
block5_pool (MaxPooling2D)   (None, 7, 7, 512)         0
=================================================================
Total params: 14,714,688
Trainable params: 14,714,688
Non-trainable params: 0
_________________________________________________________________
  ```
  - input_1 (InputLayer)         [(None, 224, 224, 3)]     0<br>
    入力データのサイズ、Noneはまだ枚数が不明のため未定義を表す
  - block1で畳み込みを2回行い、その後、MaxPoolingで圧縮する
  - block2でも同様の操作を行い、block3,4,5では畳み込み層が一つ増える
  - 最後に全結合して出力する。

## 全結合層の追加
```python:
top_model = Sequential()
top_model.add(Flatten(input_shape=model.output_shape[1:])) #0番目には個数が入っているため不要
top_model.add(Dense(256, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(num_classes, activation='softmax'))

#tom_modelとVGG16の結合
model = Model(inputs=model.input, outputs=top_model(model.output))
model.summary()
```
```
block5_pool (MaxPooling2D)   (None, 7, 7, 512)         0
_________________________________________________________________
sequential (Sequential)      (None, 2)                 6423298
=================================================================
Total params: 21,137,986
Trainable params: 21,137,986
Non-trainable params: 0
_________________________________________________________________

```
- モデルの最後にSequentialが追加される

## CNNレイヤーのフリーズとトレーニングの実行
フリーズさせる理由は、すでにVGG16は学習済みのモデルであり、全結合層だけを学習させれば完成するから？
- `for layer in model.layers[:15]:
    layer.trainable = False`
    <br>これで、0から15までのレイヤーは学習が行われない？・重みの変更が行われない？

## 学習率やエポック数のチューニングでスコアアップを図る
- optimizerの調整を行う
  adamのデフォルトは、lr=0.001。これが大きすぎる場合や小さすぎる場合は学習が進まない<br>
  これを一桁大きくしたり、小さくしてみる<br>
  ある程度のところで収束した。なので、収束するところで訓練を打ち切る。
  - ~~車とバイクの認識は簡単すぎる？lossが0になってる~~
  - スペルミスでmotorbikeではなくmoterbikeを参照してた、、、

## 学習済みモデルをh5形式で保存する
モデルを生成する処理を追加
- `model.save("./vgg16_transfer.h5")`

## コマンドラインアプリ化する
```python:
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
```
- `python predict.py car_1.jpg`<br>
- `car 100`
- gtx1050tiはメモリが足りなくて、邪魔な表示がたくさんでるな、、、

# DjangoでWebアプリ化する
![image](https://user-images.githubusercontent.com/72511158/99968584-a63cf580-2ddc-11eb-80b1-bea49e9c3226.png)
## djangoにプロジェクトの追加
- djangoをインストール
- プロジェクトを作成`django-admin startproject aiapps`

## アプリケーションの追加
- carbikeアプリケーションを作成`python manage.py startapp carbike`
- urls.pyにcarbikeが呼ばれた時の処理を追加する
```python:
from django.contrib import admin
from django.urls import path
import carbike.views as carbike

urlpatterns = [
    path('admin/', admin.site.urls),
    path('carbike/', carbike.index), #もしもcarbikeというindexを見に来たら、carbike.indexを返す
]
```

## ルーティングファイルを分割する
- 個別アプリのurls.pyを参照するように変更
- 全体のurls.pyを編集
```python: urls.py
from django.contrib import admin
from django.urls import path, include
#import carbike.views as carbike

urlpatterns = [
    path('admin/', admin.site.urls),
    path('carbike/', include('carbike.urls')), #もしもcarbikeというindexを見に来たら、carbike.indexを返す
]
```
- 個別アプリのurls.pyを編集
```python: urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('predict/', views.predict, name='prideict'),
]
```
- views.pyにpredictを追加
```python: views.py
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World!")

def predict(request):
    return HttpResponse("Show predictions")
```

## HTMLファイルを作成
`pip install django-bootstrap4`でbootstrap4モジュールをインストール
- Djangoのformを使用する<br>
base.htmlという共通のテンプレートを使用し、個別のhtmlで呼び出し、上書きすることで必要な部分だけ書き換えて使用することができる。
1. 共通ベーステンプレートファイルを作成
cabikeフォルダ内に、templatesフォルダを作成。そのtemplatesフォルダ内にcarbikeフォルダを作成し、以下の二ファイルを作成
- base.html:共通のテンプレートとなり、書き換え可能な部分を他のhtmlで書き換えて使用することができる
  ```html:
  <!DOCTYPE html>
  <html lang="ja">
  <head>
      <meta charset="UTF-8">
      {% load static %}
      {% load bootstrap4 %}
      {% bootstrap_css %}
      <link rel="stylesheet" type="text/css" href="{% static 'carbike/css/style.css' %}">
      {% bootstrap_javascript jquery='full' %}
      <title>車・バイク判定 | {% block title %}{% endblock %}</title>
  </head>
  <body>
      <nav class="navbar navbar-expand-lg navbar-light bg-light">
          <a class="navbar-brand" href="#">画像判定AIアプリ</a>
      </nav>
      <div class="container">
          {% block content %}{% endblock %}
      </div>
  </body>
  </html>
  ```
  - タイトル部分`{% block title %}{% endblock %}`
  - コンテンツ部分`{% block content %}{% endblock %}`
  - この部分をindex.htmlで作成する
- index.html：テンプレートのタイトルとコンテンツを上書きするための記述を行う
  ```html:
  {% extends 'carbike/base.html %'}
  {% block title %}車・バイク推定アプリメニュー{% endblock %}

  {% block content %}
  <div>
      <h4 class="mt-4 mb-5 booder-bottom">車・バイク推定アプリ</h4>
      <p>画像ファイルを選択して推定ボタンをクリックしてください。</p>
      <form action="{% url 'carbike:predict' %}" method="post" class="form" enctype="multipart/form-data">
      {% csrf_token %}
      <div class="form-group">
          <div class="custom-file">
              {{ form.image }}
              <label class="custom-file-label" for="customFile">
                  推定したいファイルを選択してください。
              </label>
          </div>
      </div>
      <button type="submit" class="btn btn-primary">推定する！</button>
      </form>
  </div>
  {% endblock %}
  ```
  - `{% extends 'carbike/base.html %'}`: carbike/base.htmlを上書きするために読み込む
  - `{% block title %}車・バイク推定アプリメニュー{% endblock %}`: タイトルを上書きする
  - `{% block content %}`と`{% endblock %}`で囲んだ部分で、コンテンツを上書きする
  - `<h4 class="mt-4 mb-5 booder-bottom">車・バイク推定アプリ</h4>`: classでbootstrapのSpacingを使用している
  - `<form action="{% url 'carbike:predict' %}" method="post" class="form" enctype="multipart/form-data">`: formのアクションとして、ボタンが押されると、djangoのテンプレートエンジンを使用し、carbike:predictに飛ぶようにする.また、ブラウザからデータを送る手法として、POST(通信のヘッダーにデータを含める)を使用する
    - （データを送る手法）GET：URLに変数を含めて渡す(外部から見えるため要注意)
  - `{% csrf_token %}`:Django特有の機能。クロスサイトリクエストフォージェリ対策。フォームに外部プログラムからデータを送りつける攻撃を防ぐ
  - `{{ form.image }}`:{{}}でdjangoの変数を参照する。views.pyからimageというデータを受け取り、ここに埋め込む

2. Formクラスを定義する
- forms.pyを作成
```python:
from django import forms

class PhotoForm(forms.Form):
    image = forms.ImageField(widget=forms.FileInput(attrs={'class':'custom-file-input'}))
```
  - djangoのformsをimportする
  - forms内のFormclassをもとに、PhotoFormというクラスを作成
  - formsのImageFieldを定義(画像をアップロードできる)。クラス名も定義する

- views.pyを編集<br>
`template = loader.get_template('carbike/index.html')`を追加
  - テンプレートを読み込みtemplate変数に渡す
`context = {'form':PhotoForm()}`を追加
  - djangoではcontextに値を入れて、値を渡す
  - formという名前で参照できる、PhotoFormを渡す
  - index.htmlで`{{ form.image }}`ここで、参照ができる！
`return HttpResponse(template.render(context, request))`に変更
  - templateのrender関数を使用し、contextとrequestを渡す
  - requestにはセッションの情報や、requestの種類(get,post)などの情報が入っている
  - contextにはデータの情報が入っている

## アプリケーションを認識させる
プロジェクトのsettings.pyのINSTALLED_APPSにcarbikeのコンフィグを認識させる
```Python:
INSTALLED_APPS = [
    'carbike.apps.CarbikeConfig'
```
さらに、bootstrap4も認識させる
```python:
INSTALLED_APPS = [
    'carbike.apps.CarbikeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap4'
]
```

- 次に、carbike/static/carbike/css/style.cssというファイルを作成する
- 次に、アプリのurls.pyに`app_name = 'carbike'`として、明示的に名前を付ける

## モデルの定義と推定処理を追加する
1. views.pyを編集
```python:
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm
from .models import Photo

def index(request):
    template = loader.get_template('carbike/index.html')
    context = {'form':PhotoForm()}
    return HttpResponse(template.render(context, request))

def predict(request):
    if not request.method == 'POST': #データがPOSTで送られてきてないなら、リダイレクトし、トップに戻る
        return redirect('carbike:index')

    form = PhotoForm(request.POST, request.FILES) #formにrequestからPOSTされたデータのFILESを取り出す
    if not form.is_valid(): #is_valid関数で、有効なデータかどうかチェックし、無向なら、エラーを返す
        raise ValueError('Formが不正です')

    #photoにPhotoクラスから'image'というタグのついたデータを取り出す。
    photo = Photo(image=form.cleaned_data['image'])
    # photo.predict() #コマンドラインで推定結果を表示するため

    return HttpResponse()
```
2. models.pyを編集
```python:
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

            print(self.classes[predicted], percentage)
```
このコードは推定結果をコマンドプロンプトに返す
- ブラウザ上に返すように変更
```
#print(self.classes[predicted], percentage)
return self.classes[predicted], percentage
```

- ブラウザに値を返す処理をviews.pyに追加
```python:
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from .forms import PhotoForm
from .models import Photo

def index(request):
    template = loader.get_template('carbike/index.html')
    context = {'form':PhotoForm()}
    return HttpResponse(template.render(context, request))

def predict(request):
    if not request.method == 'POST': #データがPOSTで送られてきてないなら、リダイレクトし、トップに戻る
        return redirect('carbike:index')

    form = PhotoForm(request.POST, request.FILES) #formにrequestからPOSTされたデータのFILESを取り出す
    if not form.is_valid(): #is_valid関数で、有効なデータかどうかチェックし、無向なら、エラーを返す
        raise ValueError('Formが不正です')

    #photoにPhotoクラスから'image'というタグのついたデータを取り出す。
    photo = Photo(image=form.cleaned_data['image'])
    #返り値を受け取る
    predicted, percentage = photo.predict()

    template = loader.get_template('carbike/result.html')

    context = {
        'predicted': predicted,
        'percentage': percentage,
    }

    return HttpResponse(template.render(context, request))
```

3. 推定結果を表示するresult.htmlを作成
```python:
{% extends 'carbike/base.html' %}
{% block title %}車・バイク推定結果{% endblock %}

{% block content %}
<div>
    <h4 class="mt-4 mb-5 booder-bottom">車・バイク推定結果</h4>

    <table class='table'>
        <tbody>
            <tr>
                <td>推定ラベル</td>
                <td>{{ predicted }}</td>
            </tr>
            <tr>
                <td>推定確立</td>
                <td>{{ percentage }} %</td>
            </tr>
        </tbody>
    </table>

    <a href = "{% url 'carbike:index' %}" class="btn btn-primary">画像選択メニューに戻る</a>

</div>
{% endblock %}
```
