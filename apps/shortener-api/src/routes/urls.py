from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.models.url import ShortenRequest, ShortenResponse, UrlResponse
from src.services.cache_service import delete_cached_url, get_cached_url, set_cached_url
from src.services.url_service import (
    create_short_url,
    delete_url,
    get_all_urls,
    get_url_by_short_code,
)

router = APIRouter(prefix="/v1")


@router.post("/shorten", response_model=ShortenResponse, status_code=201)
async def shorten_url(
    payload: ShortenRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    base_url = str(request.base_url).rstrip("/")
    result = await create_short_url(str(payload.url), base_url, db)
    await set_cached_url(result["short_code"], str(payload.url))
    return result


@router.get("/urls", response_model=list[UrlResponse])
async def list_urls(request: Request, db: AsyncSession = Depends(get_db)):
    base_url = str(request.base_url).rstrip("/")
    return await get_all_urls(base_url, db)


@router.get("/urls/{short_code}/stats", response_model=UrlResponse)
async def url_stats(short_code: str, request: Request, db: AsyncSession = Depends(get_db)):
    base_url = str(request.base_url).rstrip("/")
    row = await get_url_by_short_code(short_code, db)
    if not row:
        raise HTTPException(status_code=404, detail="URL not found")
    return UrlResponse(
        id=row["id"],
        short_code=row["short_code"],
        original_url=row["original_url"],
        short_url=f"{base_url}/r/{row['short_code']}",
        click_count=row["click_count"],
        created_at=row["created_at"],
    )


@router.delete("/urls/{url_id}", status_code=204)
async def remove_url(url_id: UUID, db: AsyncSession = Depends(get_db)):
    row = await get_url_by_short_code(str(url_id), db)
    if row:
        await delete_cached_url(row["short_code"])
    deleted = await delete_url(url_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="URL not found")