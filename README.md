# FastAPI在庫管理システム

## 概要
FastAPIとMySQLを使用した在庫管理システムです。Docker環境で構築され、VSCodeでのリモートデバッグに対応しています。

## 機能
- 製品の作成、取得、更新、削除（CRUD操作）
- 非同期データベース処理
- UUID ベースの製品ID管理
- RESTful API設計
- 自動生成されるAPI文書

## 技術スタック
- **Backend**: FastAPI 0.115.12
- **Database**: MySQL 8.0
- **ORM**: SQLAlchemy 2.0.41 (非同期)
- **Container**: Docker + Docker Compose
- **Language**: Python 3.11
- **Debug**: debugpy + VSCode

## クイックスタート

### 前提条件
- Docker
- Docker Compose
- VSCode（デバッグ使用時）

### 1. リポジトリのクローン
```bash
git clone <repository-url>
cd private-fastapi-inventory-control-1
```

### 2. Docker環境での起動
```bash
# コンテナのビルドと起動
docker-compose up --build

# バックグラウンドで起動する場合
docker-compose up -d --build
```

### 3. 動作確認
- **API**: http://localhost:8000
- **API文書**: http://localhost:8000/docs
- **MySQL**: localhost:3306

## API エンドポイント

### 製品管理
| メソッド | エンドポイント | 説明 |
|---------|--------------|------|
| GET | `/products/{product_id}` | 製品情報取得 |
| POST | `/products` | 製品作成 |
| PUT | `/products/{product_id}` | 製品更新 |
| DELETE | `/products/{product_id}` | 製品削除 |

### リクエスト例
```bash
# 製品作成
curl -X POST "http://localhost:8000/products" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "商品名",
       "quantity": 10,
       "price": 1000.00
     }'

# 製品取得
curl -X GET "http://localhost:8000/products/{product_id}"
```

## 開発環境

### VSCodeデバッグ設定
1. Docker環境を起動
2. VSCodeでF5キーを押す
3. 「Python: Remote Attach」を選択
4. ブレークポイントを設定してデバッグ開始

詳細は [VSCode デバッグ設定手順](docs/vscode-debug-setup.md) を参照してください。

### ローカル開発
```bash
# 依存関係のインストール
pip install -r requirements.txt

# 開発サーバー起動
uvicorn api.main:app --reload
```

## プロジェクト構成
```
private-fastapi-inventory-control-1/
├── api/                    # FastAPIアプリケーション
│   ├── cruds/             # データベース操作
│   ├── models/            # SQLAlchemyモデル
│   ├── routers/           # APIルーティング
│   ├── schemas/           # Pydanticスキーマ
│   ├── db.py             # データベース設定
│   └── main.py           # アプリケーションエントリーポイント
├── db/                    # データベース初期化スクリプト
├── docs/                  # ドキュメント
├── docker-compose.yml     # Docker Compose設定
├── Dockerfile            # Docker設定
└── requirements.txt      # Python依存関係
```

## データベース接続情報
- **Host**: mysql（コンテナ間通信）/ localhost（外部接続）
- **Port**: 3306
- **Database**: inventory
- **User**: inventory_user
- **Password**: inventory_password

## 環境変数
| 変数名 | デフォルト値 | 説明 |
|--------|--------------|------|
| `DATABASE_URL` | `mysql+aiomysql://inventory_user:inventory_password@mysql:3306/inventory` | データベース接続文字列 |
| `DB_HOST` | `mysql` | データベースホスト |
| `DB_USER` | `inventory_user` | データベースユーザー |
| `DB_PASSWORD` | `inventory_password` | データベースパスワード |
| `DB_NAME` | `inventory` | データベース名 |

## ドキュメント
- [設定ファイルの説明](docs/configuration-files.md)
- [Docker環境構築手順](docs/docker-setup.md)
- [VSCodeデバッグ設定手順](docs/vscode-debug-setup.md)
- [学習用ドキュメント](docs/README.md)

## トラブルシューティング

### よくある問題
1. **ポート3306が使用中**
   ```bash
   # 使用中のプロセスを確認
   lsof -i :3306
   ```

2. **デバッグが接続できない**
   - ポート5678が開放されているか確認
   - VSCodeのデバッグ設定を確認

3. **データベース接続エラー**
   - Docker Composeの起動順序を確認
   - 環境変数の値を確認

### ログ確認
```bash
# アプリケーションログ
docker-compose logs fastapi

# データベースログ
docker-compose logs mysql

# 全体のログ
docker-compose logs
```

## 停止・クリーンアップ
```bash
# コンテナ停止
docker-compose down

# ボリュームも含めて削除
docker-compose down -v

# 全体のクリーンアップ
docker-compose down -v --rmi all
```

## コントリビューション
1. フォークする
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add some amazing feature'`)
4. ブランチをプッシュ (`git push origin feature/amazing-feature`)
5. プルリクエストを作成
