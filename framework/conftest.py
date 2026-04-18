from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Generator, Iterator, Optional

import pytest

from common.base.api.api_base import ApiBaseClient
from common.base.mobile.appium_base import AppiumBase
from common.base.web.playwright_base import PlaywrightBase
from common.base.web.selenium_base import SeleniumBase
from common.utils.logger import get_logger

pytest_plugins = ["common.steps.auth_steps"]

LOGGER = get_logger("framework.conftest")

_FRAMEWORK_ROOT = Path(__file__).resolve().parent


def pytest_configure(config: pytest.Config) -> None:
    """Scoped Allure output + media dirs per run (session id + timestamp)."""
    from common.reporting.allure_session import build_session_paths

    paths = build_session_paths(_FRAMEWORK_ROOT)
    ar = str(paths.allure_results.resolve())
    if hasattr(config.option, "allure_report_dir"):
        config.option.allure_report_dir = ar
    os.environ["ALLURE_SESSION_ROOT"] = str(paths.session_root.resolve())
    os.environ["ALLURE_SESSION_MEDIA_DIR"] = str(paths.media.resolve())
    os.environ["ALLURE_SESSION_ID"] = paths.session_id
    LOGGER.info(
        "Allure session: %s | results -> %s",
        paths.folder_name,
        ar,
    )
    config.addinivalue_line("markers", "self_heal: tests that may persist healed locators to *_locators.json")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: Any) -> Any:
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    if rep.when == "call":
        from common.reporting.allure_capture import attach_failure_artifacts

        attach_failure_artifacts(item, rep)


@pytest.fixture(autouse=True)
def _allure_playwright_video_dir(request: pytest.FixtureRequest) -> Iterator[None]:
    """Per-test folder for Playwright video when ALLURE_RECORD_VIDEO=1."""
    if os.getenv("ALLURE_RECORD_VIDEO", "0") != "1":
        yield
        return
    base = os.environ.get("ALLURE_SESSION_MEDIA_DIR")
    if not base:
        yield
        return
    from common.reporting.allure_session import safe_node_id

    sub = Path(base) / "videos" / safe_node_id(request.node.nodeid)
    sub.mkdir(parents=True, exist_ok=True)
    prev = os.environ.get("ALLURE_PLAYWRIGHT_VIDEO_DIR")
    os.environ["ALLURE_PLAYWRIGHT_VIDEO_DIR"] = str(sub)
    yield
    if prev is not None:
        os.environ["ALLURE_PLAYWRIGHT_VIDEO_DIR"] = prev
    else:
        os.environ.pop("ALLURE_PLAYWRIGHT_VIDEO_DIR", None)


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption("--platform", action="store", default=None, help="web|mobile|api|cross")
    parser.addoption("--browser", action="store", default="chrome", help="Browser for Selenium")
    parser.addoption("--web-engine", action="store", default="selenium", help="selenium|playwright")
    parser.addoption("--base-url", action="store", default="https://example-bank.test")
    parser.addoption("--api-base-url", action="store", default="https://example-bank-api.test")


def _resolve_platform(item: pytest.Item, cli_platform: Optional[str]) -> str:
    if cli_platform:
        return cli_platform.lower()
    marker_names = {m.name for m in item.iter_markers()}
    if "mobile" in marker_names:
        return "mobile"
    if "api" in marker_names:
        return "api"
    if "cross" in marker_names:
        return "cross"
    return "web"


@pytest.fixture(scope="session")
def runtime_context(pytestconfig: pytest.Config) -> dict:
    return {
        "platform": pytestconfig.getoption("--platform"),
        "browser": pytestconfig.getoption("--browser"),
        "web_engine": pytestconfig.getoption("--web-engine"),
        "base_url": pytestconfig.getoption("--base-url"),
        "api_base_url": pytestconfig.getoption("--api-base-url"),
    }


@pytest.fixture(scope="function")
def ui_driver(request: pytest.FixtureRequest, runtime_context: dict) -> Generator[object, None, None]:
    platform = _resolve_platform(request.node, runtime_context["platform"])
    if platform not in {"web", "cross"}:
        yield None
        return

    engine = runtime_context["web_engine"].lower()
    if engine == "playwright":
        wrapper = PlaywrightBase(headless=bool(int(os.getenv("HEADLESS", "1"))))
        page = wrapper.start()
        yield page
        wrapper.stop()
        return

    wrapper = SeleniumBase(browser=runtime_context["browser"], headless=bool(int(os.getenv("HEADLESS", "1"))))
    driver = wrapper.start()
    yield driver
    wrapper.stop()


@pytest.fixture(scope="function")
def mobile_driver(request: pytest.FixtureRequest, runtime_context: dict) -> Generator[object, None, None]:
    platform = _resolve_platform(request.node, runtime_context["platform"])
    if platform not in {"mobile", "cross"}:
        yield None
        return
    wrapper = AppiumBase()
    driver = wrapper.start()
    yield driver
    wrapper.stop()


@pytest.fixture(scope="function")
def api_client(request: pytest.FixtureRequest, runtime_context: dict) -> Generator[ApiBaseClient, None, None]:
    platform = _resolve_platform(request.node, runtime_context["platform"])
    if platform not in {"api", "cross"}:
        yield ApiBaseClient(runtime_context["api_base_url"], lazy=True)
        return
    client = ApiBaseClient(runtime_context["api_base_url"])
    yield client
    client.close()


def pytest_sessionfinish(session: pytest.Session, exitstatus: int) -> None:
    from common.utils.locator_persistence import consume_heal_happened

    if consume_heal_happened():
        LOGGER.info(
            "Self-heal updated locator JSON on disk. Re-run tests once (e.g. pytest --reruns 1) "
            "so the suite uses persisted selectors, or rely on in-process retry on the next find."
        )
