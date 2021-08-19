# Djangoで初めてのブログアプリを作成する

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

```bash
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

# ルーティングファイルを追加

## ルーティングファイルとは

- 調べる

## ルーティングファイル追加手順

クライアントがpostsを要求したら、前回設定したviews.pyのindexを読み込むようにする。
つまり、プロジェクト全体のmyblogapps.urlsから、アプリ内のposts.urlsを呼び出し、そこからviews.indexを呼び出す。

1. postsディレクトリにurls.pyを作成

    ```Python :views.py
    from django.conf.urls import url
    from . import views #同階層のviewsを読み込む

    urlpatterns = [url(r'^$', views.index, name='index')]
    ```

    `urlpatterns = [url(r'^$', views.index, name='index')]`（r:正規表現（パターン一致））

1. アプリケーション内でpostsが呼ばれた時の設定<br>

    postsの中のurls.pyを見に行くように設定<br>

    - myblogapp.urls.pyを編集<br>

    ```Python:myblogapp.urls.py
    from django.conf.urls import include, url
    from django.contrib import admin

    urlpatterns = [
        url(r'^posts/', include('posts.urls')),
        url(r'^admin/', admin.site.urls),
    ]
    ```

    - from django.conf.urls import <font color="Blue">include</font>, url
    - <font color="Blue">url(r'^posts/', include('posts.urls')),</font>

1. 上記の操作で、urlの関連付けが完了し、postsのviews.pyのindexを読み込むようになる。

![image](https://user-images.githubusercontent.com/72511158/99183189-5b3c3600-277d-11eb-86d3-ea3f6f5f3885.png)

```python :views.py
def index(request):
    return HttpResponse("Hello World! このページは投稿のインデックスです")
```

- [HttpResponse]で直接データをブラウザに返している。

## 直接ではなく、テンプレートを読み込んで返す

1. postsの中に、templatesというフォルダを作成
1. templatesの中にアプリケーション(posts)と同じ名前のフォルダを作成(djangoの作法)
1. そこに、index.htmlというファイルを作成し、htmlを記述

    ```html :index.html
    <!DOCTYPE html>
    <html lang = "ja-jp">
    <head>
    <title>投稿一覧</title>
    </head>
    <body>
    <h2>これは投稿一覧のページです！</h2>
    </body>
    </html>
    ```

1. 前回のviews.pyをこのように変更
render命令により、views.pyが呼ばれると、外部のindex.htmlを読み込み、ブラウザに返す

    ```python :views.py
    from django.shortcuts import render
    from django.http import HttpResponse

    def index(request):
        #return HttpResponse("Hello World! このページは投稿のインデックスです")
        return render(request, 'posts/index.html')
    # Create your views here.
    ```
    
    - renderを使用すると,templatesを見に行くのかな。。。posts/index.htmlはtemplatesにあること前提の書き方みたいだ、、、

1. これにより、テンプレートを呼び出して、ブラウザに返すことができる
    ![image](https://user-images.githubusercontent.com/72511158/99183732-54172700-2781-11eb-9b61-e6e083c5fac3.png)

## モデルを定義する

ブログ記事のデータをDBに登録する。今回は、sqlite3に登録する。環境構築でmygrateをしたが、今回は、テーブル定義を作成して、マイグレーションをする。  
postsの`models.py`を編集する。modelはclassで定義し、データを一つの変数として扱い、データの挿入などをできるようにする。

```python :models.py
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    published = models.DateTimeField()
    image = models.ImageField(upload_to='media/') #mediaに画像ファイルを置く
    body = models.TextField()

```

- 題名:title,登校日:published,画像:image,本文:bodyを変数として定義する
- 画像は'media/'に保存する

## 作成した定義をマイグレーションする

`>python manage.py makemigrations`

- makemigrationsは新しい定義ファイルがあればそれをDBに投入するためのファイルを自動生成する。
- 今回はimageで画像を使用するので、pythonで画像を扱うパッケージ(pillow)をインストールする必要がある。<br>
`pip install pillow`

```bash
Migrations for 'posts':
  posts\migrations\0001_initial.py
    - Create model Post
```

これにより、`posts\migrations\0001_initial.py`というファイルが作成される

```python :0001_initial.py
# Generated by Django 3.1.2 on 2020-11-15 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('published', models.DateTimeField()),
                ('image', models.ImageField(upload_to='media/')),
                ('body', models.TextField()),
            ],
        ),
    ]
```

- この設定ファイルをDjangoのmigrateに渡すと、テーブルを作ったり、フィールドを作成したりしてく\れる。<br>

- migrateする`python manage.py migrate`

今後は

1. models.pyにモデルを定義
1. 更新したら、makemigrations
1. ファイルを作成したら、migrateをする
1. これによりテーブルを作成できる！

## DBを確認する

本当にテーブルが作成されたかを確認する。

- `sqlite3 db.sqlite3`<br>

sqlite3に接続する

- `.tables`

migrateで作成したテーブルが存在することを確認可能

```sqlite3
sqlite> .tables
auth_group                  django_admin_log
auth_group_permissions      django_content_type
auth_permission             django_migrations
auth_user                   django_session
auth_user_groups            posts_post
auth_user_user_permissions
```

## ブラウザからDBを操作するための管理画面を作成する

Djangoには最初からadmin画面が用意されているが、管理ユーザがいないので作成する必要がある

- `python manage.py createsuperuser`

```bash
ユーザー名 (leave blank to use 'user'): XXXX
メールアドレス: XXXXX@XXXX
Password:
Password (again):
Superuser created successfully.
```

### 先ほどのアカウントでログインすることで、管理画面にログインできる

![image](https://user-images.githubusercontent.com/72511158/99184601-6f853080-2787-11eb-814a-cd529bb74600.png)

### ブログに投稿するためのメニューを管理画面に追加する

アプリケーション(posts)のadmin.pyを編集する

```python :admin.py
from django.contrib import admin

# Register your models here.
from .models import Post

admin.site.register(Post)
```

- 同階層のmodels.pyのPostを読み込む
- 管理者画面にregisterという関数でモデル定義を登録する。これにより、管理画面で簡単にモデルにデータの登録ができるようになる！（とても便利かも～）

### 管理者画面に追加される

![image](https://user-images.githubusercontent.com/72511158/99184677-1ec20780-2788-11eb-9879-abbb35658b37.png)

 投稿が可能となる！
![image](https://user-images.githubusercontent.com/72511158/99184687-284b6f80-2788-11eb-8b3a-590e15949529.png)

### 管理画面を見やすくする

- 投稿のタイトルを表示する<br>
postsの中のmodels.pyで指定している、titelをページに返す関数を作成する。

```python :models.py
from django.db import models

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=100)
    published = models.DateTimeField()
    image = models.ImageField(upload_to='media/') #mediaに画像ファイルを置く
    body = models.TextField()

    def __str__(self):
        return self.title
```

- Postは投稿を管理するモデル
- Classがデータのひな形となり、作成したデータをObjectと呼ぶ
- ここに関数を作成することで、ページに文字列を返したりできる、、、？

結果
![image](https://user-images.githubusercontent.com/72511158/99185065-b9234a80-278a-11eb-8d95-4873db42941c.png)

## アプリケーションの画面に投稿一覧を表示させる

### Template Engine

Template Engineを使うことで、モデル(DB)からデータを取り出し、それをテンプレートファイルに渡し、データを反映したhtmlを生成することができる。<br>
つまり、動的なhtmlを作成可能！<br>
![image](https://user-images.githubusercontent.com/72511158/99185371-bfb2c180-278c-11eb-9997-5ca2711c22ac.png)
<strong>Djangoには2種類のTemplateEngineが存在する</strong>

1. Django純正
1. Jinja 2(template > temple = 寺≒神社)

- モデルからデータを取り出し、変数に格納後、テンプレートに渡す<br>

    posts.viewsに以下の記述を追加する<br>

    1. `from .models import Post`<br>
        Postというモデルを読み込む

    1. 関数indexに、`posts = Post.objects.order_by('-published')`を追加<br>

        - postsという変数に、Postの全てのオブジェクトを格納する
        - また、格納の際にモデルPostのpublishedという項目で並び変える

    1. `return render(request, 'posts/index.html', {'posts': posts})`

        - レンダリングする際に、postsをテンプレートに渡してあげる
        - {'テンプレ内での変数名': 渡す変数名}

    これにより、index.htmlを呼び出す際に、postsという変数にデータを持った上体でindex.htmlは呼び出される。そのpostsからデータを取り出すのにTemplate Engineを使用する

- postsに格納されたデータを使用する

1. index.htmlを編集する

    - Template Enginの特有の記述方法として、`{% %}`と書くと変数から値を取り出したり出力したりできる。
    - Template Engin独自の記述なので、pythonの文法とは違う

    ```html : index.html
    <!DOCTYPE html>
    <html lang = "ja-jp">
    <head>
        <title>投稿一覧</title>
    </head>
    <body>
        <h1>ようこそ、私のブログへ！</h1>

        <h2>最新の投稿</h2>

        {% for post in posts.all %}

        {{ post.title }}

        {% endfor %}
    </body>
    </html>
    ```

    ```html
    {% for post in posts.all %}

        {{ post.title }}

    {% endfor %}
    ```

    ここがTemplate Enginの部分でタイトルを変数:postsから取り出して表示している.
    結果
    ![image](https://user-images.githubusercontent.com/72511158/99185876-f807cf00-278f-11eb-9aa6-c11b7b6d4eb5.png)

1. 投稿日や本文を表示する<br>
  
    index.htmlをさらに変更

    ```html
    {{ post.title }}
    <br /><br />
    {{ post.published }}
    <br /><br />
    {{ post.body }}
    <br /><br />
    ```

1. データを要約して取り出す関数を作成

    - posts.modelsに以下の関数を追加

    ```python : models.py
    def summary(self):
        return self.body[:100]
    ```

    - summary()が呼び出されると、bodyの先頭から100文字を返す

1. index.htmlで呼び出す<br>
    index.hemlの`post.body`を`post.summary`へ変更する

    ```html :
    <br /><br />
    {{ post.summary }}
    <br /><br />
    ```

    - テンプレートから、モデルの関数を呼び出すことができる！この仕組みが、Template Engineの凄いところ？

## 画像を表示する

1. index.htmlに記述を追加

    - `<img src="{{ post.image.url }}" />`
    - imageのソースのURLをpostsから取り出す

1. 写真などの静的データを呼び出すための仕組みを構築する<br>

    myblogapp.urlsを編集する

    ```python : urls.py
    from django.conf.urls import include, url
    from django.contrib import admin
    from django.conf.urls.static import static
    from django.conf import settings

    urlpatterns = [
        url(r'^posts/', include('posts.urls')),
        url(r'^admin/', admin.site.urls),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    ```

    - staticをimportし、静的ファイルを使用する
    - settingsをimportする
    - urlpatternsに`static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)`を追加する
        - 静的なデータを表示するURLと、そのデータをどこに保持しているかを設定する

1. settings.pyを編集する

    以下の記述を追加

    ```python : settings.py
    STATIC_URL = '/static/'
    MEDIA_URL = '/pics/'
    MEDIA_ROOT = BASE_DIR
    ```

    - MEDIA_URL:呼び出したファイルをどこに関連付けるか
    - MEDIA_ROOT:どこの階層に静的ファイルが存在するか(Postで指定している場所がどこなのかを関連付ける)
    - BASE_DIR:このプロジェクトのフォルダがどこにあるかをOSから取得している
    - picsという仮想的なURLを作成して、その下にアドレスを動的に作成している<br>
    `<img src="/pics/media/%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89_4WQAfrD.jpg" />`

## 投稿の詳細ページを作成

投稿のタイトルをクリックすると、投稿詳細ページに遷移するようにする。

- DjangoはモデルをDBに格納する際に、自動でidを定義し、連番で格納している(primary_key)
- このidを選択することで、詳細ページに飛ぶようにする

```bash
sqlite> select * from sqlite_master where type='table' and name='posts_post';
    type = table
    name = posts_post
tbl_name = posts_post
rootpage = 33
     sql = CREATE TABLE "posts_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(100) NOT NULL, "published" datetime NOT NULL, "image" varchar(100) NOT NULL, "body" text NOT NULL)
```

## ルーティングとは

決められたurlpatternによって、さまざまなページを振り分けること<br>
`url(r'^posts/', include('posts.urls'))`

- urlというメソッドを使う
- postsというアドレスがあれば、posts.urlsに振り分ける

## 投稿のIDをURLから取得して渡す

`url(r'^posts/(?P<post_id>[0-9]+)/$',posts.views.post_detail, name="post_detail")`

- `r'^posts` : postsから始まるアドレス
- `(?P<post_id>[0-9]+)/$` : 番号の部分を表現。Djangoの特有の表現で、(?P<>)とすると、<>で囲まれた部分が変数名となる。/$は末尾。
  - `[0-9]+` : 0から9の数字が複数(+)並んでいるという意味
  - このパターンに一致したなら、数字を変数`<post_id>`に格納する
- `posts.view.post_detail, name="post_detail"` : postsのviewである、post_detailに変数<post_id>を渡して、ページ遷移する

1. urls.pyを編集<br>
    `url(r'^posts/(?P<post_id>[0-9]+)/$',posts.views.post_detail, name="post_detail")`

1. viewにpost_detailを追加

    ```python :
    from django.shortcuts import render
    from django.http import HttpResponse
    from .models import Post

    # Create your views here.
    def index(request):
        #return HttpResponse("Hello World! このページは投稿のインデックスです")
        posts = Post.objects.order_by('-published')
        return render(request, 'posts/index.html', {'posts': posts})

    def post_detail(request, post_id):
        return render(request, 'posts/post_detail.html',{'post_id':post_id})
    ```

1. post_detail.htmlを作成

1. urls.pyがpostsのviewを参照できるように下記を追加

    - `from posts import view`
    - urlを書き換える
    - `url(r'^posts/(?P<post_id>[0-9]+)/$', views.post_detail, name="post_detail")`

## 投稿のidからデータを取り出して表示する

1. views.pyを書き換えていく

    - returnの前に一行追加`post = Post.objects.get(pk=post_id)`
    - postという変数に、Postからpost_idを主キーとしてデータを取り出す
    - return文の変数を変更`return render(request, 'posts/post_detail.html',{'post':post})`
    - postという変数に、postを格納する

1. post_detail.htmlを編集

    タイトル、投稿日、本文が表示される

    ```html:post_detail.html
    {{ post.title }}

    {{ post.published }}

    {{ post.body }}
    ```

## オブジェクトが存在しない場合の処理を追加する

- views.pyにget_object_or_404関数をimport
  - オブジェクトを取得した際に、存在しなければ、404を返す関数

```python:views.py
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Post

# Create your views here.
def index(request):
    #return HttpResponse("Hello World! このページは投稿のインデックスです")
    posts = Post.objects.order_by('-published')
    return render(request, 'posts/index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'posts/post_detail.html',{'post':post})
```

## 投稿の一覧から詳細へのリンクを作成する

1. index.htmlのタイトルをリンクにする<br>

    `<a href ="{% url 'post_detail' post.id %}">{{ post.title }}</a>`

    - `a href`: aタグがリンクを表し、href属性でリンク先を表現する
    - `"{% url 'post_detail' post.id %}"` : DjangoのTemplateEngineを使用し、リンク先をpost_detailに置き換え、post.idをページに渡す

1. ルーティングでpost_detailを振り分けられるようにする<br>

    - urls.pyのurl部分にnameで名前を付ける`url(r'^posts/(?P<post_id>[0-9]+)/$', views.post_detail, name="post_detail")`

## 投稿一覧にBootstrapを使する

- StarterTemplateを使用
  - indes.htmlにコピペし、CSSとJSを読み込む

  ```python:index.htmlを作成
  <!DOCTYPE html>
  <html lang = "ja-jp">
  <head>
    <title>投稿一覧</title>
    <meta charset="utf-8">
     <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
     <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
     <title>Hello, world!</title>
  </head>
  <body>
    <h1>ようこそ、私のブログへ！</h1>

    <h2>最新の投稿</h2>

    {% for post in posts.all %}

      <a href ="{% url 'post_detail' post.id %}">{{ post.title }}</a>
      <br /><br />
      {{ post.published }}
      <br /><br />
      <img src="{{ post.image.url }}" />
      <br />
      {{ post.summary }}
      <br /><br />

    {% endfor %}
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
  </body>
  </html>
  ```

- ライブラリを使用し、メニューを付ける<br>

本文の一番前の部分にBootstrapのNavbarを張り付ける。その後、文字などを編集し、わかりやすくする。

```html: index.html
<!DOCTYPE html>
<html lang = "ja-jp">
<head>
  <title>投稿一覧</title>
  <meta charset="utf-8">
   <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
   <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css" integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk" crossorigin="anonymous">
   <title>Hello, world!</title>
</head>
<body>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">私のブログ</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Link</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Dropdown
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#">Action</a>
          <a class="dropdown-item" href="#">Another action</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Something else here</a>
        </div>
      </li>
      <li class="nav-item">
        <a class="nav-link disabled" href="#">Disabled</a>
      </li>
    </ul>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>
<div class="container">
  <h1>ようこそ、私のブログへ！</h1>

  <h2>最新の投稿</h2>

  {% for post in posts.all %}

    <a href ="{% url 'post_detail' post.id %}">{{ post.title }}</a>
    <br /><br />
    {{ post.published }}
    <br /><br />
    <img src="{{ post.image.url }}" />
    <br />
    {{ post.summary }}
    <br /><br />

  {% endfor %}
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js" integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js" integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI" crossorigin="anonymous"></script>
</div>
</body>
</html>
```

- `div`: Division・四角形の領域で囲う
- 結果はこうなる～、見栄えが良くなる～,便利やな！！！

![image](https://user-images.githubusercontent.com/72511158/99261409-09201100-2860-11eb-9759-ebd32b97d78f.png)

- 写真をレスポンシブに拡大・縮小する
  - imageタグにclass='img-fluid'を指定する<br>
  `<img src="{{ post.image.url }}" class = "img-fluid" />`
  - ほかのオプションを試す
  `rouded` :　角が丸くなる
  `img-thumbnail`: imageをサムネイル化する

## メニューと詳細ページを調整する

デフォルトのままだと、メニューバーにいらないリンクなどがあるので体裁を整える。

1. 画像の高さを整えるためにstyleを定義する<br>
    `<img src="{{ post.image.url }}" class = "img-fluid rounded" style="max-height: 200px;"/>`

1. タイトルの大きさを調整するために、見出しのサイズを変更する<br>

    `<h2>最新の投稿</h2>` →  `<h3>最新の投稿</h3>`

    - `<h1>`から`<h6>`の順に見出しのサイズが小さくなる

1. リンクに何かアドレスを追加する

    `<a class="nav-link" href="http://www.pornograffitti.jp/?_ga=2.47412065.75155999.1605703580-91063952.1590658384">ポルノグラフィティOfficialSite</a>`

1. 不要な部分の削除

    以下の部分を削除する(ドロップダウンアクションとサーチ)

    ```html: index.html
    <li class="nav-item dropdown">
            <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            Dropdown
            </a>
            <div class="dropdown-menu" aria-labelledby="navbarDropdown">
            <a class="dropdown-item" href="#">Action</a>
            <a class="dropdown-item" href="#">Another action</a>
            <div class="dropdown-divider"></div>
            <a class="dropdown-item" href="#">Something else here</a>
            </div>
        </li>

        <form class="form-inline my-2 my-lg-0">
        <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
        <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
    ```

1. タイトルの下に画像を表示

    アプリケーションフォルダのtemplatesと同じ階層にstaticというフォルダを作成。さらにその中に、アプリケーションと同名のフォルダを作成。このフォルダの中に画像ファイルを入れていく。]

    - staticフォルダの画像を参照.さらに、タイトルをセンターに

    ```html:
    <h1 class="text-center">ようこそ、スガヤのブログへ！</h1>
    <br /><br />
    {% load static %}
    <img src="{% static 'posts/pg.jpg'%}" class = "img-fluid rounded" style="max-height: 200px;"/>
    ```

    - 引っかかったのでメモ<br>

    まず、settings.pyに`STATIC_URL = '/static/'`があることが前提。さらに、一度サーバーを再起動する必要あり。

1. 細かい調整

    - タイトルの下にラインを入れる`<hr>`
    - 投稿詳細ページの体裁も整える。

1. StaticなAboutページの作成

    - staticフォルダのpostsにabout.htmlを作成
    - staticフォルダ内を参照するので画像などはTemplate Engineを使用する必要はない

    ```html: about.html
    <!--{% load static %} -->
    <!--<a class="nav-link" href="{% static 'posts/about.html' %}">About</a> -->
    <a class="nav-link" href="./about.html">About</a>
    ```

    ```html:about.html
    <!--{% load static %}
    <img src="{% static 'posts/pg-2.jpg'%}" class = "img-fluid rounded" style="max-height: 200px;"/>
    -->
    <img src="./pg-2.jpg" class = "img-fluid rounded" style="max-height: 200px;"/>
    ```

# AWS上でアプリケーションを公開する(別ファイル)
