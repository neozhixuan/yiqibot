from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import timedelta
from typing import Mapping
from zoneinfo import ZoneInfo

from dotenv import load_dotenv


DEFAULT_TIMEZONE_NAME = "Asia/Singapore"
DEFAULT_REMINDER_MINUTES = 10


@dataclass(frozen=True)
class BotSettings:
    bot_token: str
    raw_channel_id: str
    timezone_name: str = DEFAULT_TIMEZONE_NAME
    reminder_minutes: int = DEFAULT_REMINDER_MINUTES
    railway_deployment_id: str | None = None
    railway_project_name: str | None = None
    railway_service_name: str | None = None
    railway_environment_name: str | None = None
    railway_image: str | None = None
    railway_git_commit_sha: str | None = None

    @property
    def channel_id(self) -> str:
        if self.raw_channel_id.startswith("-100"):
            return self.raw_channel_id
        return f"-100{self.raw_channel_id}"

    @property
    def timezone(self) -> ZoneInfo:
        return ZoneInfo(self.timezone_name)

    @property
    def reminder_offset(self) -> timedelta:
        return timedelta(minutes=self.reminder_minutes)


def _get_first_value(source: Mapping[str, str], *keys: str) -> str | None:
    for key in keys:
        value = source.get(key)
        if value:
            return value
    return None


def _require_value(source: Mapping[str, str], *keys: str) -> str:
    value = _get_first_value(source, *keys)
    if value is None:
        joined_keys = ", ".join(keys)
        raise ValueError(f"Missing required environment variable: {joined_keys}")
    return value


def get_settings(env: Mapping[str, str] | None = None) -> BotSettings:
    if env is None:
        load_dotenv()
        source = os.environ
    else:
        source = env

    return BotSettings(
        bot_token=_require_value(source, "BOT_TOKEN"),
        raw_channel_id=_require_value(source, "RAW_CHANNEL_ID", "CHANNEL_ID"),
        timezone_name=source.get("TIMEZONE_NAME", DEFAULT_TIMEZONE_NAME),
        reminder_minutes=int(source.get("REMINDER_MINUTES", DEFAULT_REMINDER_MINUTES)),
        railway_deployment_id=source.get("RAILWAY_DEPLOYMENT_ID"),
        railway_project_name=source.get("RAILWAY_PROJECT_NAME"),
        railway_service_name=source.get("RAILWAY_SERVICE_NAME"),
        railway_environment_name=source.get("RAILWAY_ENVIRONMENT_NAME"),
        railway_image=source.get("RAILWAY_IMAGE"),
        railway_git_commit_sha=source.get("RAILWAY_GIT_COMMIT_SHA"),
    )
