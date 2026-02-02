# Docker Weather App (Flask + Scraping)

Dockerコンテナ上で動作する、Python製の天気予報表示アプリケーションです。
Yahoo!天気からデータをスクレイピングし、現在の東京の天気をWebブラウザに表示します。

本ドキュメントは、**Windows (WSL2)** 環境において、本サーバーを構築・起動するための手順書です。

## 1. 環境と要件

本システムを動作させるためには、以下の環境が必要です。

* **OS**: Windows 10 または 11
* **実行環境**: WSL2 (Ubuntu 20.04/22.04 推奨)
* **ソフトウェア**: Docker Desktop for Windows
* **必須設定**: Docker Desktopの設定で `Use the WSL 2 based engine` が有効になっていること。

## 2. ディレクトリ構成

本プロジェクトのファイル構成は以下の通りです。

```text
weather-app/
├── app.py              # アプリケーション本体 (Flask + Scraping処理)
├── Dockerfile          # Dockerイメージの設計図
├── requirements.txt    # 必要なPythonライブラリ一覧
└── README.md           # 本手順書

```

## 3. 構築手順 (Build & Run)

すべてのコマンドは、**WSL (Ubuntu) のターミナル**で実行してください。

### 手順①：リポジトリの取得と移動

プロジェクトのディレクトリに移動します。
（GitHubからクローンした場合）

```bash
git clone <リポジトリURL>
cd weather-app

```

（自分でファイルを作成した場合）

```bash
cd ~/weather-app

```

### 手順②：Dockerイメージの作成（ビルド）

`Dockerfile` の内容を元に、アプリケーションのイメージを作成します。

```bash
docker build -t my-weather-app .

```

* **コマンド解説**:
* `-t my-weather-app`: 作成するイメージに名前を付けています。
* `.`: カレントディレクトリのDockerfileを参照することを意味します（必須）。



**▼成功確認**
ビルド完了後、以下のコマンドでイメージが作成されたことを確認します。

```bash
docker images

```

> [ここに「docker images」を実行して my-weather-app が表示されている画面のスクショを貼ると評価UP]

### 手順③：コンテナの起動

作成したイメージをコンテナとして実行し、サーバーを立ち上げます。

```bash
docker run -d -p 8080:5000 --name weather-server my-weather-app

```

* **コマンド解説**:
* `-d`: デタッチモード（バックグラウンド）で実行します。
* `-p 8080:5000`: ポートフォワーディング設定です。PCの `8080` 番ポートへのアクセスを、コンテナ内の `5000` 番ポート（Flaskのデフォルト）へ転送します。
* `--name weather-server`: 稼働するコンテナに管理用の名前を付けます。



**▼成功確認**
コンテナがエラーなく起動しているか確認します。

```bash
docker ps

```

STATUSの項目が `Up ...` になっていれば成功です。

### 手順④：動作確認（ブラウザ）

Windows側のWebブラウザ（Chrome, Edgeなど）を起動し、以下のURLへアクセスします。

**URL:** [http://localhost:8080](https://www.google.com/search?q=http://localhost:8080)

以下のように「東京の天気」が表示されれば、構築成功です。

> [ここにブラウザで天気が表示されている実際の画面のスクショを貼る（最重要）]

---

## 4. 運用・停止手順

### サーバーの停止

```bash
docker stop weather-server

```

### サーバーの削除

停止したコンテナを削除する場合（再度同じ名前で `run` する場合に必要）：

```bash
docker rm weather-server

```

---

## 5. トラブルシューティング

構築中に発生しやすいエラーとその対処法です。

| エラー / 現象 | 考えられる原因 | 対処法 |
| --- | --- | --- |
| **`docker: command not found`** | Docker Desktopが起動していない、またはWSL連携がオフ。 | Docker Desktopを起動し、Setting > Resources > WSL Integration でUbuntuのスイッチをONにしてください。 |
| **`Bind for 0.0.0.0:8080 failed`** | ポート8080が既に使用されている。 | `docker run` のポート指定を `-p 8081:5000` などに変更し、ブラウザで `localhost:8081` にアクセスしてください。 |
| **ブラウザで「サイトにアクセスできません」** | コンテナが起動直後に終了している。 | `docker ps -a` で状態を確認してください。STATUSが `Exited` の場合、`docker logs weather-server` でPythonのエラーログを確認し、修正してください。 |
| **天気情報が表示されない（Error）** | コンテナからインターネットに接続できていない。 | 社内ネットワークや大学のWi-Fiの場合、プロキシ設定が必要なことがあります。自宅のネットワークで試してください。また、Yahoo!天気のページ構造が変更された可能性もあります。 |
| **`ModuleNotFoundError`** | ライブラリ不足。 | `requirements.txt` の記述ミス、または `Dockerfile` 内で `pip install` が実行されていない可能性があります。 |

---

## 6. 技術仕様（補足）

* **ベースイメージ**: `python:3.10-slim` (軽量化のため採用)
* **スクレイピング対象**: Yahoo!天気 (東京エリア)
* **拡張性**: `app.py` 内のURLを変更することで、他地域の天気も取得可能です。
