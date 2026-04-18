from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from common.reporting.allure_export import export_allure_artifacts
from common.utils.jira_zephyr_rtm import generate_rtm_on_demand
from common.utils.quality_guard import run_quality_checks

ROOT = Path(__file__).parent


def _derive_platform_from_tags(tags: str | None) -> str | None:
    if not tags:
        return None
    lowered = tags.lower()
    if "@mobile" in lowered:
        return "mobile"
    if "@api" in lowered:
        return "api"
    if "@cross" in lowered:
        return "cross"
    if "@web" in lowered:
        return "web"
    return None


def run_pytest(args: argparse.Namespace) -> int:
    platform = args.platform or _derive_platform_from_tags(args.tags) or "web"
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        f"--platform={platform}",
        f"--browser={args.browser}",
        f"--web-engine={args.web_engine}",
    ]
    if args.tags:
        cmd.extend(["-m", args.tags.replace("@", "")])
    if args.tests_path:
        cmd.append(args.tests_path)
    print(f"Running: {' '.join(cmd)}")
    return subprocess.call(cmd, cwd=ROOT)


def main() -> int:
    parser = argparse.ArgumentParser(description="Unified Automation Runner")
    parser.add_argument("--platform", default=None, help="web|mobile|api|cross")
    parser.add_argument("--tags", default=None, help='BDD tags like "@smoke and @web"')
    parser.add_argument("--browser", default="chrome")
    parser.add_argument("--web-engine", default="selenium", choices=["selenium", "playwright"])
    parser.add_argument("--tests-path", default=None)
    parser.add_argument("--quality-check", action="store_true")
    parser.add_argument("--build-allure", action="store_true", help="Generate HTML/PDF/Excel from latest Allure session")
    parser.add_argument(
        "--open-allure",
        action="store_true",
        help="After export, open Allure index.html in the default browser (if present)",
    )
    parser.add_argument("--build-rtm", action="store_true")
    args = parser.parse_args()

    if args.quality_check:
        run_quality_checks(project_root=ROOT)

    exit_code = run_pytest(args)

    if args.build_allure:
        export_allure_artifacts(ROOT / "common" / "reports", open_browser=args.open_allure)

    if args.build_rtm:
        generate_rtm_on_demand()

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
