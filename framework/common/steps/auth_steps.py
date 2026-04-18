from __future__ import annotations

from pytest_bdd import given, parsers, then, when


@given(parsers.parse('user logs in with username "{username}" and password "{password}"'))
def common_login(runtime_context: dict, ui_driver, mobile_driver, username: str, password: str) -> None:
    """
    Shared login step for netbanking/mobile/cross channel.
    Actual login actions should be delegated to page objects.
    """
    platform = (runtime_context.get("platform") or "").lower()
    if ui_driver:
        # Hook web login actions here.
        pass
    elif mobile_driver:
        # Hook mobile login actions here.
        pass
    elif platform == "cross":
        # Cross-channel can compose from web + mobile + api fixtures.
        pass


@when("user lands on account summary")
def user_lands_on_account_summary() -> None:
    pass


@then("dashboard should be visible")
def dashboard_should_be_visible() -> None:
    pass
