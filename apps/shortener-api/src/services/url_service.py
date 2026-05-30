import random
import string
from uuid import UUID

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.url import UrlResponse


def _generate_short_code(length: int = 6) -> str:
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


async def create_short_url(original_url: str, base_url: str, db: AsyncSession) -> dict:
    short_code = _generate_short_code()

    await db.execute(
        text(
            "INSERT INTO urls (short_code, original_url) VALUES (:short_code, :original_url)"
        ),
        {"short_code": short_code, "original_url": original_url},
    )
    await db.commit()

    return {
        "short_code": short_code,
        "short_url": f"{base_url}/r/{short_code}",
    }


async def get_all_urls(base_url: str, db: AsyncSession) -> list[UrlResponse]:
    result = await db.execute(
        text("SELECT id, short_code, original_url, created_at, click_count FROM urls ORDER BY created_at DESC")
    )
    rows = result.fetchall()

    return [
        UrlResponse(
            id=row.id,
            short_code=row.short_code,
            original_url=row.original_url,
            short_url=f"{base_url}/r/{row.short_code}",
            click_count=row.click_count,
            created_at=row.created_at,
        )
        for row in rows
    ]


async def delete_url(url_id: UUID, db: AsyncSession) -> bool:
    result = await db.execute(
        text("DELETE FROM urls WHERE id = :id"),
        {"id": str(url_id)},
    )
    await db.commit()
    return result.rowcount > 0


async def get_url_by_short_code(short_code: str, db: AsyncSession) -> dict | None:
    result = await db.execute(
        text("SELECT id, short_code, original_url, created_at, click_count FROM urls WHERE short_code = :short_code"),
        {"short_code": short_code},
    )
    row = result.fetchone()
    if not row:
        return None
    return dict(row._mapping)