# Dockerコマンド
本章の目的は、これまでに登場したDockerコマンドや、登場はしていないが知っておくべきDockerコマンドをまとめて整理することです。

どのようなコマンドがあるかを調べたい場合、```docker help```を実行しましょう。コマンドの一覧が表示されます。

```sh
$ docker help
...（略）...
Management Commands:
  builder     Manage builds
  config      Manage Docker configs
  container   Manage containers
  context     Manage contexts
  engine      Manage the docker engine
  image       Manage images
  network     Manage networks
  node        Manage Swarm nodes
  plugin      Manage plugins
  secret      Manage Docker secrets
  service     Manage services
  stack       Manage Docker stacks
  swarm       Manage Swarm
  system      Manage Docker
  trust       Manage trust on Docker images
  volume      Manage volumes

Commands:
  attach      Attach local standard input, output, and error streams to a running container
  build       Build an image from a Dockerfile
  commit      Create a new image from a containers changes
  cp          Copy files/folders between a container and the local filesystem
  create      Create a new container
...（略）...
```

それぞれのコマンドの詳細は、```docker COMMAND --help```と実行すると調べることができます。

```sh
$ docker build --help

Usage:	docker build [OPTIONS] PATH | URL | -

Build an image from a Dockerfile

Options:
      --add-host list           Add a custom host-to-IP mapping (host:ip)
      --build-arg list          Set build-time variables
      --cache-from strings      Images to consider as cache sources
      --cgroup-parent string    Optional parent cgroup for the container
      --compress                Compress the build context using gzip
...（略）...
```

## dockerイメージの操作
### docker build
DockerfileをもとにDockerイメージを作成するコマンドです。

```
$ docker build [オプション] [Dockerfile配置ディレクトリのパス]
```

|オプション|説明|
|:--|:--|
|-t イメージ名[:タグ名], --tag=イメージ名[:タグ名]|イメージ名とタグ名を指定します。|
|-f *Dockerfile*, --file=*Dockerfile*|```docker build```はデフォルトでDockerfileという名前のDockerfileを探しますが、別名のDockerfileを利用したい場合に```-f```でDockerfileを指定します。|
|--pull=true|FROMで指定したベースイメージをレジストリから強制的に再取得します。最新版を必ずダウンロードする場合に有効です。|

### docker search
Docker Hubのレジストリに登録されているレジストリを検索するコマンドです。

```sh
$ docker search [オプション] [検索キーワード]
```

例えばhttpdを検索すると次の結果が得られます。

```
$ docker search httpd
NAME                                    DESCRIPTION                                     STARS               OFFICIAL            AUTOMATED
httpd                                   The Apache HTTP Server Project                  2974                [OK]                
centos/httpd-24-centos7                 Platform for running Apache httpd 2.4 or bui…   31                                      
centos/httpd                                                                            29                                      [OK]
arm32v7/httpd                           The Apache HTTP Server Project                  9                                       
polinux/httpd-php                       Apache with PHP in Docker (Supervisor, CentO…   4                                       [OK]
salim1983hoop/httpd24                   Dockerfile running apache config                2                                       [OK]
publici/httpd                           httpd:latest                                    1                                       [OK]
solsson/httpd-openidc                   mod_auth_openidc on official httpd image, ve…   1                                       [OK]

...（略）...
```

Docker公認のイメージを使いたい場合、OFFICIALの項目が[OK]となっているリポジトリを探します。

|オプション|説明|
|:--|:--|
|--limit *数値*|一覧の表示件数を制限します。|

ただし、```docker search```で出来ることはリポジトリの検索までで、タグを知りたい場合[Docker Hub](https://hub.docker.com/)のWebサイトなどアクセスするか、APIを使用する必要があります

### docker pull
DockerレジストリからDockerイメージをダウンロードするコマンドです。

```sh
$ docker pull [オプション] リポジトリ名[:タグ名]
```

リポジトリ名とタグ名はDocker Hubに存在するものを指定します。省略した場合デフォルトタグ（ほとんどの場合```latest```）が使用されます。

### docker images
```docker build```でビルドしたり```docker pull```でダウンロードしたりするなどして、ホスト環境に保存されているDockerイメージの一覧を表示するコマンドです。

```sh
$ docker images [オプション] [リポジトリ[:タグ]]
```

リポジトリ名やタグ名を指定することで、表示を制限することができます。

|オプション|説明|
|:--|:--|
|-a, --all|全てのイメージを表示（デフォルトは中間コンテナは非表示）|
|-q, --quit|イメージIDのみ表示|

### docker tag
Dockerイメージの名前を修正したり、タグを付け直したりするコマンドです。

```sh
$ docker tag 元イメージ名[:元タグ名] 新イメージ名[:新タグ名]
```
## Dockerコンテナの操作
Dockerコンテナの状態は「実行中」「停止」「破棄」といういずれかに分類されます。Dockerコンテナを操作するコマンドを理解するためには、それぞれの状態を知り、コンテナのライフサイクルを把握することが重要です。

|状態|説明|
|:--|:--|
|実行中|```docker run```や```docker start```などのコマンドによって、アプリケーションが実行中の状態です。サーバアプリケーションの場合、バックグラウンドによる実行中状態が続きますが、コマンドラインツールなどはプログラムが終了すると停止状態に移行します。|
|停止|実行中のコンテナは、明示的にコンテナを停止するか、正常／異常終了した場合に移行する状態です。コンテナ終了時の状態は保存されているため、停止したコンテナは再実行可能です。|
|破棄|停止したコンテナがディスクから削除された状態です。一度破棄され亜コンテナは再び開始することはできません。|

### docker run
Dockerイメージからコンテナを作成し、実行するコマンドです。

```sh
$ docker run [オプション] イメージ名[:タグ名] [コマンド] [コマンド引数...]
```

コマンドおよびコマンド引数を与えることで、Dockerfileで指定していた```CMD```を上書きできます。

|オプション|説明|
|:--|:--|
|--name=*コンテナ名*|コンテナに名前を割り当てます。|
|--rm|コンテナ終了時、コンテナを自動的に削除します。|
|-d|バックグラウンドで実行し、ターミナルにコンテナIDを表示します。|
|--mount type=*マウントタイプ*,src=*ホスト側のディレクトリ*,dst=*コンテナ側のディレクトリ*|[Dockerコンテナを実行する](https://github.com/JuvenileTalk9/artemis/blob/master/03_%E3%83%87%E3%82%B9%E3%82%AF%E3%83%88%E3%83%83%E3%83%97%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3/%E3%83%87%E3%82%B9%E3%82%AF%E3%83%88%E3%83%83%E3%83%97%E3%82%A2%E3%83%97%E3%83%AA%E3%82%B1%E3%83%BC%E3%82%B7%E3%83%A7%E3%83%B3.md#docker%E3%82%B3%E3%83%B3%E3%83%86%E3%83%8A%E3%82%92%E5%AE%9F%E8%A1%8C%E3%81%99%E3%82%8B)参照|
|-p *ホスト側のポート*:*コンテナ側のポート*|ホスト側のポートをコンテナ側のポートにフォワーディングします。|

### docker ps
実行中および停止中のコンテナの一覧を表示するコマンドです。

```sh
$ docker ps [オプション]
```

表示される項目の意味を確認しましょう。

|項目|内容|
|:--|:--|
|CONTAINER ID|コンテナのID|
|IMAGE|コンテナの元となるDockerイメージ|
|COMMAND|コンテナで実行されているコマンド|
|CREATED|コンテナが作成されてからの経過時間|
|STATUS|コンテナの実行状態|
|PORTS|ホストのポートとコンテナのポートの紐付け状況|
|NAMES|コンテナの名前|

|オプション|内容|
|:--|:--|
|-a, --all|全てのコンテナを表示1します。|
|-f, --filter=*フィルタ*|次の状況に応じて出力をフィルタします。<br>- "name=*コンテナ名*" ： コンテナ名の全てまたは一部が一致するコンテナを表示します。 <br> - "id=*コンテナID*" ： 一致するコンテナIDのみ表示します。 <br> - "status=*ステータス名* ： created、restarting、running、paused、exited、deadの指定した状態のコンテナのみ表示します。
|-q, --quit|コンテナIDのみ表示します。|

### docker stop
実行しているコンテナを終了するコマンドです。

```sh
$ docker stop [オプション] コンテナ名またはコンテナID [コンテナ名またはコンテナID...]
```
### docker start
停止しているコンテナを再実行するコマンドです。

```sh
$ docker start [オプション] コンテナ名またはコンテナID [コンテナ名またはコンテナID...]
```

### docker restart
実行しているコンテナを再起動するコマンドです。

```sh
$ docker restart [オプション] コンテナ名またはコンテナID [コンテナ名またはコンテナID...]
```

### docker rm
停止したコンテナを完全に破棄するコマンドです。

```sh
$ docker rm [オプション] コンテナ名またはコンテナID
```

|オプション|説明|
|:--|:--|
|-f|実行中のコンテナを強制的に削除します。|
|-v, --volums|コンテナと関連づけられたボリュームも削除します。|

### docker logs
実行しているコンテナの標準出力を表示するコマンドです。

```sh
$ docker logs [オプション] コンテナ名またはコンテナID
```

|オプション|説明|
|:--|:--|
|-f|標準出力を取得し続けます。|
|-t|出力にタイムスタンプを付与します。|

### docker exec
実行しているコンテナで任意のコマンドを実行するコマンドです。

```sh
$ docker exec [オプション] コンテナIDまたはコンテナ名 コマンド
```

|オプション|説明|
|:--|:--|
|-d|コマンドをバックグラウンドで実行します。|
|-i|標準入力を開いたままにします。|
|-t|仮想ターミナルを割り当てます。|

```-i```と```-t```を組み合わせて、コンテナの中にSSHでログインしたかのようにコンテナ内部を操作することも可能です。

```sh
$ docker exec -t コンテナIDまたはコンテナ名 /bin/bash
```

### docker cp
コンテナ間、またはホストーコンテナ間でファイルをコピーするコマンドです。

```sh
$ docker cp [オプション] コンテナIDまたはコンテナ名:コンテナ内のコピー元 ホストのコピー先
$ docker cp [オプション] ホストのコピー元 コンテナIDまたはコンテナ名:コンテナ内のコピー先
```

appコンテナ内の```/var/www/html/log.txt```をホストのカンレントディレクトリにコピーする場合は次のようにします。

```sh
$ docker cp app:/var/www/html/log.txt .
```

逆に、ホスト側の```upload.txt```をappコンテナの```/var/www/html```内にコピーする場合は、次のようにします。

```sh
$ docker cp upload.txt app:/var/www/html/
```

## 運用管理向けコマンド
### docker image prune
使われていないDockerイメージを一括削除するコマンドです。

```sh
$ docker image prune
```

### docker container prune
停止状態のDockerコンテナを一括削除するコマンドです。

```sh
$ docker container prune
```


### docker stats
コンテナ単位でのリソースの利用状況を確認するコマンドです。

```sh
$ docker stats [オプション] [コンテナID...]
```

|オプション|説明|
|:--|:--|
|-a, --all|全てのコンテナを表示します。|
|--no-stream|通常はコマンドを実行すると現在のリソースの使用状況を流し続けますが、このオプションを付与すると初回の結果のみ表示します。|

以上

[目次へ戻る](https://github.com/JuvenileTalk9/Docker)