# Webアプリケーション
本章の目的は、Dockerを使って一般的なWebアプリケーションを作成できるようになることです。Docker Hubから目的のイメージを探す方法や、Dockerにおけるポートフォワーティング機能の概要や使い方を中心に解説していきます。

# アプリケーションの仕様
デスクトップアプリケーションのときと同様に、以下に今回作成するアプリケーションの仕様を定めます。

- WebサーバはApache HTTP Serverを使用する
- 8888ポートでアクセス可能とする
- アクセスするとHelloと表示される

## Dockerイメージを作成する
アプリケーション実行までの基本的な流れは、デスクトップアプリケーションのときと同じで、まずDockerイメージをDockerfileからビルドし、次にビルドしたDockerイメージを元にコンテナを実行します。

今回はApache HTTP Serverを使用するため、コンテナで使用できるベースとなるイメージを[Docker Hub](https://hub.docker.com/)で確認します。まず、Docker Hubに接続し、画面上部の検索窓からapache等で検索します。

![Docker Hub トップページ](https://raw.githubusercontent.com/JuvenileTalk9/artemis/master/04_Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/docker_hub_top.png)

すると、ユーザがアップロードしたDockerイメージがずらっと並びます。ここで、いくつかのイメージの右上に「OFFICIAL IMAGE」と書かれているものがあることに気づきます。これは、Docker公認のイメージであることを示しており、公認のものが表示されたらそちらを使うほうが安心です。今回はDocker公認イメージのhttpdを選択します。

![apache](https://raw.githubusercontent.com/JuvenileTalk9/artemis/master/04_Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/docker_hub_apache.png)

httpdをクリックすると、次の画面が表示されます。中央には「Description」「Reviews」「Tags」のタブがあります。

![httpd](https://raw.githubusercontent.com/JuvenileTalk9/artemis/master/04_Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/docker_hub_httpd.png)

「Description」はアプリケーションのバージョン、リファレンス、コンテナの概要などが記載されています。

![description](https://raw.githubusercontent.com/JuvenileTalk9/artemis/master/04_Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/docker_hub_httpd_description.png)

バージョンを一覧で確認したい場合は「Tags」を確認します。DockerイメージをDockerfileのFROMやdocker pullコマンドで取得するとき、タグ名を指定しない場合、一番上のlatestが自動的に選択されます。

![tags](https://raw.githubusercontent.com/JuvenileTalk9/artemis/master/04_Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/docker_hub_httpd_tags.png)

Apache HTTP ServerでWebアプリケーションを作りたい場合、httpdを指定すればよいことが分かったので、Dockerfileを作ります。今回はコンテナ内で実行したいコマンドがないため、```FROM```だけで充分です。

```Dockerfile
FROM httpd:latest
```
同時に、Dockerfileと同じディレクトリに```index.html```を作ります。

```html:index.html
<html>
    <header>
        <title>Hello</title>
    </header>
    <body>
        <p>Hello WebApp</p>
    </body>
</html>
```

これで準備は完了です。それではDockerイメージをビルドしてみましょう。イメージのビルドは```docker build```コマンドです。

```sh
$ docker build -t webapp .
```

「Successfully...」のメッセージが表示されたら成功です。```docker images```コマンドでビルドできているか確認してみましょう。

```sh
$ docker images
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
httpd               latest              b2c2ab6dcf2e        22 hours ago        166MB
webapp              latest              b2c2ab6dcf2e        22 hours ago        166MB
```

## Dockerコンテナを実行する
次に、作成したDockerイメージをもとにコンテナを起動します。ここでのポイントは、Dockerイメージをビルドした段階ではコンテナ内に```index.html```を配置しておりませんし、アクセスするためのURLなども規定していないという点です。Dockerでは、それらは全てDocker起動時に指定します。

はじめにDocker起動のコマンドを示し、内容について一つ一つ解説していきます。先ほど作成した```index.html```があるディレクトリに移動し、以下のコマンドを実行します。

```sh
$ docker run --name app -p 8888:80 --mount type=bind,src=`pwd`,dst=/usr/local/apache2/htdocs/ -d webapp:latest
```

|コマンド|説明|
|:--|:--|
|--name [コンテナ名] | コンテナに名前をつけます。今回はappという名前をつけました。|
|-p [ホスト側のポート番号]:[コンテナ側のポート番号]|ホストのポートとコンテナのポートをポートフォワーディングします。詳細は以下で説明します。|
|--mount type=bind,src=[ホスト側のパス],dst=[コンテナ側のパス]|ホストのディレクトリをコンテナのディレクトリにマウントします。-vオプションでも同様のことが可能です。ここでは、Webサーバの公開ディレクトリに```index.html```をマウントし、外部からWebブラウザを通して参照できるようにします。[Docker Hubで公開されているhttpdのリファレンス](https://hub.docker.com/_/httpd?tab=description)を読むと、Webサーバの公開ディレクトリはデフォルトで```/usr/local/apache2/htdocs/```に設定されているようなので、ホスト側は```index.html```があるディレクトリに、コンテナ側は上記に設定しました。|
|-d|バックグラウンドでコンテナを実行します。-dをつけない場合、実行したコンソールが実行状態で停止してしまい、アプリケーションを常駐したい場合は使い勝手が悪いため-dをつけます。|
|webbapp:latest|コンテナの元となるDockerイメージを指定します。ビルド時にタグをつけなかった場合、デフォルトで```latest```が付けられます。|

ポートフォワーディングについて詳しく見ていきます。今回、Apache HTTP Serverで解放しているポートはデフォルトの80のため、コンテナ側のポートは必然的に80になります。そのため、コンテナ内部では80ポートへアクセスできますが、これはコンテナ内部に限定されたコンテナポートと呼ばれるもので、コンテナの外から80ポートを使ってアクセスすることができません。そこで、外部からのHTTPリクエストを受ける場合はポートフォワーディングを用いて、コンテナ外からの通信をコンテナポートに転送する必要があります。

試しに、コンテナが起動している状態で```curl```により80ポートにアクセスしてみます。

```sh
$ curl http://localhost:80/
curl: (7) Failed connect to localhost:80; Connection refused
```

接続に失敗しました。コンテナの外からのアクセスは8888ポートに限定されていることがわかります。

```sh
$ curl http://localhost:8888/
<html>
    <header>
        <title>Hello</title>
    </header>
    <body>
        <p>Hello WebApp</p>
    </body>
</html>
```

コンテナは```docker stop```コマンドにより停止できます。停止したコンテナは削除しなければ、```docker start```コマンドで再度起動できます。

```sh
$ docker stop app
$ docker start app
```

最後に、Webアプリが動作していることを確認しましょう。コンテナが起動している状態で、ブラウザで[http://localhost:8888](http://localhost:8888])にアクセスし、Webアプリが動作していることを確認します。

![app](https://raw.githubusercontent.com/JuvenileTalk9/artemis/master/04_Web%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/app.png)

## 実行中のコンテナを操作する
起動しているコンテナでコマンドを実行したい場合、```docker exec```コマンドを使います。例えば、Webサーバの公開ディレクトリの中身を以下のコマンドで参照できます。

```sh
$ docker exec app ls /usr/local/apache2/htdocs/
Dockerfile
index.html
```

```/usr/local/apache2/htdocs/```は、ホスト側の```index.html```があるディレクトリとマウントしているため、ホスト側と同じファイルが表示されました。

SSHのようにコンテナにログインしたい場合は、bashなどのシェルを起動します。-itオプションをつけることで、対話的にコマンドが実行できます。

```sh
$ docker exec -it app /bin/bash
root@dde14fd6e07c:/usr/local/apache2# 
```

コンテナ内の```httpd.conf```を参照すると、公開ディレクトリが```/usr/local/apache2/htdocs```に設定されていることが確認できます。

```sh
root@dde14fd6e07c:/usr/local/apache2# cat /usr/local/apache2/conf/httpd.conf | grep DocumentRoot
# DocumentRoot: The directory out of which you will serve your
DocumentRoot "/usr/local/apache2/htdocs"
    # access content that does not live under the DocumentRoot.
```

以上

[目次へ戻る](https://github.com/JuvenileTalk9/artemis)