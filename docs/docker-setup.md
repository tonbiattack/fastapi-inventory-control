# Docker環境構築手順

## 概要
FastAPIアプリケーションとMySQLデータベースをDockerで構築し、VSCodeのリモートデバッグを可能にする手順です。

## 必要なファイル

### 1. docker-compose.yml
```yaml
version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: inventory_mysql
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: inventory
      MYSQL_USER: inventory_user
      MYSQL_PASSWORD: inventory_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./db/products.sql:/docker-entrypoint-initdb.d/products.sql
    networks:
      - inventory_network

  fastapi:
    build: .
    container_name: inventory_fastapi
    ports:
      - "8000:8000"
      - "5678:5678"  # Debug port
    volumes:
      - .:/app
    depends_on:
      - mysql
    environment:
      - DATABASE_URL=mysql+aiomysql://inventory_user:inventory_password@mysql:3306/inventory
      - PYTHONPATH=/app
    networks:
      - inventory_network
    command: python -m debugpy --listen 0.0.0.0:5678 --wait-for-client -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  mysql_data:

networks:
  inventory_network:
    driver: bridge
```

### 2. Dockerfile
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000 5678

CMD ["python", "-m", "debugpy", "--listen", "0.0.0.0:5678", "--wait-for-client", "-m", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
```

### 3. requirements.txt
```txt
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy==2.0.23
aiomysql==0.2.0
debugpy==1.8.0
pydantic==2.5.0
```

## 構築手順

1. **プロジェクトルートで実行**：
   ```bash
   docker-compose up --build
   ```

2. **動作確認**：
   - FastAPI: http://localhost:8000
   - MySQL: localhost:3306

3. **データベース接続情報**：
   - Host: localhost (外部から) / mysql (コンテナ内)
   - Port: 3306
   - User: inventory_user
   - Password: inventory_password
   - Database: inventory

## 重要なポイント

### デバッグポート設定
- ポート5678をデバッグ用に開放
- `--wait-for-client`フラグでデバッガー接続を待機

### 環境変数の活用
- `DATABASE_URL`でデータベース接続文字列を設定
- `PYTHONPATH`でPythonパスを設定

### ネットワーク設定
- `inventory_network`でサービス間通信を設定
- MySQLサービス名`mysql`をホスト名として使用

### ボリュームマウント
- ソースコードの変更がリアルタイムで反映
- MySQLデータは永続化ボリュームで保存
- 初期化SQLファイルを自動実行

## トラブルシューティング

### よくある問題と解決法

1. **MySQLコンテナが起動しない**
   - ポート3306が既に使用されている場合は、別のポートを使用

2. **FastAPIアプリがMySQLに接続できない**
   - ネットワーク設定を確認
   - 環境変数の値を確認

3. **デバッグが接続できない**
   - ポート5678が開放されているか確認
   - VSCodeのデバッグ設定を確認

## 停止・削除手順

```bash
# コンテナ停止
docker-compose down

# ボリュームも含めて削除
docker-compose down -v

# イメージも削除
docker-compose down --rmi all
```