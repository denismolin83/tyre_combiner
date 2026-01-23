from app.models.product import RawProduct
from app.schemas.raw_product import RawProductCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

class StorageService:
    @staticmethod
    async def upsert_raw_products(db: AsyncSession, products: list[RawProductCreate]):
        # Логика для добавления или обновления RawProduct в базе данных
        """
        Массовое создание или обновление RawProduct
        Используем PostgreSQL ON CONFLICT для апсерт операции
        """

        if not products:
            return
        
        #Подготовим данные для вставки
        data = [p.model_dump() for p in products]

        #Создаем зарос на вставку
        stmt = insert(RawProduct).values(data)

        #Описываем что обновлять при конфликте (по source и external_id)
        update_stmt = stmt.on_conflict_do_update(
            index_elements=["source", "external_id"],
            set_={
                "name": stmt.excluded.name,
                "price": stmt.excluded.price,
                "stock": stmt.excluded.stock,
                "raw_data": stmt.excluded.raw_data,
                "updated_at": RawProduct.updated_at
            }
        )

        await db.execute(update_stmt)
        await db.commit()