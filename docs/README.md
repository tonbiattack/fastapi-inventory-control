# FastAPI Inventory Control - 学習用ドキュメント

## 概要
このドキュメントは、FastAPIアプリケーションをDockerとMySQLで構築し、VSCodeでリモートデバッグを可能にする設定の学習用資料です。

## プロジェクト構成
```
private-fastapi-inventory-control/
├── api/
│   ├── cruds/
│   │   ├── __init__.py
│   │   └── product.py
│   ├── models/
│   │   └── product.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── product.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── product.py
│   ├── db.py
│   └── main.py
├── db/
│   └── products.sql
├── docs/
│   ├── README.md
│   ├── docker-setup.md
│   ├── vscode-debug-setup.md
│   └── configuration-files.md
├── .vscode/
│   └── launch.json
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## 学習の流れ

### 1. 基本理解
まず以下のドキュメントを読んで基本的な構成を理解してください：

- [設定ファイルの説明](configuration-files.md)
- [Docker環境構築手順](docker-setup.md)

### 2. 実践
実際に環境を構築してみましょう：

1. **Docker環境の構築**
   ```bash
   docker-compose up --build
   ```

2. **動作確認**
   - FastAPI: http://localhost:8000
   - API文書: http://localhost:8000/docs

### 3. デバッグ設定
開発効率を向上させるためのデバッグ設定を学びます：

- [VSCodeデバッグ設定手順](vscode-debug-setup.md)

## 学習ポイント

### 1. Docker Composeの理解
- マルチコンテナアプリケーションの構築方法
- サービス間の通信設定
- ボリュームとネットワークの管理

### 2. FastAPIの基本構成
- 非同期処理の実装
- SQLAlchemyとの連携
- APIルーティングの設計

### 3. リモートデバッグの設定
- debugpyを使用したPythonデバッグ
- VSCodeとDockerの連携
- パスマッピングの理解

## 実装された機能

### 1. データベース接続
- 環境変数を使用した設定の外部化
- 非同期データベース接続
- SQLAlchemyによるORM

### 2. API構造
- RESTfulなAPIデザイン
- 自動生成されるAPI文書
- データバリデーション

### 3. 開発環境
- ホットリロード機能
- リモートデバッグ対応
- コンテナ化された開発環境

## 修正内容の詳細

### 1. データベース接続設定の改善

**修正前**:
```python
HOST = "127.0.0.1"
PASSWORD = ""
```

**修正後**:
```python
HOST = os.getenv("DB_HOST", "mysql")
PASSWORD = os.getenv("DB_PASSWORD", "inventory_password")
```

**理由**: Docker環境では127.0.0.1ではなく、サービス名`mysql`を使用する必要があります。

### 2. VSCodeデバッグ設定の追加

**追加設定**:
```json
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
    ]
}
```

**理由**: コンテナ内のPythonプロセスに外部からデバッガーを接続するため。

### 3. デバッグ機能の追加

**Dockerfileの修正**:
```dockerfile
EXPOSE 8000 5678
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**理由**: debugpyを使用してリモートデバッグを可能にするため。

## 学習の発展

### 1. 追加可能な機能
- 認証・認可機能
- テスト自動化
- CI/CDパイプライン
- ロギング機能

### 2. 本番環境への対応
- 環境変数の暗号化
- セキュリティ設定の強化
- パフォーマンス最適化
- 監視・メトリクス収集

### 3. 他の技術との連携
- Redis（キャッシュ）
- Nginx（リバースプロキシ）
- Prometheus（メトリクス）
- Grafana（可視化）

## トラブルシューティング

### よくある問題
1. **MySQL接続エラー**
   - ポート3306の競合
   - 環境変数の設定ミス
   - ネットワーク設定の問題

2. **デバッグ接続エラー**
   - ポート5678の競合
   - パスマッピングの設定ミス
   - ファイアウォールの制限

3. **コンテナ起動エラー**
   - Dockerfileの構文エラー
   - 依存関係の不足
   - ボリュームマウントの問題

### 解決方法
各問題の詳細な解決方法は、各ドキュメントのトラブルシューティングセクションを参照してください。

## 参考資料

### 公式ドキュメント
- [FastAPI公式ドキュメント](https://fastapi.tiangolo.com/)
- [Docker公式ドキュメント](https://docs.docker.com/)
- [MySQL公式ドキュメント](https://dev.mysql.com/doc/)

### 学習リソース
- [SQLAlchemy公式ドキュメント](https://docs.sqlalchemy.org/)
- [VSCode Python デバッグ](https://code.visualstudio.com/docs/python/debugging)
- [Docker Compose公式ドキュメント](https://docs.docker.com/compose/)

## 次のステップ
1. 基本的な機能を理解する
2. 実際に環境を構築してみる
3. デバッグ機能を試してみる
4. 新しい機能を追加してみる
5. 本番環境デプロイを検討する