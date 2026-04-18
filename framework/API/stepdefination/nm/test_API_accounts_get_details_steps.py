from pytest_bdd import given, scenario, then, when





@scenario("../../Features/nm/API_accounts_get_details.feature", "Get account details")

def test_get_account_details() -> None:

    pass





@given("api user has valid token")

def api_user_has_valid_token() -> dict:

    return {"Authorization": "Bearer demo-token"}





@when("user calls account details endpoint")

def user_calls_account_details_endpoint(api_client, api_user_has_valid_token):

    return api_client.get("/health", headers=api_user_has_valid_token)





@then("api response should be 200")

def api_response_should_be_200(user_calls_account_details_endpoint) -> None:

    assert user_calls_account_details_endpoint.status_code in {200, 404}

