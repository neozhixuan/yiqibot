from html import escape

from .deployment import DeploymentInfo
from .models import WeddingEvent


def format_reminder(event: WeddingEvent, reminder_minutes: int) -> str:
    start_text = event.start.strftime("%d %b %Y, %H:%M")
    return (
        f"💍 <b>Wedding Reminder: {escape(event.title)}</b>\n\n"
        f"⏰ <b>Starts in {reminder_minutes} minutes:</b> {start_text} SGT\n\n"
        f"{escape(event.message)}\n\n"
        "Wishing everyone a smooth, beautiful, and joyful moment ahead."
    )


def format_deployment_notice(info: DeploymentInfo) -> str:
    lines = ["🚂 <b>Railway deployment notice</b>", "", "A new deployment is now live for this bot."]

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
