# プロジェクトの初期設定とマイグレート
settings.pyを開く。ここには様々な設定が書かれている。練習では、DBとしてデフォルトで入っているsqlite3を用いる。
- sqlite3は軽量で、ファイルベースのDB。接続人数が多くなるとパフォーマンスが低下する。
## 言語設定の変更
settings.pyの言語設定部分を以下のように設定する。

```python
# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

#LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ja'

#TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True
```
保存して、再びサーバーを表示する。日本語になった！
![image](https://user-images.githubusercontent.com/72511158/98946472-4706f780-2537-11eb-9b32-1cdb348c78fd.png)

## DBのテーブルを設定
- データを作成したり、移行することを「マイグレート・マイグレーション」という
- デフォルトで作成されているモデルをデータベースに反映させる。
- マイグレート`python manage.py migrate`
成功すると以下が表示される。テーブルが作成されたらしい...

```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  ```

# アプリケーションの作成
postsというアプリケーションを作成`python manage.py startapp posts`<br>
カレントディレクトリに下記構成のフォルダが作成される
```bash
C:.
│  db.sqlite3
│  manage.py
│
├─myblogapp
│  │  settings.py
│  │  urls.py
│  │  wsgi.py
│  │  __init__.py
│  │
│  └─__pycache__
│          settings.cpython-36.pyc
│          settings.cpython-38.pyc
│          urls.cpython-36.pyc
│          wsgi.cpython-36.pyc
│          __init__.cpython-36.pyc
│          __init__.cpython-38.pyc
│
└─posts
    │  admin.py
    │  apps.py
    │  models.py
    │  tests.py
    │  views.py
    │  __init__.py
    │
    └─migrations
            __init__.py
```
## apps.pyのPostsConfigをプロジェクトから呼べるように設定ファイルに登録
settings.py内のINSTALLED_APPSに下記を追加<br>
`'posts.apps.PostsConfig'`

# リクエスト処理の流れ
![image](https://user-images.githubusercontent.com/72511158/98948852-5176c080-253a-11eb-9759-ee5ea64c236a.png)
1. クライアントがWebブラウザからアクセスし、リクエスト①を投げる
1. ルーティングファイルの設定を見てどのページを見るのか②で指定する
1. そのページをビューと呼ぶ。ビューの中でデータベースにアクセスする必要があるなら、モデル使③して、DBからデータをとってくる④
1. 外部のテンプレートが必要なら、テンプレートと合成して⑤、クライアントに返す⑥

# シンプルなリクエスト処理を実装
一つのビューをルーティングで指定して、クライアントに返す。<br>
実際のプロジェクトでは外部にテンプレートを用意して、合成するが、今回はviews.pyに直接書き込む。<br>
views.pyに以下のコードを追加
```Python
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello World! このページは投稿のインデックスです")
```
- 文法説明（明日書くか～）

<strong>Django2.0以降のURLパターンの記述方法について</strong><br>
Django1.11以前とDjango2.0以降では、URLパターンの記述方法に以下のような違いがある。
- Django1.1では、django.conf.urls.urlを使う

```Python
from django.conf.urls import urls

rulpatterns = [
    url(r'admin/', admin.site.urls),
    #url(正規表現によるURLパターン、ビュー関数)
    #・・・
]
```
- Django2.0以降では、urlも使えるが、よりシンプルに定義できるpathが追加された。先頭を示すハット(^)や末尾を示す＄は不要

```python
form django.urls import paths
urlpatterns = [
    path('admin/', admin.site.urls),
    #path(URLパターン、ビュー関数),
    #・・・
]
```
