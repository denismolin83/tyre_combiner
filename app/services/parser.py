from abc import ABC, abstractmethod

import httpx
from lxml import etree

from ..schemas.raw_product import RawProductCreate
from ..schemas.robotyre import RobotyreXMLItem


class BaseParser(ABC):
    """Базовый класс для парсеров"""

    url: str
    source_name: str

    def __init__(self, url: str, source_name: str):
        self.url = url
        self.source_name = source_name

    async def _download(self) -> bytes:
        """Загружает данные по URL асинхронно"""
        async with httpx.AsyncClient(timeout=120.0, follow_redirects=True) as client:
            response = await client.get(self.url)
            response.raise_for_status()
            return response.content

    @abstractmethod
    async def parse(self) -> list[RawProductCreate]:
        """Парсит данные и возвращает список RawProductCreate"""
        pass


class RobotyreXMLParser(BaseParser):
    async def parse(self) -> list[RawProductCreate]:
        content = await self._download()
        root = etree.fromstring(content)
        offers = root.findall(".//offer")

        parsed_items = []
        for offer in offers:
            # 1. Собираем все картинки в список
            pictures = [p.text for p in offer.xpath("./picture") if p.text]

            # 2. Собираем параметры в словарь
            params = {
                p.get("name"): p.text
                for p in offer.xpath("./param")
                if p.get("name") and p.text
            }

            # 3. Валидируем через RobotyreXMLItem
            raw_item = RobotyreXMLItem(
                id=offer.get("id"),
                name=offer.findtext("name", default=""),
                vendor=offer.findtext("vendor"),
                price=float(offer.findtext("price", default="0.0")),
                count=int(offer.findtext("count", default="0")),
                picture=pictures,
                params=params,
            )

            # 4. Преобразуем в RawProductCreate
            parsed_items.append(
                RawProductCreate(
                    source=self.source_name,
                    external_id=raw_item.id,
                    name=raw_item.name,
                    vendor=raw_item.vendor,
                    price=raw_item.price,
                    stock=raw_item.count,
                    raw_data={
                        "params": raw_item.params,
                        "all_pictures": [str(p) for p in raw_item.picture],
                    },
                )
            )

        return parsed_items
