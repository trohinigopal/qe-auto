"""Auto-generated page object — replace LOCATORS with real selectors from DevTools."""

from selenium.webdriver.common.by import By


class NbMyFeaturePage:
    """Placeholder locators extracted from manual testcase wording (quoted phrases)."""

    LOCATORS: dict[str, tuple[str, str]] = {
        "page_root": (By.TAG_NAME, "body"),
    }

    def __init__(self, driver) -> None:
        self.driver = driver
