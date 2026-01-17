from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.parser import RobotyreXMLParser
from app.services.storage import StorageService
from app.config import settings

router = APIRouter(prefix="/imports", tags=["imports"])

@router.post("/robotyre_ym")
async def import_robotyre_ym(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Импорт данных из Robotyre Yandex Market фида"""

    async def run_import():
        parser = RobotyreXMLParser(
            url=settings.ROBOTYRE_XML_URL,
            source_name="robotyre_ym"
        )
        products = await parser.parse()
        await StorageService.upsert_raw_products(db, products)
        print(f"Imported {len(products)} products from Robotyre Yandex Market feed.")
    
    background_tasks.add_task(run_import)
    
    return {"message": "Import from Robotyre Yandex Market feed started in background."}
