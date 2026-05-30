import asyncpg

from src.models import ClickEvent


async def process(event: ClickEvent, db: asyncpg.Connection) -> None:
    await db.execute(
        """
        INSERT INTO click_events (short_code, clicked_at, user_agent, referrer)
        VALUES ($1, $2, $3, $4)
        """,
        event.short_code,
        event.clicked_at,
        event.user_agent,
        event.referrer,
    )

    await db.execute(
        "UPDATE urls SET click_count = click_count + 1 WHERE short_code = $1",
        event.short_code,
    )
