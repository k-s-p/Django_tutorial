# Djangoのインストール
1. `conda install django`Djangoに必要なパッケージをインストール
1.  `pip install django`<br>
今回は、バージョン1.11を使用するため`pip install django==1.11`

# 新規プロジェクトの作成
以下のコマンドで、新規プロジェクトを作成する。今回は"myblogapp"というプロジェクトを作成<br>
`django-admin startproject myblogapp`<br>
作成すると、カレントディレクトリに下記構成のフォルダが作成される。
```bash
C:.
│
└─myblogapp
    │  manage.py
    │
    └─myblogapp
            settings.py
            urls.py
            wsgi.py
            __init__.py
```
- manage.py：Pythonのコマンドラインのツールを格納しているファイル。
- \_\_init\_\_.py：Pythonのパッケージであることを明示するファイル
- settings.py：Pythonの様々な設定が書き込まれている。
- urls.py：アプリケーションの昨日の単位を追加して、どういうURLで呼ぶのかというパターンを設定するファイル。
- wsgi.py：Web Server Gateway Interface.ほかのWebサーバーとDjangoの連携の仕組みを書くファイル。
デフォルトは、内蔵サーバーを使用する。内蔵サーバーは遅いため、本番環境ではApache,Ngixなどを使用する。

# 開発サーバの起動とページ表示
- サーバーの起動に失敗したため、Pythonのバージョンを下げる（最新のpythonと最新のDjangoなら起動するのかな...)
`conda install python=3.6`<br>
1. サーバーを起動<br>
Djangoのプロジェクトディレクトリのトップで
`python manage.py runserver`<br>
成功したら、下記が表示される。（もし失敗する場合は、アンチウイルスソフトでブロックされている可能性あり。）

```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).

You have 18 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
November 12, 2020 - 22:04:41
Django version 3.1.2, using settings 'myblogapp.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
2. Webページの表示<br>
ブラウザのURL欄に`http://127.0.0.1:8000/`と記述<br>
画面が表示されると成功。
![image](https://user-images.githubusercontent.com/72511158/98944755-df4fad00-2534-11eb-9137-8e420b2011ca.png)
