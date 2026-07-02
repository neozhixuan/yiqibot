from __future__ import annotations

from dataclasses import dataclass

from .app_config import BotSettings


@dataclass(frozen=True)
class DeploymentInfo:
    deployment_id: str | None
    project_name: str | None
    service_name: str | None
    environment_name: str | None
    image: str | None
    git_commit_sha: str | None

    @property
    def short_commit_sha(self) -> str | None:
        if not self.git_commit_sha:
            return None
        return self.git_commit_sha[:7]


def get_deployment_info(settings: BotSettings) -> DeploymentInfo | None:
    if not settings.railway_deployment_id and not settings.railway_image:
        return None

    return DeploymentInfo(
        deployment_id=settings.railway_deployment_id,
        project_name=settings.railway_project_name,
        service_name=settings.railway_service_name,
        environment_name=settings.railway_environment_name,
        image=settings.railway_image,
        git_commit_sha=settings.railway_git_commit_sha,
    )
