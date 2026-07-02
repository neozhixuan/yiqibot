from __future__ import annotations

import asyncio
import logging
from collections.abc import Awaitable, Callable, Sequence
from datetime import datetime

from telegram import Bot

from .app_config import BotSettings
from .deployment import DeploymentInfo, get_deployment_info
from .models import WeddingEvent
from .notifier import send_deployment_notice, send_reminder


logger = logging.getLogger(__name__)

NowProvider = Callable[[], datetime]
SleepFn = Callable[[float], Awaitable[None]]
ReminderSender = Callable[[Bot, str, WeddingEvent, int], Awaitable[None]]
DeploymentSender = Callable[[Bot, str, DeploymentInfo], Awaitable[None]]
BotFactory = Callable[[str], Bot]


def create_bot(token: str) -> Bot:
    return Bot(token=token)


def get_current_time(settings: BotSettings, now_provider: NowProvider | None = None) -> datetime:
    if now_provider is not None:
        return now_provider()
    return datetime.now(settings.timezone)


async def run_scheduler(
    settings: BotSettings,
    events: Sequence[WeddingEvent],
    bot_factory: BotFactory = create_bot,
    sleep: SleepFn = asyncio.sleep,
    now_provider: NowProvider | None = None,
    reminder_sender: ReminderSender = send_reminder,
    deployment_sender: DeploymentSender = send_deployment_notice,
) -> None:
    bot = bot_factory(settings.bot_token)
    sorted_events = sorted(events, key=lambda event: event.reminder_time(settings.reminder_offset))
    deployment_info = get_deployment_info(settings)

    logger.info(
        "Wedding reminder bot started. Timezone: %s. Channel: %s",
        settings.timezone_name,
        settings.channel_id,
    )
    logger.info("Loaded %d wedding events", len(sorted_events))

    async with bot:
        if deployment_info is not None:
            await deployment_sender(bot, settings.channel_id, deployment_info)

        for event in sorted_events:
            now = get_current_time(settings, now_provider)
            reminder_time = event.reminder_time(settings.reminder_offset)

            if reminder_time <= now:
                logger.info(
                    "Skipping '%s' because reminder time already passed: %s SGT",
                    event.title,
                    reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
                )
                continue

            wait_seconds = (reminder_time - now).total_seconds()
            logger.info(
                "Next reminder: '%s' at %s SGT. Sleeping for %.0f seconds.",
                event.title,
                reminder_time.strftime("%Y-%m-%d %H:%M:%S"),
                wait_seconds,
            )

            await sleep(wait_seconds)
            await reminder_sender(bot, settings.channel_id, event, settings.reminder_minutes)

    logger.info("All wedding reminders have been processed. Bot exiting.")
