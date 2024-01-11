from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal

from uuid import UUID


class ProductBase(BaseModel):
    """
    製品の基本情報を表すベースクラス。

    Attributes:
        name (str): 製品の名前。最大100文字。
        quantity (int): 在庫数量。0より大きい数値。
        price (Decimal): 製品の価格。0より大きい数値。
    """
    name: str = Field(..., max_length=100, example="製品名", description="製品名")
    quantity: int = Field(..., gt=0, example=10, description="在庫数量")
    price: Decimal = Field(..., gt=0, example="999.99", description="製品の価格")


class ProductCreate(ProductBase):
    """
    製品を作成するために使用するクラス。ProductBaseから継承されます。
    """
    pass


class ProductCreateResponse(ProductBase):
    """
    製品作成後のレスポンスデータを表すクラス。
    ProductBaseから継承され、一意の製品IDが追加されます。

    Attributes:
        id (str): 製品の一意の識別子。
    """
    id: UUID = Field(..., example="123e4567-e89b-12d3-a456-426614174000",
                     description="一意の製品ID")

    class Config:
        orm_mode = True


class ProductRead(ProductBase):
    """
    製品情報を読み取るために使用するクラス。ProductBaseから継承され、一意の製品IDが追加されます。

    Attributes:
        id (str): 一意の製品ID。
    """
    id: UUID = Field(..., example="123e4567-e89b-12d3-a456-426614174000",
                     description="一意の製品ID")


class ProductUpdate(ProductBase):
    """
    製品情報を更新するために使用するクラス。ProductBaseから継承され、
    必要に応じて製品名、数量、価格をオプションで更新できます。

    Attributes:
        name (Optional[str]): 更新される製品名。省略可能。
        quantity (Optional[int]): 更新される在庫数量。省略可能。
        price (Optional[Decimal]): 更新される製品の価格。省略可能。
    """
    name: Optional[str] = Field(
        None, max_length=100, example="更新された製品名", description="製品名")
    quantity: Optional[int] = Field(None, example=5, description="更新された在庫数量")
    price: Optional[Decimal] = Field(
        None, example="1099.99", description="更新された製品の価格")
