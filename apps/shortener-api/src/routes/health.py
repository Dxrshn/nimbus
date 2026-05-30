from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db
from src.services.cache_service import ping as redis_ping

router = APIRouter()


@router.get("/health")
async def liveness():
    return {"status": "ok"}


@router.get("/ready")
async def readiness(db: AsyncSession = Depends(get_db)):
    checks = {}

    try:
        await db.execute(text("SELECT 1"))
        checks["database"] = "ok"
    except Exception:
        checks["database"] = "error"

    checks["redis"] = "ok" if await redis_ping() else "error"

    all_ok = all(v == "ok" for v in checks.values())
    return {"status": "ok" if all_ok else "error", "checks": checks}