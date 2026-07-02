from __future__ import annotations

from html import escape

from .deployment import DeploymentInfo
from .models import WeddingEvent


def _format_next_event_preview(next_event: WeddingEvent | None) -> str:
    if next_event is None:
        return "🫶 <b>Next up:</b> This is the last scheduled reminder."

    next_start_text = next_event.start.strftime("%d %b %Y, %H:%M")
    return f"🫶 <b>Next up:</b> {escape(next_event.title)} at {next_start_text} SGT"


def format_reminder(
    event: WeddingEvent,
    reminder_minutes: int,
    next_event: WeddingEvent | None = None,
) -> str:
    start_text = event.start.strftime("%d %b %Y, %H:%M")
    return (
        f"💍 <b>Wedding Reminder: {escape(event.title)}</b>\n\n"
        f"⏰ <b>Starts in {reminder_minutes} minutes:</b> {start_text} SGT\n\n"
        f"{escape(event.message)}\n\n"
        f"{_format_next_event_preview(next_event)}\n\n"
        "Wishing everyone a smooth, beautiful, and joyful moment ahead."
    )


def format_deployment_notice(info: DeploymentInfo) -> str:
    lines = ["✨ <b>Zaiyiqi bot has updated!</b>", "", "A fresh Railway deployment is now live and ready to help."]

    if info.project_name or info.service_name:
        project_label = escape(info.project_name or "Unknown project")
        service_label = escape(info.service_name or "Unknown service")
        lines.append(f"Project/Service: {project_label} / {service_label}")

    if info.environment_name:
        lines.append(f"Environment: {escape(info.environment_name)}")

    if info.deployment_id:
        lines.append(f"Deployment ID: {escape(info.deployment_id)}")

    if info.image:
        lines.append(f"Image: {escape(info.image)}")

    if info.short_commit_sha:
        lines.append(f"Commit: {escape(info.short_commit_sha)}")

    lines.extend(["", "The Railway worker has restarted and is ready to continue sending reminders."])
    return "\n".join(lines)
