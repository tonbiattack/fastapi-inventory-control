from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Column, String, Integer, DECIMAL
from api.db import Base


class Product(Base):
    """
    製品情報を表すデータモデルクラスです。

    このクラスはSQLAlchemyのBaseクラスを継承しており、
    データベースのproductsテーブルにマッピングされています。

    :param id: 製品の一意識別子。UUID形式。
    :param name: 製品の名前。最大100文字の文字列。
    :param quantity: 製品の数量。整数値。
    :param price: 製品の価格。10桁までの小数2桁までの数値。
    """
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
