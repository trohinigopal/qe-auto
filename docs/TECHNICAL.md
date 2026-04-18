# qe-auto — Technical Documentation

This document describes the **qe-auto** test automation repository: architecture, features, setup, and operational commands. The executable framework lives under **`framework/`** unless noted otherwise.

---

## 1. Purpose and scope

**qe-auto** hosts a **multi-channel** automation framework for banking-style applications:

| Channel | Technology | Typical use |
|--------|------------|-------------|
| **Netbanking** | Selenium or Playwright | Web UI (browser) |
| **MobileBanking** | Appium | Native / hybrid mobile |
| **API** | `requests` via `ApiBaseClient` | REST / HTTP APIs |
| **CrossChannel** | Selenium/Playwright **+** API client | End-to-end journeys across UI and API |

Tests are written as **Gherkin** (`.feature`) and bound with **pytest-bdd**. Execution is driven by **pytest** with shared **fixtures** (`ui_driver`, `mobile_driver`, `api_client`) defined in `framework/conftest.py`.

---

## 2. Repository layout

```text
qe-auto/
  README.md                    # Short pointer + quick entry
  docs/
    TECHNICAL.md               # This document
  framework/                   # Main automation root (cd here to run commands)
    runner.py                  # CLI wrapper: pytest + optional quality / Allure / RTM
    conftest.py                # Global pytest config, fixtures, Allure session paths, capture hooks
    pytest.ini                 # testpaths, markers (no fixed --alluredir; set in conftest)
    requirements.txt           # Python dependencies
    Netbanking/
      Features/nm/             # Gherkin features
      pageobject/nm/           # Page objects, *_dom_materialized.json, locators JSON
      stepdefination/nm/       # test_*_steps.py (scenarios) + *_step_defs.py (shared steps)
      stepdefination/conftest.py  # pytest_plugins → NB step_defs
    MobileBanking/             # Same pattern
    API/
      Features/nm/
      pageobject/nm/
      stepdefination/nm/
      stepdefination/conftest.py  # pytest_plugins → API step_defs
    CrossChannel/
      Features/nm/
      pageobject/nm/           # e.g. *_journey.py orchestration stubs
      stepdefination/nm/
      conftest.py              # pytest_plugins → NB + API step_defs (reuse)
    UserStories/en/            # User story markdown (input to generators)
    ManualTestCases/en/        # Manual TC markdown (input to manual_tc_to_bdd)
    common/
      base/                    # api_base, selenium_base, playwright_base, appium_base
      reporting/               # allure_export, allure_session, allure_capture
      steps/                   # e.g. auth_steps (pytest_plugins)
      utils/                   # generators, BDD runners, self-heal, Jira/RTM, quality_guard, logger
      logs/, reports/          # Runtime logs; Allure under reports/sessions/
```

**Naming convention (per channel):** same **stem** for `Features/nm/<stem>.feature`, `pageobject/nm/<stem>_page.py` (or `_client.py` / `_journey.py`), and `stepdefination/nm/test_<stem>_steps.py`.

---

## 3. Prerequisites

### 3.1 Required

| Prerequisite | Notes |
|--------------|--------|
| **Python 3.10+** (3.12 used in development) | Virtual environment recommended |
| **pip** | Install `framework/requirements.txt` |
| **Chrome** (or Chromium) | Default for Selenium; install matching **ChromeDriver** or use Selenium Manager (bundled in recent Selenium) |
| **Git** | For cloning the repository |

### 3.2 Optional but recommended

| Software | Purpose |
|----------|---------|
| **Allure Commandline** | Generate interactive HTML from `allure-results` (`npm i -g allure-commandline` or `scoop install allure`) |
| **Node.js / npm** | Installing Allure CLI globally |
| **Firefox** + **geckodriver** | If using `--browser firefox` |
| **Playwright browsers** | After `pip install playwright`, run `playwright install` (or rely on bundled browser for Playwright) |
| **Appium server** + **Android SDK / Xcode** | For real mobile runs (MobileBanking) |
| **JDK** | Often required by Android tooling / Appium ecosystem |

### 3.3 Python dependencies (`framework/requirements.txt`)

| Package | Role |
|---------|------|
| pytest, pytest-bdd | Test runner and Gherkin binding |
| pytest-rerunfailures | Retries (if used in suites) |
| selenium | WebDriver API |
| playwright | Playwright Python API |
| Appium-Python-Client | Mobile |
| requests | HTTP (wrapped by `ApiBaseClient`) |
| allure-pytest | Allure integration |
| pandas, openpyxl, fpdf2 | Allure export (Excel/PDF summaries) |
| python-dotenv | Optional env loading |

---

## 4. Installation and first run

```bash
cd framework
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

pip install -r requirements.txt
# Optional for Playwright-driven tests:
# playwright install
```

**Working directory:** almost all commands assume **`framework/`** as the current working directory.

Smoke check:

```bash
python runner.py --help
python -m pytest --collect-only -q
```

---

## 5. Configuration model

### 5.1 Pytest options (`conftest.py` / CLI)

| Option | Default | Description |
|--------|---------|-------------|
| `--platform` | inferred from markers or `web` | `web` \| `mobile` \| `api` \| `cross` — controls which drivers are real vs lazy |
| `--browser` | `chrome` | Selenium browser name |
| `--web-engine` | `selenium` | `selenium` \| `playwright` |
| `--base-url` | `https://example-bank.test` | Web SUT base URL |
| `--api-base-url` | `https://example-bank-api.test` | API base URL for `ApiBaseClient` |

**Platform resolution:** CLI `--platform` wins; else markers on the test item (`mobile`, `api`, `cross`); else **`web`**.

### 5.2 Fixtures (`conftest.py`)

| Fixture | Scope | Behavior |
|---------|--------|----------|
| `runtime_context` | session | Bundles CLI options for tests/helpers |
| `ui_driver` | function | `None` if platform is not `web`/`cross`. Else Playwright `Page` or Selenium `WebDriver` |
| `mobile_driver` | function | Active for `mobile` / `cross` |
| `api_client` | function | `ApiBaseClient`; lazy for non-API platforms unless `api`/`cross` |

### 5.3 Environment variables (high level)

| Variable | Effect |
|----------|--------|
| `HEADLESS` | `1` headless browser (default); `0` headed |
| `SELF_HEAL` | `1` enables DOM self-heal heuristics; `0` disables |
| `API_TOKEN`, `API_KEY` | Substituted into `*_api_materialized.json` header placeholders `${...}` |
| `ALLURE_SESSION_ID` | Prefix for Allure session folder name |
| `ALLURE_SCREENSHOT_ALWAYS` | `1` attaches screenshot after every call-phase step (UI/mobile) |
| `ALLURE_RECORD_VIDEO` | `1` enables Playwright video recording per test under session `media/videos/` |

---

## 6. Feature areas (how they work)

### 6.1 BDD execution (pytest-bdd)

1. **Feature files** (`Features/nm/*.feature`) hold Gherkin scenarios.
2. **Step definitions** are Python functions decorated with `@given` / `@when` / `@then` (often `parsers.parse("exact text")`).
3. **Scenario tests** in `test_<stem>_steps.py` use `@scenario("path/to.feature", "Scenario Name")`.

**Important:** pytest collects **fixtures** from `conftest.py` and from modules listed in **`pytest_plugins`**. Step implementations that live in `*_step_defs.py` must be loaded via:

- `Netbanking/stepdefination/conftest.py` → `nb_homefinance_emicalc_manual_step_defs`
- `API/stepdefination/conftest.py` → `api_my_feature_step_defs`
- `CrossChannel/conftest.py` → both NB and API step_defs for cross scenarios

Without this, steps in a separate file would not register as pytest fixtures and pytest-bdd would raise **StepDefinitionNotFoundError**.

### 6.2 User story → manual testcase → BDD (generators)

| Utility | Module | Input | Output |
|---------|--------|-------|--------|
| User story → manual TC | `common.utils.user_story_to_manual` | `UserStories/en/*.md` | `ManualTestCases/en/*.md` |
| Manual TC → BDD | `common.utils.manual_tc_to_bdd` | Manual markdown | `.feature`, `*_page.py`, `test_*_steps.py` |

**manual_tc_to_bdd** builds Gherkin and stub step files under the chosen **channel** (`Netbanking`, `MobileBanking`, `API`, `CrossChannel`).

Example:

```bash
cd framework
python -m common.utils.manual_tc_to_bdd -i ManualTestCases/en/example.md -c Netbanking -p NB_example_feature --tag web
```

### 6.3 Web: DOM materialization (`bdd_dom_materialize`)

After manual→BDD output:

1. **`bdd_dom_materialize`** opens real URLs in Selenium, uses **`dom_self_heal.suggest_locator_from_dom`** to propose locators per step, and writes **`pageobject/nm/<stem>_dom_materialized.json`**.
2. It **patches** `test_*_steps.py` so each step calls **`bdd_step_runner.execute_materialized_step(ui_driver, step_text, _FW, channel, stem)`**.
3. **`bdd_step_runner.execute_materialized_step`** loads the JSON, applies **navigation heuristics** (e.g. open base URL / secondary URL) and then **click / assert** using stored selectors where present.

```bash
python -m common.utils.bdd_dom_materialize -c Netbanking -p nb_homefinance_emicalc_manual ^
  --base-url https://example.com/ --secondary-url https://example.com/subpage
```

| Flag | Meaning |
|------|---------|
| `--headed` | Browser headed during scan |
| `--min-score` | DOM match threshold |
| `--patch-only` | Skip browser; rewrite JSON + patch steps only |

### 6.4 API: contract materialization (`api_bdd_materialize`)

1. Writes **`pageobject/nm/<stem>_api_materialized.json`** with `api_base_url`, `endpoints`, `payloads`, `default_headers` (supports `${API_TOKEN}`-style env substitution at runtime).
2. Patches steps to call **`api_bdd_step_runner.execute_api_materialized_step(api_client, step_text, _FW, channel, stem)`**.
3. The runner maps **acceptance criterion** phrases and keywords to POST/GET and assertions (2xx/4xx, HTTPS, etc.).

```bash
python -m common.utils.api_bdd_materialize -c API -p api_my_feature --api-base-url https://api.example.com
python -m common.utils.api_bdd_materialize -c API -p api_my_feature --api-base-url https://api.example.com --config overrides.json
```

### 6.5 Cross-channel scenarios

- **Feature** lives under `CrossChannel/Features/nm/`.
- **Steps are not duplicated:** `CrossChannel/conftest.py` loads Netbanking and API **`_step_defs`** modules via `pytest_plugins`.
- Run with **`--platform cross`** so both **`ui_driver`** and **`api_client`** are active.
- Example feature: web EMI flow steps + API lead steps in one scenario.

### 6.6 Self-heal and locator persistence

- **`dom_self_heal`**: suggests locators from visible DOM (used by materializer and optional runtime healing).
- **`locator_persistence`**: hooks in `pytest_sessionfinish` can log when healed locators were written to disk (`self_heal` marker in `pytest.ini`).

### 6.7 Allure reporting (session-scoped)

On each pytest run, **`conftest.py`** calls **`allure_session.build_session_paths`**, which creates:

`common/reports/sessions/<session_id>_<YYYYMMDD_HHMMSS>/`

and sets **`config.option.allure_report_dir`** to that folder’s **`allure-results`**.

After the run, **`allure_export.export_allure_artifacts`** can:

- Run **`allure generate`** (needs **Allure CLI** on PATH) → `allure-html/index.html`
- Emit **`allure_summary.xlsx`** and **`allure_summary.pdf`** from parsed `*-result.json`
- Write **`report_hub.html`** with links to HTML, PDF, Excel, and `media/` folders

**Capture:**

- **Screenshots:** on failure (or always if `ALLURE_SCREENSHOT_ALWAYS=1`) via `allure_capture.attach_failure_artifacts`.
- **Video:** Playwright only, when `ALLURE_RECORD_VIDEO=1` and per-test dirs under `media/videos/`.

Latest session pointer: **`common/reports/sessions/LATEST_SESSION.txt`**.

### 6.8 Unified runner (`runner.py`)

- Invokes **pytest** with `--platform`, `--browser`, `--web-engine`, optional **`-m`** from `--tags`.
- Optional **`--quality-check`** (before tests), **`--build-allure`**, **`--open-allure`**, **`--build-rtm`**.

Platform default from tags: `@mobile` → mobile, `@api` → api, `@cross` → cross, `@web` → web; else **web**.

### 6.9 Other utilities (reference)

| Module | Role |
|--------|------|
| `common.utils.jira_zephyr_rtm` | RTM / Zephyr integration hooks (`--build-rtm`) |
| `common.utils.quality_guard` | Quality checks (`--quality-check`) |
| `common.utils.logger` | Logging to `common/logs/` |
| `common.utils.gcp_utils` | GCP-related helpers (if used by your pipelines) |
| `common.steps.auth_steps` | Shared auth-related steps (`pytest_plugins` in root `conftest`) |

---

## 7. Command reference

### 7.1 Runner (`framework/runner.py`)

```bash
cd framework

python runner.py
python runner.py --platform web|mobile|api|cross
python runner.py --platform web --browser firefox --web-engine playwright
python runner.py --tags "@smoke"
python runner.py --tags "@web and @smoke"
python runner.py --tests-path Netbanking/stepdefination/nm/test_nb_homefinance_emicalc_manual_steps.py

python runner.py --quality-check
python runner.py --build-allure
python runner.py --build-allure --open-allure
python runner.py --build-rtm
```

### 7.2 Pytest (direct)

Supports **`--base-url`** and **`--api-base-url`** (not passed by `runner.py` today — use for real SUT URLs).

```bash
cd framework

python -m pytest
python -m pytest -m "smoke and web"
python -m pytest Netbanking/stepdefination/nm/test_nb_homefinance_emicalc_manual_steps.py --platform web --base-url https://your-web-app/
python -m pytest API/stepdefination/nm/test_api_my_feature_steps.py --platform api --api-base-url https://your-api/
python -m pytest CrossChannel/stepdefination/nm/test_CC_authentication_cross_login_steps.py --platform cross --base-url https://your-web/ --api-base-url https://your-api/
```

### 7.3 Generators

```bash
cd framework

python -m common.utils.user_story_to_manual -i UserStories/en/story.md -o ManualTestCases/en/out_manual.md

python -m common.utils.manual_tc_to_bdd -i ManualTestCases/en/foo.md -c Netbanking -p NB_feature --tag web

python -m common.utils.bdd_dom_materialize -c Netbanking -p <stem> --base-url https://... [--secondary-url https://...]

python -m common.utils.api_bdd_materialize -c API -p <stem> --api-base-url https://... [--config path.json]
```

### 7.4 Allure export (programmatic)

```bash
cd framework
python -c "from pathlib import Path; from common.reporting.allure_export import export_allure_artifacts; export_allure_artifacts(Path('common/reports'))"
```

---

## 8. Test discovery (`pytest.ini`)

`testpaths` includes all four channel **`stepdefination`** trees. Collecting **everything** can be heavy; narrow with **file path** or **`-m`** markers.

Registered **markers** include: `web`, `mobile`, `api`, `cross`, `smoke`, `regression`, `generated`, `self_heal`.

---

## 9. CI/CD notes

- Set **`PLATFORM`**, **`TAGS`**, **`BROWSER`**, **`WEB_ENGINE`** to match `runner.py` options.
- Install **Python deps** and optionally **Allure CLI** on the agent for HTML reports.
- Expose **secrets** (`API_TOKEN`, etc.) via CI variables, not committed JSON.
- Archive **`common/reports/sessions/`** (or copy `LATEST_SESSION` contents) as build artifacts.

---

## 10. Troubleshooting

| Symptom | Likely cause | Action |
|---------|----------------|--------|
| `StepDefinitionNotFoundError` | Step module not loaded as `pytest_plugins` | Ensure `stepdefination/conftest.py` exists for that channel and lists `*_step_defs` |
| Allure HTML not generated | `allure` CLI missing | Install Allure commandline; PDF/Excel may still be produced |
| API tests skip or wrong client | Wrong `--platform` | Use `--platform api` or `cross` as needed |
| DNS / connection errors | Placeholder base URLs | Point `--api-base-url` / materialized JSON to reachable hosts |
| Unicode errors in PDF export | Non-ASCII in summaries | Export uses ASCII-safe paths for PDF table cells |

---

## 11. Related documents

- **`framework/README.md`** — concise operational README (commands and quick reference).
- **`qe-auto/README.md`** — repository entry and link to `framework/README.md`.

---

*Document version: aligned with repository layout and tooling as of the last update. For behavior of specific classes, see source under `framework/common/` and channel folders.*
