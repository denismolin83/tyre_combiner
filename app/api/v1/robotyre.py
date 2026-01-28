from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.services.parser import RobotyreXMLParser
from app.services.storage import StorageService

router = APIRouter(prefix="/robotyre", tags=["Robotyre"])


@router.post("/sync")
async def sync_robotyre_ym(
    background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)
):
    """Импорт данных из Robotyre Yandex Market фида"""

    async def run_import():
        # Фиксируем время начала импорта
        session_start = datetime.now(timezone.utc).replace(tzinfo=None)

        parser = RobotyreXMLParser(
            url=settings.ROBOTYRE_XML_URL, source_name="robotyre_ym"
        )
        products = await parser.parse()

        # UPSERT (обновляем существующие, в том числе поле updated_at)
        await StorageService.upsert_raw_products(db, products, session_start)

        # Обнуляем всех кто в базе, но не пришел в текущем импорте
        await StorageService.reset_outdated_stock(
            db=db, source="robotyre_ym", session_start=session_start
        )

        await db.commit()
        print(f"Imported {len(products)} products from Robotyre Yandex Market feed.")

    background_tasks.add_task(run_import)

    return {"message": "Import from Robotyre Yandex Market feed started in background."}
