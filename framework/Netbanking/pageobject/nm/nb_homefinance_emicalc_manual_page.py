"""Auto-generated page object — replace LOCATORS with real selectors from DevTools."""

from selenium.webdriver.common.by import By


class NbHomefinanceEmicalcManualPage:
    """Placeholder locators extracted from manual testcase wording (quoted phrases)."""

    LOCATORS: dict[str, tuple[str, str]] = {
        "calculate_your_home_loan": (By.CSS_SELECTOR, "[data-testid=\"TODO-calculate_your_home_loan\"]"),  # Calculate Your Home Loan
        "calculate_monthly_emi": (By.CSS_SELECTOR, "[data-testid=\"TODO-calculate_monthly_emi\"]"),  # Calculate monthly EMI
    }

    def __init__(self, driver) -> None:
        self.driver = driver
