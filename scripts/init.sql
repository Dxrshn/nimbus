CREATE TABLE IF NOT EXISTS urls (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    original_url TEXT NOT NULL,
    short_code  VARCHAR(10) UNIQUE NOT NULL,
    click_count INTEGER NOT NULL DEFAULT 0,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS click_events (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    short_code  VARCHAR(10) NOT NULL,
    clicked_at  TIMESTAMPTZ NOT NULL,
    user_agent  TEXT,
    referrer    TEXT
);

CREATE INDEX IF NOT EXISTS idx_urls_short_code ON urls(short_code);
CREATE INDEX IF NOT EXISTS idx_click_events_short_code ON click_events(short_code);
