from datetime import datetime

from sqlalchemy import update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import RawProduct
from app.schemas.raw_product import RawProductCreate


class StorageService:
    @staticmethod
    async def upsert_raw_products(
        db: AsyncSession, products: list[RawProductCreate], session_time: datetime
    ):
        # Логика для добавления или обновления RawProduct в базе данных
        """
        Массовое создание или обновление RawProduct
        Используем PostgreSQL ON CONFLICT для апсерт операции
        """

        if not products:
            return

        # Подготовим данные для вставки
        data = [p.model_dump() for p in products]

        # Создаем зарос на вставку
        stmt = insert(RawProduct).values(data)

        # Описываем что обновлять при конфликте (по source и external_id)
        update_stmt = stmt.on_conflict_do_update(
            index_elements=["source", "external_id"],
            set_={
                "name": stmt.excluded.name,
                "price": stmt.excluded.price,
                "stock": stmt.excluded.stock,
                "raw_data": stmt.excluded.raw_data,
                "updated_at": session_time,
            },
        )

        await db.execute(update_stmt)
        # wait db.commit()

    @staticmethod
    async def reset_outdated_stock(
        db: AsyncSession, source: str, session_start: datetime
    ):
        """
        Сбросить остаток у не обновленных товаров
        """

        stmt = (
            update(RawProduct)
            .where(RawProduct.source == source)
            .where(RawProduct.updated_at < session_start)  # не обновились сейчас
            .where(RawProduct.stock > 0)  # и еще имеют остаток
            .values(stock=0)
        )

        result = await db.execute(stmt)
        print(f"[{source}] Занулено устаревших товаров: {result.rowcount}")
