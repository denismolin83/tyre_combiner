from datetime import datetime, timezone
import httpx

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.services.storage import StorageService
from app.services.avito_parse import AvitoExcelParser


router = APIRouter(prefix="/avito", tags=["Avitio Excel"])


async def get_yandex_downlod_url(public_url: str) -> str:
    # Здесь можно реализовать логику получения прямой ссылки на скачивание файла
    # Например, если public_url требует аутентификации или специальных параметров

    api_url = "https://cloud-api.yandex.net"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{api_url}/v1/disk/public/resources/download",
            params={"public_key": public_url},
        )
        response.raise_for_status()
        data = response.json()
        direct_link = data.get("href")

    return direct_link


@router.post("/sync")
async def sync_avito_excel(background_tasks: BackgroundTasks, db: AsyncSession = Depends(get_db)):
    """Импорт данных из Avito Excel файла"""

    async def run_import():
        # Фиксируем время начала импорта
        session_start = datetime.now(timezone.utc).replace(tzinfo=None)

        my_disk_url = "https://disk.yandex.ru/i/vPnuZtHPX07hjA"

        direct_link = await get_yandex_downlod_url(public_url=my_disk_url)

        #Парсим
        parser = AvitoExcelParser(url=direct_link, source_name="excel_avito")
        products = await parser.parse()
        print(products)

        # UPSERT (обновляем существующие, в том числе поле updated_at)
        await StorageService.upsert_raw_products(db, products, session_start)

        # Обнуляем всех кто в базе, но не пришел в текущем импорте
        await StorageService.reset_outdated_stock(
            db=db, source="excel_avito", session_start=session_start
        )

        await db.commit()
        print(f"Imported {len(products)} products from Avito Excel file.")

    background_tasks.add_task(run_import)

    return {"message": "Import from Avito Excel file started in background."}
