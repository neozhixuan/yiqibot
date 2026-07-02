from dataclasses import dataclass
from datetime import datetime, timedelta


@dataclass(frozen=True)
class WeddingEvent:
    title: str
    start: datetime
    message: str

    def reminder_time(self, reminder_offset: timedelta) -> datetime:
        return self.start - reminder_offset
