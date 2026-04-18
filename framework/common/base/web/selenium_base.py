from __future__ import annotations

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class SeleniumBase:
    def __init__(self, browser: str = "chrome", headless: bool = True, timeout: int = 20) -> None:
        self.browser = browser
        self.headless = headless
        self.timeout = timeout
        self.driver: webdriver.Remote | None = None

    def start(self):
        if self.browser != "chrome":
            raise NotImplementedError("Starter supports chrome only. Extend as needed.")
        options = ChromeOptions()
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(options=options)
        return self.driver

    def stop(self) -> None:
        if self.driver:
            self.driver.quit()
            self.driver = None

    def open(self, url: str) -> None:
        assert self.driver is not None
        self.driver.get(url)

    def click(self, locator: tuple[str, str]) -> None:
        assert self.driver is not None
        WebDriverWait(self.driver, self.timeout).until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: tuple[str, str], value: str) -> None:
        assert self.driver is not None
        element = WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(value)

    def text(self, locator: tuple[str, str]) -> str:
        assert self.driver is not None
        return WebDriverWait(self.driver, self.timeout).until(EC.visibility_of_element_located(locator)).text

    @staticmethod
    def by_id(value: str) -> tuple[str, str]:
        return By.ID, value
