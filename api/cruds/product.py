from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import api.models.product as product_model
import api.schemas.product as product_schema


async def create_product(
    db: AsyncSession, product_create: product_schema.ProductCreate
) -> product_model.Product:
    """
    新しい製品をデータベースに作成します。

    :param db: SQLAlchemyの非同期セッションオブジェクト。
    :param product_create: 新しく作成する製品の情報を含むスキーマオブジェクト。
    :return: 作成された製品のモデルインスタンス。
    """
    product = product_model.Product(**product_create.dict())
    db.add(product)
    await db.commit()
    await db.refresh(product)
    return product


async def get_product(db: AsyncSession, product_id: str) -> product_model.Product | None:
    """
    指定されたIDを持つ製品をデータベースから取得します。

    :param db: SQLAlchemyの非同期セッションオブジェクト。
    :param product_id: 取得する製品のID。
    :return: 指定されたIDを持つ製品のモデルインスタンス。該当する製品がない場合はNone。
    """
    result: Result = await db.execute(
        select(product_model.Product).filter(
            product_model.Product.id == product_id)
    )
    return result.scalars().first()


async def update_product(
    db: AsyncSession, product_create: product_schema.ProductCreate, original: product_model.Product
) -> product_model.Product:
    """
    指定された製品情報で既存の製品を更新します。

    :param db: SQLAlchemyの非同期セッションオブジェクト。
    :param product_create: 更新する製品の新しい情報を含むスキーマオブジェクト。
    :param original: 更新する製品の既存モデルインスタンス。
    :return: 更新された製品のモデルインスタンス。
    """
    original.name = product_create.name
    original.price = product_create.price
    original.quantity = product_create.quantity
    db.add(original)
    await db.commit()
    await db.refresh(original)
    return original


async def delete_product(db: AsyncSession, original: product_model.Product) -> None:
    """
    データベースから指定された製品を削除します。

    :param db: SQLAlchemyの非同期セッションオブジェクト。
    :param original: 削除する製品のモデルインスタンス。
    """
    await db.delete(original)
    await db.commit()
