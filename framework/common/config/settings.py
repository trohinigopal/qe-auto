from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    base_url: str = os.getenv("BASE_URL", "https://example-bank.test")
    api_base_url: str = os.getenv("API_BASE_URL", "https://example-bank-api.test")
    jira_base_url: str = os.getenv("JIRA_BASE_URL", "")
    jira_user: str = os.getenv("JIRA_USER", "")
    jira_token: str = os.getenv("JIRA_TOKEN", "")
    zephyr_base_url: str = os.getenv("ZEPHYR_BASE_URL", "")
    zephyr_token: str = os.getenv("ZEPHYR_TOKEN", "")
    gcp_project_id: str = os.getenv("GCP_PROJECT_ID", "")


SETTINGS = Settings()
