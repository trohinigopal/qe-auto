"""Netbanking web login — maps to Features/nm/NB_authentication_login.feature."""





class NetbankingLoginPage:

    """Page object for netbanking username/password login and post-login shell."""



    def __init__(self, driver) -> None:

        self.driver = driver



    def login(self, username: str, password: str) -> None:

        # Add actual locators and actions.

        _ = (username, password)

