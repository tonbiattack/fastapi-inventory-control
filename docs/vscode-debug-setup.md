# VSCode デバッグ設定手順

## 概要
DockerコンテナとしてリモートデバッグでFastAPIアプリケーションをデバッグする手順です。

## 前提条件
- Docker環境が構築済み
- VSCodeにPython拡張機能がインストール済み

## 設定ファイル

### .vscode/launch.json
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: FastAPI (Local)",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "api.main:app",
                "--reload"
            ],
            "jinja": true,
            "justMyCode": true
        },
        {
            "name": "Python: Attach to Docker",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "localhost",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ],
            "justMyCode": true
        }
    ]
}
```

## デバッグ手順

### 1. Dockerコンテナの起動
```bash
docker-compose up --build
```

### 2. デバッガーの接続
1. VSCodeでF5キーを押す
2. 「Python: Attach to Docker」を選択
3. デバッガーがコンテナに接続される

### 3. ブレークポイントの設定
- コード内の任意の行をクリックして赤い点（ブレークポイント）を設定
- APIエンドポイントを呼び出すとブレークポイントで停止

### 4. デバッグ操作
- **F5**: 実行継続
- **F10**: ステップオーバー（次の行）
- **F11**: ステップイン（関数内部）
- **Shift+F11**: ステップアウト（関数から出る）

## 重要なポイント

### ポートマッピング
- Docker側：5678（デバッグポート）
- ローカル側：5678で受信

### パスマッピング
- ローカル：`${workspaceFolder}`（プロジェクトルート）
- リモート：`/app`（コンテナ内パス）

### デバッガーの待機
- コンテナは`--wait-for-client`フラグによりデバッガー接続を待機
- デバッガー接続前はアプリケーションが開始されない

## 設定の詳細説明

### attach設定
```json
"request": "attach"
```
- 既に起動しているプロセスに接続
- DockerコンテナのPythonプロセスに接続

### connect設定
```json
"connect": {
    "host": "localhost",
    "port": 5678
}
```
- 接続先のホストとポートを指定
- debugpyが待機しているポートに接続

### pathMappings設定
```json
"pathMappings": [
    {
        "localRoot": "${workspaceFolder}",
        "remoteRoot": "/app"
    }
]
```
- ローカルのファイルパスとリモートのファイルパスをマッピング
- ブレークポイントの設定に必要

## トラブルシューティング

### よくある問題と解決法

1. **デバッガーが接続できない**
   - Dockerコンテナが起動しているか確認
   - ポート5678が開放されているか確認
   - ファイアウォールの設定を確認

2. **ブレークポイントが効かない**
   - パスマッピングが正しいか確認
   - ファイルが正しく同期されているか確認

3. **デバッガーが途中で切断される**
   - コンテナの再起動によるもの
   - 再度F5でデバッガーを接続

### デバッグ用のログ確認
```bash
# コンテナのログを確認
docker-compose logs fastapi

# debugpyの状態を確認
docker exec -it inventory_fastapi ps aux | grep debugpy
```

## 参考コマンド

### デバッグ環境の確認
```bash
# コンテナの状態確認
docker-compose ps

# ネットワーク確認
docker network ls

# ポート確認
docker port inventory_fastapi
```

### デバッグ用追加設定
```json
{
    "name": "Python: Attach to Docker (Debug Mode)",
    "type": "python",
    "request": "attach",
    "connect": {
        "host": "localhost",
        "port": 5678
    },
    "pathMappings": [
        {
            "localRoot": "${workspaceFolder}",
            "remoteRoot": "/app"
        }
    ],
    "justMyCode": false,
    "logToFile": true
}
```
- `"justMyCode": false`：ライブラリ内部もデバッグ
- `"logToFile": true`：デバッグログをファイルに出力