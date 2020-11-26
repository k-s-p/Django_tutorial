#作成したmyblogappをAWSで公開する
AWS無料枠に登録し、ubuntu環境で、Ngix,Postgreを使用する。<br>
これらの使い方を簡単に書き残しておく。

## AWS無料枠に登録
1. 下記サイトに接続し、無料枠で登録する。<br>
https://aws.amazon.com/jp/ec2/?ec2-whats-new.sort-by=item.additionalFields.postDateTime&ec2-whats-new.sort-order=desc
- Amazon EC2とは<br>
安全でサイズ変更可能なコンピューティング性能をクラウド内で提供するウェブサービス。プロセッサ、ストレージ、ネットワーキング、オペレーティングシステム、購入モデルを選択可能。従量課金制で使用可能。
2. Amazon EC2を無料枠で使用
3. アカウントtypeはパーソナル
4. 必要事項は英語で入力？
5. 無料枠でもクレジット登録必要
6. 電話番号の検証後、プランの選択
7. ベーシックプランを選択(無料)
8. ルートユーザでサインイン
9. 登録完了!

## EC2のインスタンス(Ubuntu 16.04LTS)を立てる
1. 仮想マシンを起動する<br>
![image](https://user-images.githubusercontent.com/72511158/100353827-78e98500-3032-11eb-9b23-bbfdf2367720.png)
  - いろんなことができる！
2. クイックスタートでAMI(Amazon Machin Image)を選択<br>
AMIは、ソフトウェア構成(OS,アプリケーションサーバー、アプリケーション)含むテンプレートのことらしい。とりあえず、当初の予定通り、`Ubuntu Server 16.04 LTS (HVM), SSD Volume Type`を選択。
3. インスタンスタイプの選択<br>
インスタンスとは、アプリケーションを実行できる仮想サーバー。インスタンスタイプはさまざまなCPU,メモリ、ストレージ、ネットワークきゃばシティの組み合わせによって構成される。無料枠では、`t2.micro`が使用可能なようだ。
![image](https://user-images.githubusercontent.com/72511158/100354872-28732700-3034-11eb-951c-0002cc8167fa.png)
4. 認証キーを作成
キーを使用し、仮想環境にアクセスするようになる。<br>
大事に保存する！
5. 作成完了！
![image](https://user-images.githubusercontent.com/72511158/100355349-f3b39f80-3034-11eb-8116-368c203461f0.png)

## TeraTermからUbuntuに接続する
接続はSSHを用いて行う。
- SSHとは、安全に通信を行って、ネットワークに接続された機器を遠隔操作するための通信手段(プロトコル)の一つ.現在は、SSH2が主流となっている。サーバー側で「SSHデーモン」、クライアント側で「SSHクライアント」が起動されている必要があり、Linuxではほぼデフォルトで起動されている。
- TeraTermとは、Windows上で動作する多機能端末。主に、SSHクライアントとして使用される。
1. TeraTermをインストール
2. 新しい接続で、ホストにAWS EC2のパブリックDNSをコピペ
3. know hostsリストに追加
4. ユーザ名を入力
5. パスワードではなく、秘密鍵を使用する
6. アクセス完了！

## ubuntuにPython3,PostgreSQL,Ngixをインストールする
今回は、GUIではないのでAnacondaを使用せず、直接インストールしていく
- `sudo apt-get update`:データベース（リポジトリ）のカタログを更新する
### インストール作業
-  `sudo apt-get install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx`
<br>※Ubuntu環境ではPython2とPython3が共存できるため、コマンドは`python`ではなく`python3`と明示する必要がある

## PostgreSQLの設定をする
- `sudo -u postgres psql`:postgresといユーザーでpsql(DBに接続)する
- データベース作成`CREATE DATABASE myblogapp;`
- ユーザーとパスワードを作成`CREATE USER mybloguser WITH PASSWORD 'p@ssword';`
- 日本語が使えるようにする`ALTER ROLE mybloguser SET client_encoding TO 'utf8';`
- 実行された結果だけ見に行くようにする`ALTER ROLE mybloguser SET default_transaction_isolation TO 'read committed';`
- タイムゾーンの設定`ALTER ROLE mybloguser SET timezone TO 'UTC+9';`
- 権限を与える`GRANT ALL PRIVILEGES ON DATABASE myblogapp TO mybloguser;`
- `\q`でpostgreの環境から脱出

## virtualenvをインストールし仮想環境を構築
virtualenvを使用することで、一つのシステム内に独立した複数の開発環境を構築することが可能。ローカル環境では、ANACONDAに同梱していた
- pipのインストール`sudo -H pip3 install --upgrade pip`
- virtualenvのインストール`sudo -H pip3 install virtualenv`
- py36という環境を作成`virtualenv py36`
- 仮想環境を起動`source py36/bin/activate`
- `pip install django gunicorn psycopg2`
  - django
  - gunicorn(アプリケーションサーバー)
  - psycopg2(Pythonからpostgresqlに接続するためのもの)

## プロジェクトファイルをアップロードする(WinSCP)
SSH環境ではSCPのクライアントでファイル転送を行う
- WinSCPはすでに持ってるのでインストール不要
- AWSへの接続設定を行う
  - 接続方法は、SCPを使用
  - ホスト名には、サーバーのパブリックIPを入力
  - ユーザー名を入力し、秘密鍵で認証
- myblogappファイルを丸ごとアップする
