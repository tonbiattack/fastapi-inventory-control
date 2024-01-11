from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.product as product_schema
import api.cruds.product as product_crud
from api.db import get_db
from uuid import UUID

router = APIRouter()


@router.get("/products/{product_id}", response_model=product_schema.ProductBase)
async def list_tasks(product_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    指定されたIDの製品情報を取得します。

    :param product_id: 取得したい製品のID。
    :param db: SQLAlchemyの非同期セッションオブジェクト。
    :return: 製品情報。製品が見つからない場合は404エラーを返します。
    """
    product = await product_crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product_schema.ProductBase(
        name=product.name,
        quantity=product.quantity,
        price=product.price
    )


@router.post("/products", response_model=product_schema.ProductCreateResponse)
async def create_product(
    task_body: product_schema.ProductCreate, db: AsyncSession = Depends(get_db)
):
    """
    新しい製品をデータベースに作成します。

    :param task_body: 作成する製品のデータ。
    :param db: SQLAlchemyの非同期セッションオブジェクト。
    :return: 作成された製品の情報。
    """
    return await product_crud.create_product(db, task_body)


@router.put("/products/{product_id}", response_model=product_schema.ProductCreateResponse)
async def update_task(
    product_id: UUID, task_body: product_schema.ProductCreate, db: AsyncSession = Depends(get_db)
):
    """
    指定されたIDの製品を更新します。

    :param product_id: 更新したい製品のID。
    :param task_body: 更新する製品のデータ。
    :param db: SQLAlchemyの非同期セッションオブジェクト。
    :return: 更新された製品の情報。製品が見つからない場合は404エラーを返します。
    """
    task = await product_crud.get_product(db, product_id=product_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await product_crud.update_product(db, task_body, original=task)


@router.delete("/products/{product_id}", response_model=None)
async def delete_product(product_id: UUID, db: AsyncSession = Depends(get_db)):
    """
    指定されたIDの製品を削除します。

    :param product_id: 削除したい製品のID。
    :param db: SQLAlchemyの非同期セッションオブジェクト。
    :return: 削除操作の成否。製品が見つからない場合は404エラーを返します。
    """
    product = await product_crud.get_product(db, product_id=product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    return await product_crud.delete_product(db, original=product)
