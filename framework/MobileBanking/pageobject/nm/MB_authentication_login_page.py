"""Mobile banking app login — maps to Features/nm/MB_authentication_login.feature."""





class MobileBankingLoginPage:

    """Page object for mobile app login (PIN/password/biometric flows)."""



    def __init__(self, driver) -> None:

        self.driver = driver



    def login(self, username: str, password: str) -> None:

        _ = (username, password)

