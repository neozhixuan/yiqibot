from __future__ import annotations

import logging

from telegram import Bot
from telegram.constants import ParseMode

from .deployment import DeploymentInfo
from .messages import format_deployment_notice, format_reminder
from .models import WeddingEvent


logger = logging.getLogger(__name__)


async def send_html_message(bot: Bot, channel_id: str, text: str) -> None:
    await bot.send_message(
        chat_id=channel_id,
        text=text,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True,
    )


async def send_reminder(
    bot: Bot,
    channel_id: str,
    event: WeddingEvent,
    reminder_minutes: int,
    next_event: WeddingEvent | None = None,
) -> None:
    try:
        await send_html_message(bot, channel_id, format_reminder(event, reminder_minutes, next_event))
        logger.info("Sent reminder for '%s' to channel %s", event.title, channel_id)
    except Exception:
        logger.exception("Failed to send reminder for '%s'; continuing to next event", event.title)


async def send_deployment_notice(bot: Bot, channel_id: str, info: DeploymentInfo) -> None:
    try:
        await send_html_message(bot, channel_id, format_deployment_notice(info))
        logger.info("Sent Railway deployment notice to channel %s", channel_id)
    except Exception:
        logger.exception("Failed to send Railway deployment notice; continuing with scheduler startup")
