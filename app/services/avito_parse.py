import io

import pandas as pd

from app.schemas.avito import AvitoExcelItem
from app.schemas.raw_product import RawProductCreate


from app.services.parser import BaseParser


class AvitoExcelParser(BaseParser):
    async def parse(self) -> list[RawProductCreate]:
        content = await self._download()

        # Читаем нужный лист
        df = pd.read_excel(
            io.BytesIO(content), 
            sheet_name="Шины, диски и кол-Легковые шины",
            skiprows=1
        )

        # Убираем пустые строки
        df = df.dropna(how="all").reset_index(drop=True)

        parsed_items = []
        for _, row in df.iterrows():
            try:
                raw_dict = row.to_dict()

                if pd.isna(raw_dict.get("Уникальный идентификатор объявления")):
                    continue

                item = AvitoExcelItem(**raw_dict)

                parsed_items.append(
                    RawProductCreate(
                        source=self.source_name,
                        external_id=item.id,
                        name=item.name,
                        vendor=item.brand,
                        price=item.price,
                        stock=int(item.stock),
                        raw_data={
                            "description": item.description,
                            "original_data": {k: v for k, v in raw_dict.items() if pd.notna(v)}
                        }
                    )
                )

            except Exception as e:
                continue

        return parsed_items
