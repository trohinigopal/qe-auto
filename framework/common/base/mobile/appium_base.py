from __future__ import annotations

import os

from appium import webdriver
from appium.options.android import UiAutomator2Options


class AppiumBase:
    def __init__(self) -> None:
        self.server_url = os.getenv("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
        self.driver = None

    def start(self):
        options = UiAutomator2Options().load_capabilities(
            {
                "platformName": os.getenv("MOBILE_PLATFORM", "Android"),
                "appium:automationName": "UiAutomator2",
                "appium:deviceName": os.getenv("DEVICE_NAME", "Android Emulator"),
                "appium:appPackage": os.getenv("APP_PACKAGE", ""),
                "appium:appActivity": os.getenv("APP_ACTIVITY", ""),
                "appium:noReset": True,
            }
        )
        self.driver = webdriver.Remote(self.server_url, options=options)
        return self.driver

    def stop(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None
