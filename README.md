# Python-Node.js 連携テスト

このプロジェクトは、Node.jsクライアントからPythonサーバーにリクエストを送信するシンプルなテスト環境です。

## セットアップ

1. Pythonの依存関係をインストール:
```bash
pip install -r requirements.txt
```

2. Node.jsの依存関係をインストール:
```bash
npm install
```

## 実行方法

1. まず、Pythonサーバーを起動:
```bash
python server.py
```

2. 別のターミナルで、Node.jsクライアントを実行:
```bash
node client.js
```

正常に動作すれば、Node.jsクライアントがPythonサーバーからのレスポンスを表示します。 