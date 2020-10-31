# Hello World
本章の目的は、DockerイメージとDockerコンテナについて理解し、DockerでHello Worldが実行できるようになることです。登場するコマンドについては登場したときに逐次説明していきます。

## DockerイメージとDocklerコンテナ
Dockerのアプリケーションは、Dockerイメージをもと作成されたDockerコンテナで実行されます。DockerイメージとDockerコンテナをまとめると次のようになります。

|名称|説明|
|:--|:--|
|Dockerイメージ|Dockerコンテナを構成するOS、アプリケーション、設定などをまとめたもので、コンテナのテンプレートとなるもの|
|Dockerコンテナ|Dockerイメージをもとに作成され、OSやアプリケーションが実行されている状態|

Dockerでアプリケーションを実行するためには、まずDockerイメージを作成し、Dockerイメージを使ってDockerコンテナを実行します。

## Hello World
まずHello World!!と出力するだけのアプリケーション```helloworld.sh```を作成します。ここではシェルスクリプトで実装します。

```sh:helloworld.sh
#!/bin/sh

echo "Hello World!!"
```

続いて```helloworld.sh```と同じディレクトリに、Dockerがどんなイメージを作成するか定義する```Dockerfile```を作成します。

```
FROM centos:7

COPY helloworld.sh /usr/local/bin
RUN chmod +x /usr/local/bin/helloworld.sh

CMD ["helloworld.sh"]
```

```FROM```はコンテナのベースとなるOSを定義します。ここではCentOSを指定しています。OSも1つのDockerイメージとして管理されます。CentOSのDockerイメージは初期状態ではローカル環境にはないため、Dockerイメージ作成時に自動的にダウンロードされます。```:7```は、ダウンロードされるCentOSのDockerイメージのタグ名を7にするという意味です。

```COPY```は```helloworld.sh```をホスト側から、コンテナ側の```/user/local/bin```にコピーしています。

```RUN```はコンテナ側で任意のコマンドを実行するコマンドで、ここでは```chmod```コマンドで```helloworld.sh```に実行権限を与えています。

```CMD```は作成したイメージをDockerコンテナとして実行されたときにコンテナ内で実行されるコマンドを定義します。ここでは先ほど作成した```helloworld.sh```を実行しています。

次に、```docker build```コマンドでDockerイメージをビルドします。```-t```オプションは、作成するDockerイメージのイメージ名とタグ名を指定できます。ここでは、イメージ名は```helloworld```、タグ名を```latest```としています。

```sh
$ docker build -t helloworld:latest .
```

```docker images```コマンドで、```helloworld```という名前でDockerイメージが作成されていることが確認できます。```helloworld```コンテナのベースとなるCentOSのイメージも同時にダウンロードされています。

```sh
$ docker images
REPOSITORY   TAG      IMAGE ID      CREATED       SIZE
helloworld   latest   58803ca82251  7 minutes ago 203MB
centos       7        5e35e350aded  5 months ago  203MB
```

また、この段階ではあくまでもイメージをビルドしただけで、コンテナは作成されていません。

```sh
$ docker ps -a
CONTAINER ID   MAGE    COMMAND   CREATED   STATUS    PORTS   NAMES
```

最後に、```docker run```コマンドでDockerコンテナを実行します。

```sh
$ docker run helloworld:latest
Hello World!!!
```
```docker ps```コマンドで、コンテナが実行され、終了（Exited）状態になっていることが確認できます。


```sh
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                    PORTS               NAMES
37bedc101365        helloworld:latest   "helloworld.sh"     2 seconds ago       Exited (0) 1 second ago                       pedantic_cori
```

## DockerイメージとDockerコンテナの確認と削除
Dockerイメージは、Dockerfileをもとに```docker build```コマンドで作成できることを学びました。作成したDockerイメージの一覧は```docker images```コマンドで参照できます。

```sh
$ docker images
REPOSITORY   TAG      IMAGE ID      CREATED       SIZE
helloworld   latest   58803ca82251  7 minutes ago 203MB
centos       7        5e35e350aded  5 months ago  203MB
```

Dockerイメージを削除する場合は、```docker rmi```コマンドを実行します。

```sh
$ docker rmi [DockerイメージのREPOSITORY]
```

ただし、削除したいイメージがDockerコンテナで使用されている場合は、先にDockerコンテナを削除する必要があります。Dockerコンテナの一覧は```docker ps```コマンドで参照できます。```-a```オプションを付与することで、現在実行されていないDockerコンテナも表示されます。

```sh
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                    PORTS               NAMES
37bedc101365        helloworld:latest   "helloworld.sh"     2 seconds ago       Exited (0) 1 second ago                       pedantic_cori
```

Dockerコンテナを削除する場合は、```docker rm```コマンドを実行します。

```sh
$ docker rm [DockerコンテナのNAMES]
```

以上

[目次へ戻る](https://github.com/JuvenileTalk9/Docker)