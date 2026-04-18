"""REST client for account details — maps to Features/nm/API_accounts_get_details.feature."""





class AccountsGetDetailsApiClient:

    """Calls account-related endpoints (balances, profile, limits)."""



    def __init__(self, api_client) -> None:

        self.api_client = api_client



    def get_account(self):

        return self.api_client.get("/accounts/12345")

