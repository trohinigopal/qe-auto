from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from common.config.settings import SETTINGS
from common.utils.logger import get_logger

LOGGER = get_logger("framework.rtm")


def _fetch_zephyr_testcases() -> list[dict[str, Any]]:
    # Replace with real Zephyr API call.
    return [{"key": "TEST-101", "story": "US-10", "defects": ["BUG-5"]}]


def _fetch_jira_stories() -> list[dict[str, Any]]:
    # Replace with real Jira API call.
    return [{"key": "US-10", "summary": "Netbanking login"}]


def generate_rtm_on_demand() -> Path:
    LOGGER.info("Generating RTM from Jira/Zephyr (base Jira URL: %s)", SETTINGS.jira_base_url)
    testcases = _fetch_zephyr_testcases()
    stories = _fetch_jira_stories()
    payload = {
        "generated_at": datetime.utcnow().isoformat(),
        "stories": stories,
        "testcases": testcases,
    }
    out_file = Path(__file__).resolve().parents[1] / "reports" / "rtm.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    LOGGER.info("RTM generated at %s", out_file)
    return out_file
