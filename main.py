import asyncio
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

from bot.app_config import get_settings
from bot.events import get_events
from bot.scheduler import run_scheduler


def main() -> None:
    settings = get_settings()
    events = get_events(settings.timezone)
    asyncio.run(run_scheduler(settings, events))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Wedding reminder bot stopped manually.")
