## Docker で Kaggle の環境を構築

### Image を pull する

```
docker pull gcr.io/kaggle-gpu-images/python:latest
```

### Docker run

作成した image からコンテナを作成し実行する

MacOS では、Docker がホストおの GPU を直接利用することはサポートされていない。
そのため今回は`--gpus all`オプションを使わずにコンテナを起動する

```
docker run -itd -p 8888:8888 -v "$(pwd)":/home --name kaggle gcr.io/kaggle-gpu-images/python /bin/bash
```

#### オプション

1. `-itd`

- -i

  - コンテナの標準入力を有効化する。
  - シェル操作やコンテナ内でコマンドを直接実行できるようにする

- -t

  - コンテナに擬似ターミナル(tty)を割り当てる
  - コンテナ内での対話的な操作が可能になる

- -d
  - コンテナをバックグラウンドで実行する
  - 実行後、ターミナルを占有しない

2. `-p 8888:8888`

- ポートマッピングを指定
  - ホストのポート 8888 をコンテナのポート 8888 にマッピングする。
  - これにより、ホストマシンの`localhost: 8888`で、コンテナのサービス
    (例えば Jupyter Notebook)にアクセスできる

3. `-v "$(pwd)":/home`

- ボリュームマウントを指定
  - ホストの`$(pwd)`ディレクトリをコンテナの`/home`ディレクトリにマウントする。
  - `$(pwd)`: 現在の作業ディレクトリのパスを取得する
  - コンテナ内では`/home`ディレクトリとしてアクセス可能(マウント先)
  - ホストとコンテナでデータを共有できる

4. `--name kaggle`

- コンテナの名前を指定
  - 作成するコンテナに **kaggle** と名前をつける

5. `gcr.io/kaggle-gpu-images/python`

- 使用する Docker イメージを指定している

6. `/bin/bash`

- コンテナ内で実行するコマンド
  - コンテナ起動後に`/bin/bash`を実行します
  - シェルセッションを提供するため、コンテナ内で直接コマンドを実行できます。

### コンテナ内に入る

```
docker exec -it kaggle /bin/bash
```

### 停止

```
docker stop kaggle
```

### 再起動

```
docker start kaggle
```

### 参考

- [GitHub](https://github.com/Kaggle/docker-python?tab=readme-ov-file)
- [Zenn の記事](https://zenn.dev/yuto_mo/articles/d261e96f35986a)
- [Qiita の記事](https://qiita.com/A7_data/items/9d1a1911e001236a6b5b)
