# Docker Compose
本章の目的は、Docker Composeの概要と使い方について学習することです。

## Docker Compose概要
Composeは、複数のコンテナを使うDockerアプリケーションを定義／実行するためのツールです。

Dockerでアプリケーションを作成する場合、単一のコンテナで完結する場合は今までに学習したコマンドを実行することで実現可能です。しかし、フロントエンドのWebサーバを配置し、ビジネスロジックをもつアプリケーションサーバを配置し、データベースや他アプリケーションと通信するようなアプリケーションを作る場合、複数のコンテナを立ち上げ、制御する必要があり、コマンドだけで管理していくことが困難になってきます。

こうした複数のコンテナを相互に接続するシステムを構築する場合、Docker Composeが利用できます。Composeは、yaml形式の設定ファイルで複数のコンテナを一括で管理／実行できるユーティリティです。

## Docker Composeのインストール

[GitHub](https://github.com/docker/compose/releases)からDocker Composeのモジュールをダウンロード可能です。バージョン番号の部分はリンク先から確認して、最新版などに適宜修正してください。

```sh
$ sudo curl -L https://github.com/docker/compose/releases/download/1.25.5/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
$ sudo chmod +x /usr/local/bin/docker-compose
```

次のコマンドでバージョン番号が表示されたらインストール完了です。
```sh
$ docker-compose --version
docker-compose version 1.25.5, build 8a1c60f6
```

## 単一のコンテナを実行する
[Webアプリケーション](https://github.com/JuvenileTalk9/Docker/blob/main/04_Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3.md)の章で作った次の実行例と同じものをdocker-composeで作成します。

```sh
$ docker run --name app -p 8888:80 --mount type=bind,src=`pwd`,dst=/usr/local/apache2/htdocs/ -d webapp
```

```compose```という名前のディレクトリに```docker-compose.yml```というファイルを作成し、下記のように記述します。

```yml
version: "3.8"
services:
    app:
        container_name: app
        image: webapp:latest
        ports:
            - 8888:80
        volumes:
            - .:/usr/local/apache2/htdocs/
```

内容を一つ一つ見ていきましょう。

```version```はCompose file（上記のyml形式のファイルのこと）で使用するバージョンを定義しています。バージョンはdocker-composeのバージョンごとに異なるので、インストールしたdocker-composeのバージョンと下記リンクのリファレンスを比較して、環境にあったバージョンを指定してください。

- [Compose file version 3 reference](https://docs.docker.com/compose/compose-file/)

アプリケーションを動かす各要素は```services```のネストの中に定義します。今回はアプリケーション一つだけなので、```app```という名前のネストを作り、その中にそれぞれの設定を記載していきます。```app```の部分は任意の名前で問題ないですが、あとから管理しやすい名前をつけます。

```services```で記述する設定内容はたくさんあるため、必要であれば下記リファレンスを参照します。

- [Service configuration reference](https://docs.docker.com/compose/compose-file/#service-configuration-reference)

ここでは、```container_name```、```image```、```ports```、```volumes```を使います。

```container_name```は、作成されるDockerコンテナの名前を指定します。ここではappを指定しました。

```image```は、コンテナのもととなるDockerイメージを指定します。ここでは、[Webアプリケーション](https://github.com/JuvenileTalk9/Docker/blob/main/04_Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3.md)の章で作成した```webapp```イメージを指定しています。

```ports```は、ポートフォワーディングのリストを記述します。ここではホスト側8888ポートをコンテナ側の80ポートに転送します。

```volumes```は、ホスト側のコンテナ側のディレクトリやボリュームのマウント設定を記述します。ここでは、ホスト側のカレントディレクトリをコンテナ側の```/usr/local/apache2/htdocs/```にマウントしています

これで、```docker run --name app -p 8888:80 --mount type=bind,src=`pwd`,dst=/usr/local/apache2/htdocs/ -d webapp```と同じコードをdocker-compose.ymlで再現しました。次に、下記コマンドでDockerコンテナを実行します。

```sh
$ docker-compose up -d
```

```-d```オプションは、```docker run```と同じでバックグラウンドでのコンテナ実行を指定するオプションです。

Dockerコンテナの一覧を見てみましょう。```app```というコンテナが実行されていることが分かります。

```
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND              CREATED             STATUS              PORTS                  NAMES
17a23933119e        webapp:latest       "httpd-foreground"   2 minutes ago       Up 2 minutes        0.0.0.0:8888->80/tcp   app
```

コンテナを停止するときは、```docker-compose down```でコンテナを全て停止／削除することができます。

```sh
$ docker-compose down
Stopping compose_app_1 ... done
Removing compose_app_1 ... done
Removing network compose_default

$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES
```

docker-composeでDockerイメージのビルドも同時に行いたい場合、```build```属性を追加します。```build```ではDockerfileが存在するディレクトリを指定します。この例ではカレントディレクトリを指定しています。作成したDockerイメージは、```image```属性でした名前で作成されます。

```yml
version: "3.8"
services:
    app:
        container_name: app
        build: .
        image: webapp
        ports:
            - 8888:80
        volumes:
            - .:/usr/local/apache2/htdocs/
```

ビルドとコンテナの実行を同時に行うときは、```--build```オプションを追加します。```--build```オプションをつけることで```docker-compose up```のたびに必ずDockerイメージをリビルドしますが、省略した場合、すでに同じ名前のDockerイメージが存在する場合ビルドはスキップします。

```
$ docker-compose up -d --build
Creating network "compose_default" with the default driver
Building app
Step 1/1 : FROM httpd:latest
 ---> b2c2ab6dcf2e

Successfully built b2c2ab6dcf2e
Successfully tagged compose_app:latest
Creating compose_app_1 ... done
```

## 複数のコンテナを実行する
docker-composeを使えば、複数のコンテナの起動も容易になります。ここでは、webサーバ1つとデータベース1つを、1つのComposefileで起動してみたいと思います。

まず```compose_multi```というディレクトリを作成し、下記のようにします。

```tree
compose_multi
├── docker-compose.yml
├── db
│   └── （空）
└── webapp
    ├── Dockerfile
    └── index.html
```

```db```はコンテナのデータベースの内容を保存するホスト側のディレクトリです。```webapp```はWebサーバ上で動作するアプリケーションで、これまでと同じものです。

次に、```docker-compose.yml```に以下を記述します。

```yml
version: "3.8"
services:
    webapp:
        container_name: webapp
        build: ./webapp/
        image: webapp
        ports:
            - 8888:80
        volumes:
            - ./webapp/:/usr/local/apache2/htdocs/
    
    db:
        container_name: mysql
        image: mysql:latest
        volumes:
            - ./db/:/var/lib/mysql
        environment:
            MYSQL_ROOT_PASSWORD: mysql
```

先ほどの単一アプリケーションの例とことなり、今度は```services```の中に2つのアプリケーションが記述されています。

```webapp```は先ほどと同じWebアプリケーションが動作するコンテナです。Dockerfileは```docker-compose.yml```からの相対パスである```./webapp/```にあります。```volumes```も同様です。

```db```はデータベースが動作するコンテナです。ここではDocker Hubで公開されているMySQLのイメージを使います。データベースの内容は```volumes```でホスト側とマウントしておくことで、一度コンテナを停止／破棄したあとでも同じコンテナを起動すれば再利用することが可能になります。

```environment```はコンテナ内の環境変数を記述する部分で、ここではMySQLのルートユーザのパスワードを記述してあります。ユーザの作成やパスワードの設定もここで可能です。

では、```docker-compose```を使ってコンテナを起動してみましょう。すでに起動済みのコンテナがある場合は、あらかじめ```docker-compose down```で停止してから進んでください。

```sh
$ docker-compose up -d --build
Creating network "compose_multi_default" with the default driver
Building webapp
Step 1/1 : FROM httpd:latest
 ---> b2c2ab6dcf2e

Successfully built b2c2ab6dcf2e
Successfully tagged webapp:latest
Pulling db (mysql:latest)...
latest: Pulling from library/mysql
54fec2fa59d0: Already exists
bcc6c6145912: Pull complete
951c3d959c9d: Pull complete
05de4d0e206e: Pull complete
319f0394ef42: Pull complete
d9185034607b: Pull complete
013a9c64dadc: Pull complete
42f3f7d10903: Pull complete
c4a3851d9207: Pull complete
82a1cc65c182: Pull complete
a0a6b01efa55: Pull complete
bca5ce71f9ea: Pull complete
Digest: sha256:61a2a33f4b8b4bc93b7b6b9e65e64044aaec594809f818aeffbff69a893d1944
Status: Downloaded newer image for mysql:latest
Creating webapp ... done
Creating mysql  ... done
```

MySQLのイメージがダウンロードされ、```webapp```と```mysql```の2つのコンテナが作成／起動されました。ブラウザを用いてWebアプリが起動していることを確認してください。また、MySQLが起動しているかは以下コマンドで確認できます。

```sh
$ docker exec -it mysql bash
[root@2e1da43b14cb\] mysql -u root -p -h 127.0.0.1
Enter password:   # <- docker-compose.ymlで指定したルートユーザのパスワードを入力する
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 8
Server version: 8.0.20 MySQL Community Server - GPL

Copyright (c) 2000, 2020, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

mysql> 
```

MySQLに入ることができました。試しにデータを入れてみましょう。

```sql
CREATE DATABASE sample;
USE sample;

CREATE TABLE users (
    id INT(8) AUTO_INCREMENT NOT NULL,
    name VARCHAR(64) NOT NULL,
    PRIMARY KEY(id)
);

INSERT INTO users (name) VALUE ('1st user');
INSERT INTO users (name) VALUE ('2st user');
```

下記のデータがSELECT分で確認できます。

```sql
mysql> SELECT * FROM users;
+----+----------+
| id | name     |
+----+----------+
|  1 | 1st user |
|  2 | 2st user |
+----+----------+
```

データベースのデータがホスト側に保存されていることを確認するために、一度コンテナを削除して、再度起動してみましょう。

```sh
$ docker-compose down
Stopping mysql  ... done
Stopping webapp ... done
Removing mysql  ... done
Removing webapp ... done
Removing network compose_multi_default

$ docker-compose up -d --build
Creating network "compose_multi_default" with the default driver
Building webapp
Step 1/1 : FROM httpd:latest
 ---> b2c2ab6dcf2e

Successfully built b2c2ab6dcf2e
Successfully tagged webapp:latest
Creating webapp ... done
Creating mysql  ... done
```

MySQLのイメージは既にダウンロードされているため、再度ダウンロードはしません。

では、下記コマンドで先ほど破棄したコンテナ上で作成したMySQLのデータが参照できることを確認しましょう。

```sh
$ docker exec -it mysql bash
[root@1aeb5076fad1\] mysql -u root -p -h 127.0.0.1
Enter password:    # <- docker-compose.ymlで指定したルートユーザのパスワードを入力する

mysql> USE sample;
mysql> SELECT * FROM users;
+----+----------+
| id | name     |
+----+----------+
|  1 | 1st user |
|  2 | 2st user |
+----+----------+
```

以上

[目次へ戻る](https://github.com/JuvenileTalk9/Docker)
