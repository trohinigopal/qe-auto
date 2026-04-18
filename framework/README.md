# Enterprise Unified Automation Framework

> **Full technical documentation** (architecture, prerequisites, feature deep-dives, command matrix): [`../docs/TECHNICAL.md`](../docs/TECHNICAL.md)

Unified automation framework for banking channels:

- Netbanking (web UI)
- Mobile Banking (native/hybrid app)
- API Banking
- Cross Channel journeys

Stack:

- `pytest`, `pytest-bdd`
- Selenium or Playwright (web)
- Appium (mobile)
- `requests` (API)
- Allure reporting
- Jira + Zephyr RTM utility hooks

**Working directory for every command below:** `framework/` (the folder that contains `runner.py`, `conftest.py`, and `pytest.ini`).

```bash
cd framework
```

---

## Prerequisites

```bash
python -m venv venv
# Windows: venv\Scripts\activate
# Unix:    source venv/bin/activate

pip install -r requirements.txt
```

Optional: install a browser driver (e.g. Chrome + matching ChromeDriver) for Selenium UI tests.

---

## Run tests (unified runner)

`runner.py` forwards to `pytest` with `--platform` and optional tag filtering.

| Command | Description |
|--------|-------------|
| `python runner.py` | Defaults: platform `web`, browser `chrome`, engine `selenium` |
| `python runner.py --platform web` | Web UI tests |
| `python runner.py --platform mobile` | Mobile (Appium) |
| `python runner.py --platform api` | API tests |
| `python runner.py --platform cross` | Cross-channel (web + API drivers; see below) |
| `python runner.py --platform web --browser firefox` | Alternate browser |
| `python runner.py --web-engine playwright` | Playwright instead of Selenium |
| `python runner.py --tags "@smoke"` | Pytest marker expression (`@` stripped) |
| `python runner.py --tags "@web and @smoke"` | Combined markers |
| `python runner.py --tests-path Netbanking/stepdefination/nm/test_nb_homefinance_emicalc_manual_steps.py` | Single file or path |
| `python runner.py --quality-check` | Run quality checks before pytest |
| `python runner.py --build-allure` | After tests, generate Allure HTML + PDF + Excel + `report_hub.html` (latest session) |
| `python runner.py --build-allure --open-allure` | Same, then open Allure `index.html` in the default browser |
| `python runner.py --build-rtm` | After tests, generate RTM (Zephyr/Jira hook) |

Platform from tags (if `--platform` omitted): `@mobile` → mobile, `@api` → api, `@cross` → cross, `@web` → web.

Example:

```bash
python runner.py --platform cross --tests-path CrossChannel/stepdefination/nm/test_CC_authentication_cross_login_steps.py
```

---

## Run tests (pytest directly)

Use this when you need options the runner does not pass (e.g. base URLs).

| Option | Purpose |
|--------|---------|
| `--platform web\|mobile\|api\|cross` | Which drivers are active (`conftest.py`) |
| `--browser chrome` | Browser for Selenium |
| `--web-engine selenium\|playwright` | Web automation backend |
| `--base-url https://...` | Web SUT base URL (default in `conftest`: `https://example-bank.test`) |
| `--api-base-url https://...` | API base URL (default: `https://example-bank-api.test`) |

Examples:

```bash
# All tests under configured testpaths (see pytest.ini)
python -m pytest

# Netbanking BDD (web)
python -m pytest Netbanking/stepdefination/nm/test_nb_homefinance_emicalc_manual_steps.py --platform web --base-url https://homeloans.hdfc.bank.in/

# API BDD
python -m pytest API/stepdefination/nm/test_api_my_feature_steps.py --platform api --api-base-url https://httpbin.org

# Cross-channel (needs both Selenium session and API client)
python -m pytest CrossChannel/stepdefination/nm/test_CC_authentication_cross_login_steps.py --platform cross --base-url https://homeloans.hdfc.bank.in/ --api-base-url https://httpbin.org
```

Markers (see `pytest.ini`):

```bash
python -m pytest -m "smoke and web"
python -m pytest -m cross
```

---

## Environment variables (runtime)

| Variable | Typical use |
|----------|-------------|
| `HEADLESS` | `1` (default) headless browser; `0` headed |
| `SELF_HEAL` | `1` allow DOM self-heal; `0` disable |
| `API_TOKEN`, `API_KEY` | Substituted in `*_api_materialized.json` headers (`${API_TOKEN}`) |
| `ALLURE_SESSION_ID` | Optional short id prefix for the report folder name (default: random hex) |
| `ALLURE_SCREENSHOT_ALWAYS` | `1` to attach a screenshot after every UI step (not only failures) |
| `ALLURE_RECORD_VIDEO` | `1` to record Playwright video per test into the session `media/videos/` tree |

---

## Allure reports (session-scoped)

Each pytest run creates a **unique folder**:

`common/reports/sessions/<session_id>_<YYYYMMDD_HHMMSS>/`

Under it:

| Path | Content |
|------|---------|
| `allure-results/` | Raw Allure JSON (`*-result.json`, attachments) |
| `allure-html/` | Generated site (after export) — **`index.html`** |
| `allure_summary.xlsx` | Spreadsheet: every test row with status, duration, labels, messages |
| `allure_summary.pdf` | Compact PDF table (same data subset) |
| `report_hub.html` | Links to HTML report, PDF, Excel, and `media/` folders |
| `media/screenshots/` | Reserved for screenshots (failures attach to Allure + optional files here) |
| `media/videos/` | Playwright `.webm` when `ALLURE_RECORD_VIDEO=1` |
| `manifest.json` | Session metadata |
| `../sessions/LATEST_SESSION.txt` | Points to the last session root (for automation) |

**Install Allure CLI** (required for the interactive HTML report):

```bash
npm install -g allure-commandline
# or: scoop install allure
```

**Generate reports** after a test run (uses the latest session in `LATEST_SESSION.txt`):

```bash
python -c "from pathlib import Path; from common.reporting.allure_export import export_allure_artifacts; export_allure_artifacts(Path('common/reports'))"
```

Or via runner:

```bash
python runner.py --build-allure
python runner.py --build-allure --open-allure
```

**Screenshots:** on failed UI/mobile steps, a PNG is attached to Allure automatically. Set `ALLURE_SCREENSHOT_ALWAYS=1` to attach after every call-phase step.

**Video:** Playwright only — set `ALLURE_RECORD_VIDEO=1` (uses per-test folders under `media/videos/`). Selenium does not record video in this framework.

---

## Generate BDD from manual test cases

Produces a `.feature`, page object stub, and `test_<stem>_steps.py` under the chosen channel.

```bash
python -m common.utils.manual_tc_to_bdd -i ManualTestCases/en/your_case.md -c Netbanking -p NB_your_feature --tag web
```

Channels: `Netbanking`, `MobileBanking`, `API`, `CrossChannel`.

---

## Web: DOM materialize (after manual → BDD)

Scans the browser DOM, writes `pageobject/nm/<stem>_dom_materialized.json`, and patches step defs to call `bdd_step_runner.execute_materialized_step`.

```bash
python -m common.utils.bdd_dom_materialize -c Netbanking -p nb_homefinance_emicalc_manual ^
  --base-url https://homeloans.hdfc.bank.in/ ^
  --secondary-url https://homeloans.hdfc.bank.in/home-loan-emi-calculator
```

| Flag | Meaning |
|------|---------|
| `--headed` | Run browser headed (`HEADLESS=0` for the scan) |
| `--min-score 0.22` | DOM hint match threshold |
| `--patch-only` | Skip Selenium; refresh JSON + patch steps only |

---

## API: contract materialize (after manual → BDD)

Writes `pageobject/nm/<stem>_api_materialized.json` and patches steps to call `api_bdd_step_runner.execute_api_materialized_step`.

```bash
python -m common.utils.api_bdd_materialize -c API -p api_my_feature --api-base-url https://your-api-host.example
```

Optional merge file for real paths/payloads:

```bash
python -m common.utils.api_bdd_materialize -c API -p api_my_feature --api-base-url https://your-api-host.example --config path/to/overrides.json
```

---

## Cross-channel tests

Cross-channel scenarios live under `CrossChannel/Features/nm/`. Step implementations are **not** duplicated: `CrossChannel/conftest.py` loads

- `Netbanking.stepdefination.nm.nb_homefinance_emicalc_manual_step_defs`
- `API.stepdefination.nm.api_my_feature_step_defs`

Run with **`--platform cross`** so `ui_driver` and `api_client` are both active.

---

## Folder structure

```text
framework/
  Netbanking/   MobileBanking/   API/   CrossChannel/
    Features/nm/    pageobject/nm/    stepdefination/nm/
  common/
    base/  reporting/  steps/  utils/  logs/  reports/
  conftest.py
  pytest.ini
  runner.py
```

---

## Feature and file naming

Gherkin files: `Features/nm/<PREFIX>_<epic>_<feature>.feature`

Related assets use the same stem under `pageobject/nm/` and `stepdefination/nm/test_<stem>_steps.py`. See the table in earlier sections of this file for patterns (`*_page.py`, `*_client.py`, `*_journey.py`).

---

## Jenkins / CI

Typical pipeline variables:

- `PLATFORM=web|mobile|api|cross`
- `TAGS=@smoke`
- `BROWSER=chrome|firefox`
- `WEB_ENGINE=selenium|playwright`

Example:

```bash
python runner.py --platform %PLATFORM% --tags "%TAGS%" --browser %BROWSER% --web-engine %WEB_ENGINE%
```

---

## Reporting and quality (via runner)

- Allure export: `python runner.py --build-allure` (`common/reporting/allure_export.py`) — see **Allure reports** above
- RTM / Zephyr: `python runner.py --build-rtm` (`common/utils/jira_zephyr_rtm.py`)
- Quality checks: `python runner.py --quality-check` (`common/utils/quality_guard.py`)

Pytest’s Allure output directory is set in `conftest.py` (session folder under `common/reports/sessions/`), not in `pytest.ini`.

---

## Notes

- Shared auth steps: `common/steps/auth_steps.py` (loaded via `pytest_plugins` in `conftest.py`).
- Cross-channel reuses Netbanking + API **step definition modules** (`*_step_defs.py`); see `CrossChannel/conftest.py`.
- Avoid duplicate Gherkin step text across features unless they intentionally share the same step definition.
