"""Attach screenshots and Playwright videos to Allure reports."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any


def attach_png(data: bytes, name: str) -> None:
    try:
        import allure
        from allure_commons.types import AttachmentType

        allure.attach(data, name=name, attachment_type=AttachmentType.PNG)
    except Exception:
        pass


def attach_webm(data: bytes, name: str) -> None:
    try:
        import allure
        from allure_commons.types import AttachmentType

        allure.attach(data, name=name, attachment_type=AttachmentType.WEBM)
    except Exception:
        pass


def attach_screenshot_from_driver(driver: Any, name: str = "screenshot") -> None:
    """Selenium / Appium WebDriver."""
    try:
        attach_png(driver.get_screenshot_as_png(), name)
    except Exception:
        pass


def attach_screenshot_from_playwright(page: Any, name: str = "screenshot") -> None:
    try:
        attach_png(page.screenshot(), name)
    except Exception:
        pass


def attach_latest_playwright_video(video_dir: Path, name: str = "playwright-video") -> None:
    if not video_dir.is_dir():
        return
    webms = sorted(video_dir.glob("*.webm"), key=lambda p: p.stat().st_mtime, reverse=True)
    if not webms:
        return
    path = webms[0]
    try:
        attach_webm(path.read_bytes(), f"{name}-{path.name}")
    except OSError:
        pass


def attach_failure_artifacts(item: Any, rep: Any) -> None:
    """Call from pytest_runtest_makereport when rep.when == 'call'."""
    if rep.when != "call":
        return
    always = os.getenv("ALLURE_SCREENSHOT_ALWAYS", "0") == "1"
    failed = getattr(rep, "failed", False) or getattr(rep, "outcome", None) == "failed"
    if not failed and not always:
        return

    funcargs = getattr(item, "funcargs", None) or {}
    if not funcargs:
        req = getattr(item, "_request", None)
        if req is not None:
            funcargs = getattr(req, "funcargs", {}) or {}

    ui = funcargs.get("ui_driver")
    if ui is not None:
        if type(ui).__name__ == "Page":
            attach_screenshot_from_playwright(ui, "ui-screenshot")
        else:
            attach_screenshot_from_driver(ui, "ui-screenshot")

    mob = funcargs.get("mobile_driver")
    if mob is not None:
        attach_screenshot_from_driver(mob, "mobile-screenshot")

    if os.getenv("ALLURE_RECORD_VIDEO", "0") == "1":
        try:
            from common.reporting.allure_session import safe_node_id

            base = os.environ.get("ALLURE_SESSION_MEDIA_DIR")
            if base:
                vdir = Path(base) / "videos" / safe_node_id(item.nodeid)
                attach_latest_playwright_video(vdir, "execution-video")
        except Exception:
            pass
