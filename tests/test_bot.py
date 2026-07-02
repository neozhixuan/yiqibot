import unittest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock
from zoneinfo import ZoneInfo

from bot.app_config import BotSettings, get_settings
from bot.deployment import DeploymentInfo, get_deployment_info
from bot.events import get_events
from bot.messages import format_deployment_notice, format_reminder
from bot.models import WeddingEvent
from bot.notifier import send_reminder
from bot.scheduler import run_scheduler


SGT = ZoneInfo("Asia/Singapore")


class DummyBot:
    def __init__(self) -> None:
        self.send_message = AsyncMock()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class BotTests(unittest.IsolatedAsyncioTestCase):
    def test_get_settings_adds_channel_prefix(self) -> None:
        settings = get_settings({"BOT_TOKEN": "token", "RAW_CHANNEL_ID": "12345"})
        self.assertEqual(settings.channel_id, "-10012345")

    def test_get_settings_keeps_existing_channel_prefix(self) -> None:
        settings = get_settings({"BOT_TOKEN": "token", "RAW_CHANNEL_ID": "-10012345"})
        self.assertEqual(settings.channel_id, "-10012345")

    def test_get_settings_accepts_channel_id_env_var(self) -> None:
        settings = get_settings({"BOT_TOKEN": "token", "CHANNEL_ID": "-10012345"})
        self.assertEqual(settings.channel_id, "-10012345")

    def test_get_settings_keeps_channel_username(self) -> None:
        settings = get_settings({"BOT_TOKEN": "token", "CHANNEL_ID": "@zaiyiqibot_channel"})
        self.assertEqual(settings.channel_id, "@zaiyiqibot_channel")

    def test_get_settings_requires_bot_token(self) -> None:
        with self.assertRaises(ValueError):
            get_settings({"RAW_CHANNEL_ID": "12345"})

    def test_wedding_event_reminder_time_uses_offset(self) -> None:
        event = WeddingEvent(
            title="Tea Ceremony",
            start=datetime(2026, 7, 4, 10, 0, tzinfo=SGT),
            message="Prepare tea.",
        )
        self.assertEqual(
            event.reminder_time(timedelta(minutes=10)),
            datetime(2026, 7, 4, 9, 50, tzinfo=SGT),
        )

    def test_get_events_returns_wedding_schedule(self) -> None:
        events = get_events(SGT)
        self.assertEqual(len(events), 26)
        self.assertEqual(events[0].title, "Parents Veiling & Shu Tou")
        self.assertEqual(events[0].start.tzinfo, SGT)

    def test_format_reminder_includes_minutes_and_escapes_html(self) -> None:
        event = WeddingEvent(
            title="Photos <Now>",
            start=datetime(2026, 7, 4, 16, 30, tzinfo=SGT),
            message="Bring <bouquet> & smile.",
        )
        message = format_reminder(event, 10)
        self.assertIn("Wedding Reminder: Photos &lt;Now&gt;", message)
        self.assertIn("Starts in 10 minutes:", message)
        self.assertIn("Bring &lt;bouquet&gt; &amp; smile.", message)

    def test_get_deployment_info_returns_none_without_railway_markers(self) -> None:
        settings = BotSettings(
            bot_token="token",
            raw_channel_id="12345",
        )
        self.assertIsNone(get_deployment_info(settings))

    def test_format_deployment_notice_includes_short_commit(self) -> None:
        info = DeploymentInfo(
            deployment_id="dep-123",
            project_name="wedding-bot",
            service_name="worker",
            environment_name="production",
            image="sha256:test",
            git_commit_sha="abcdef1234567890",
        )
        message = format_deployment_notice(info)
        self.assertIn("dep-123", message)
        self.assertIn("sha256:test", message)
        self.assertIn("abcdef1", message)

    async def test_send_reminder_sends_expected_telegram_message(self) -> None:
        bot = DummyBot()
        event = WeddingEvent(
            title="Banquet",
            start=datetime(2026, 7, 4, 18, 0, tzinfo=SGT),
            message="Guests are arriving.",
        )

        await send_reminder(bot, "-10012345", event, 10)

        bot.send_message.assert_awaited_once()
        call = bot.send_message.await_args.kwargs
        self.assertEqual(call["chat_id"], "-10012345")
        self.assertIn("Wedding Reminder: Banquet", call["text"])
        self.assertTrue(call["disable_web_page_preview"])

    async def test_run_scheduler_skips_past_events_and_sends_future_events(self) -> None:
        settings = BotSettings(
            bot_token="token",
            raw_channel_id="12345",
            reminder_minutes=10,
        )
        now = datetime(2026, 7, 4, 10, 0, tzinfo=SGT)
        past_event = WeddingEvent(
            title="Past Event",
            start=datetime(2026, 7, 4, 10, 5, tzinfo=SGT),
            message="Past",
        )
        future_event = WeddingEvent(
            title="Future Event",
            start=datetime(2026, 7, 4, 10, 20, tzinfo=SGT),
            message="Future",
        )
        bot = DummyBot()
        sleep = AsyncMock()
        reminder_sender = AsyncMock()
        deployment_sender = AsyncMock()
        now_values = iter([now, now])

        await run_scheduler(
            settings,
            [future_event, past_event],
            bot_factory=lambda token: bot,
            sleep=sleep,
            now_provider=lambda: next(now_values),
            reminder_sender=reminder_sender,
            deployment_sender=deployment_sender,
        )

        deployment_sender.assert_not_awaited()
        sleep.assert_awaited_once_with(600.0)
        reminder_sender.assert_awaited_once_with(bot, "-10012345", future_event, 10)

    async def test_run_scheduler_sends_deployment_notice_on_startup(self) -> None:
        settings = BotSettings(
            bot_token="token",
            raw_channel_id="12345",
            railway_deployment_id="dep-123",
            railway_service_name="worker",
        )
        bot = DummyBot()
        sleep = AsyncMock()
        reminder_sender = AsyncMock()
        deployment_sender = AsyncMock()

        await run_scheduler(
            settings,
            [],
            bot_factory=lambda token: bot,
            sleep=sleep,
            reminder_sender=reminder_sender,
            deployment_sender=deployment_sender,
        )

        deployment_sender.assert_awaited_once()
        reminder_sender.assert_not_awaited()
        sleep.assert_not_awaited()


if __name__ == "__main__":
    unittest.main()
