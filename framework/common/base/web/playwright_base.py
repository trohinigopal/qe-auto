from __future__ import annotations

import os
from pathlib import Path

from playwright.sync_api import Browser, BrowserContext, Page, Playwright, sync_playwright


class PlaywrightBase:
    def __init__(self, headless: bool = True) -> None:
        self.headless = headless
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None
        self._context: BrowserContext | None = None
        self.page: Page | None = None

    def start(self) -> Page:
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=self.headless)

        video_dir = os.environ.get("ALLURE_PLAYWRIGHT_VIDEO_DIR")
        record_video = os.getenv("ALLURE_RECORD_VIDEO", "0") == "1" and video_dir

        if record_video:
            p = Path(video_dir)
            p.mkdir(parents=True, exist_ok=True)
            self._context = self._browser.new_context(
                record_video_dir=str(p),
                record_video_size={"width": 1280, "height": 720},
            )
        else:
            self._context = self._browser.new_context()

        self.page = self._context.new_page()
        return self.page

    def stop(self) -> None:
        if self._context:
            self._context.close()
        if self._browser:
            self._browser.close()
        if self._playwright:
            self._playwright.stop()

    def open(self, url: str) -> None:
        assert self.page is not None
        self.page.goto(url)

    def click(self, selector: str) -> None:
        assert self.page is not None
        self.page.locator(selector).click()

    def fill(self, selector: str, value: str) -> None:
        assert self.page is not None
        self.page.locator(selector).fill(value)
