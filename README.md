# Docker で Kaggle の環境を構築

## kaggle 用イメージ、コンテナ作成

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

## Kaggle API を使えるようにする

- Kaggle API を活用することで、データのダウンロードや提出など、Kaggle の主要な機能を効率的に利用できる。
- API を設定しない場合、認証が必要な操作ができないため、コンテナの活用範囲が限定される。

### Kaggle API トークンの取得

- [Kaggle のアカウントページ](https://www.kaggle.com/)にログインする
- Settings の API セクションから**Create New Token**をクリックし`kaggle.json`をダウンロードする

### API トークをコンテナに配置する

1. `kaggle.json`をコンテナでアクセス可能な位置(今回だとコンテナを起動した位置`$(pwd)`)に配置する。
   例えば、ホストの作業ディレクトリの位置(コンテナ内の`/home`)に配置する。

2. コンテナ内で、以下のコマンドを実行して適切な場所にコピーする

```
// ルートディレクトリに.kaggleディレクトリを作成
// -pで必要に応じて親ディレクトリも作成することができる
mkdir -p /root/.kaggle
// homeディレクトリのkaggle.jsonを/root/.kaggleにコピー
cp /home/kaggle.json /root/.kaggle/
// kaggle.jsonのパーミッションを600に設定
chmod 600 /root/.kaggle/kaggle.json
// homeディレクトリのkaggle.jsonを削除
rm /home/kaggle.json
```

- Kaggle API クライアントは、デフォルトでユーザーのホームディレクトリの`~/.kaggle/kaggle.json`を参照する。
- Docker コンテナ内でコマンドを実行するとデフォルトで root ユーザとして動作します

```
// 現在のユーザ名の確認
root@container:/# whoami
root

//ホームディレクトリの確認
root@container:/# echo $HOME
/root
```

- セキュリティのためにパーミッションを 600(所有者のみ読み取り、書き込み可能)に設定しないといけない

```
// パーミッションの確認
ls -l /root/.kaggle
```

### 参考

- [GitHub](https://github.com/Kaggle/kaggle-api/blob/main/docs/README.md)
