# 設定ファイルの説明

## 概要
プロジェクトで使用される各種設定ファイルの詳細な説明です。

## ファイル構成

### 1. docker-compose.yml
Docker Composeの設定ファイルです。

#### 主要な設定項目

##### MySQLサービス
```yaml
mysql:
  image: mysql:8.0
  environment:
    MYSQL_ROOT_PASSWORD: rootpassword
    MYSQL_DATABASE: inventory
    MYSQL_USER: inventory_user
    MYSQL_PASSWORD: inventory_password
```

**説明**:
- `image`: MySQL 8.0のDockerイメージを使用
- `MYSQL_ROOT_PASSWORD`: rootユーザーのパスワード
- `MYSQL_DATABASE`: 自動作成されるデータベース名
- `MYSQL_USER/MYSQL_PASSWORD`: アプリケーション用のユーザー

##### FastAPIサービス
```yaml
fastapi:
  build: .
  ports:
    - "8000:8000"
    - "5678:5678"
  environment:
    - DATABASE_URL=mysql+aiomysql://inventory_user:inventory_password@mysql:3306/inventory
```

**説明**:
- `build: .`: 現在のディレクトリのDockerfileを使用
- `ports`: ホストとコンテナのポートマッピング
- `DATABASE_URL`: データベース接続文字列

### 2. Dockerfile
FastAPIアプリケーションのコンテナイメージを定義します。

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 5678
CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

**説明**:
- `FROM python:3.11-slim`: 軽量なPython 3.11イメージを使用
- `WORKDIR /app`: コンテナ内の作業ディレクトリを設定
- `COPY requirements.txt .`: 依存関係ファイルをコピー
- `RUN pip install`: 依存関係をインストール
- `COPY . .`: アプリケーションコードをコピー
- `EXPOSE`: ポートを公開
- `CMD`: デバッグ付きでアプリケーションを起動

### 3. requirements.txt
Pythonの依存関係を定義します。

```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
aiomysql==0.2.0
debugpy==1.8.0
pydantic==2.5.0
```

**説明**:
- `fastapi`: WebAPIフレームワーク
- `uvicorn[standard]`: ASGI サーバー（標準機能付き）
- `sqlalchemy`: ORM（オブジェクト関係マッピング）
- `aiomysql`: MySQL用の非同期ドライバー
- `debugpy`: Pythonデバッガー
- `pydantic`: データバリデーション

### 4. api/db.py
データベース接続の設定ファイルです。

#### 修正前
```python
DATABASE = "mysql+aiomysql"
USER = "root"
PASSWORD = ""
HOST = "127.0.0.1"
PORT = "3306"
DB_NAME = "inventory"
```

#### 修正後
```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE = "mysql+aiomysql"
USER = os.getenv("DB_USER", "inventory_user")
PASSWORD = os.getenv("DB_PASSWORD", "inventory_password")
HOST = os.getenv("DB_HOST", "mysql")
PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "inventory")

DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "{}://{}:{}@{}:{}/{}".format(DATABASE, USER, PASSWORD, HOST, PORT, DB_NAME)
)
```

**修正内容**:
- 環境変数を使用してDocker環境に対応
- ハードコーディングから設定可能な値に変更
- `DATABASE_URL`環境変数で上書き可能

### 5. .vscode/launch.json
VSCodeのデバッグ設定です。

#### 修正前
```json
{
    "name": "Python: FastAPI",
    "type": "python",
    "request": "launch",
    "module": "uvicorn",
    "args": [
        "app.main:app",
        "--reload"
    ]
}
```

#### 修正後
```json
{
    "configurations": [
        {
            "name": "Python: FastAPI (Local)",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": [
                "api.main:app",
                "--reload"
            ]
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
            ]
        }
    ]
}
```

**修正内容**:
- ローカル実行用とDocker接続用の2つの設定を追加
- `request: "attach"`でリモートデバッグに対応
- `pathMappings`でローカルとコンテナのパスをマッピング

## 環境変数の説明

### Docker Compose環境変数
```yaml
environment:
  - DATABASE_URL=mysql+aiomysql://inventory_user:inventory_password@mysql:3306/inventory
  - PYTHONPATH=/app
```

- `DATABASE_URL`: データベース接続文字列
- `PYTHONPATH`: Pythonモジュールの検索パス

### MySQL環境変数
```yaml
environment:
  MYSQL_ROOT_PASSWORD: rootpassword
  MYSQL_DATABASE: inventory
  MYSQL_USER: inventory_user
  MYSQL_PASSWORD: inventory_password
```

- `MYSQL_ROOT_PASSWORD`: MySQLのrootパスワード
- `MYSQL_DATABASE`: 初期データベース名
- `MYSQL_USER`: アプリケーション用ユーザー名
- `MYSQL_PASSWORD`: アプリケーション用パスワード

## セキュリティ考慮事項

### 本番環境での注意点
1. **パスワード管理**
   - 環境変数やSecretを使用
   - ハードコーディングは避ける

2. **ポート公開**
   - 必要最小限のポートのみ公開
   - デバッグポートは開発環境のみ

3. **ネットワーク**
   - 内部ネットワークを使用
   - 外部からの不要なアクセスを制限

### 開発環境での設定
```yaml
# 開発環境用の設定例
environment:
  - DEBUG=true
  - DATABASE_URL=mysql+aiomysql://inventory_user:inventory_password@mysql:3306/inventory
  - PYTHONPATH=/app
```

## カスタマイズ方法

### ポート変更
```yaml
ports:
  - "8080:8000"  # ホストポート8080でアクセス
  - "5679:5678"  # デバッグポート変更
```

### 異なるデータベース設定
```yaml
environment:
  - DATABASE_URL=mysql+aiomysql://myuser:mypass@mysql:3306/mydb
```

### 追加の環境変数
```yaml
environment:
  - DATABASE_URL=mysql+aiomysql://inventory_user:inventory_password@mysql:3306/inventory
  - PYTHONPATH=/app
  - LOG_LEVEL=DEBUG
  - API_KEY=your-api-key
```