import asyncio
from warehouse.db.database import async_session
from warehouse.models import SKU


async def seed():
    async with async_session() as session:
        paints = [
            SKU(
                sku="PAINT-WHT-1L",
                ean="5901234123457",
                name="White Paint 1L",
                description="Interior matt white",
            ),
            SKU(
                sku="PAINT-WHT-5L",
                ean="5901234123458",
                name="White Paint 5L",
                description="Interior matt white",
            ),
            SKU(
                sku="PAINT-BLK-1L",
                ean="5901234123459",
                name="Black Paint 1L",
                description="Interior matt black",
            ),
            SKU(
                sku="PAINT-RED-1L",
                ean="5901234123460",
                name="Red Paint 1L",
                description="Interior gloss red",
            ),
            SKU(
                sku="PRIMER-1L",
                ean="5901234123461",
                name="Primer 1L",
                description="Universal primer",
            ),
        ]

        session.add_all(paints)
        await session.commit()
        print(f"Seeded {len(paints)} SKUs")


if __name__ == "__main__":
    asyncio.run(seed())
