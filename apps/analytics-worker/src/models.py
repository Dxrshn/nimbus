from dataclasses import dataclass
from datetime import datetime


@dataclass
class ClickEvent:
    short_code: str
    clicked_at: datetime
    user_agent: str
    referrer: str

    @classmethod
    def from_dict(cls, data: dict) -> "ClickEvent":
        return cls(
            short_code=data["short_code"],
            clicked_at=datetime.fromisoformat(data["clicked_at"]),
            user_agent=data.get("user_agent", ""),
            referrer=data.get("referrer", ""),
        )
