"""
After manual_tc_to_bdd output, scan DOM at --base-url, persist locators, and patch step
definitions so steps call bdd_step_runner.execute_materialized_step.

Usage (from framework directory):
  python -m common.utils.bdd_dom_materialize -c Netbanking -p nb_homefinance_emicalc_manual \\
    --base-url https://homeloans.hdfc.bank.in/ \\
    --secondary-url https://homeloans.hdfc.bank.in/home-loan-emi-calculator
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
from pathlib import Path

from common.base.web.selenium_base import SeleniumBase
from common.utils.bdd_feature_parse import normalize_step_text
from common.utils.dom_self_heal import suggest_locator_from_dom


def extract_step_strings_from_steps_py(steps_py: Path) -> list[str]:
    """Step texts exactly as in parsers.parse(...) — must match pytest-bdd registration."""
    content = steps_py.read_text(encoding="utf-8")
    tree = ast.parse(content)
    out: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Name):
            continue
        if node.func.id not in ("given", "when", "then"):
            continue
        if not node.args:
            continue
        inner = node.args[0]
        if not isinstance(inner, ast.Call) or not isinstance(inner.func, ast.Attribute):
            continue
        if inner.func.attr != "parse" or not inner.args:
            continue
        arg0 = inner.args[0]
        if isinstance(arg0, ast.Constant) and isinstance(arg0.value, str):
            out.append(arg0.value)
    return out


def _hints_for_step(step_text: str) -> list[str]:
    t = normalize_step_text(step_text)
    hints = [t]
    for chunk in re.split(r"[,;(]", t):
        c = chunk.strip()
        if len(c) > 12:
            hints.append(c[:120])
    for q in re.findall(r"[\"“]([^\"”]+)[\"”]", step_text):
        if len(q) > 3:
            hints.append(q)
    seen: set[str] = set()
    ordered: list[str] = []
    for h in hints:
        h = h.strip()
        if h and h not in seen:
            seen.add(h)
            ordered.append(h)
    return ordered[:12]


def _by_to_str(by_val: object) -> str:
    s = str(by_val).lower()
    if s.startswith("by."):
        return s.split(".", 1)[-1]
    return s


def _scan_steps_on_pages(
    driver,
    step_texts: list[str],
    urls: list[str],
    min_score: float,
) -> dict[str, dict[str, str]]:
    """Return normalized step key -> {by, selector} for best match across URLs."""
    results: dict[str, dict[str, str]] = {}
    for step in step_texts:
        best: tuple[str, str] | None = None
        for url in urls:
            if not url:
                continue
            driver.get(url)
            driver.implicitly_wait(1)
            hints = _hints_for_step(step)
            loc = suggest_locator_from_dom(driver, hints, min_score=min_score)
            if loc:
                best = (_by_to_str(loc[0]), loc[1])
                break
        if best:
            results[normalize_step_text(step)] = {"by": best[0], "selector": best[1]}
    return results


def _inject_mat_constants(content: str, channel: str, stem: str) -> str:
    if "_MAT_STEM" in content:
        return content
    marker = "from pytest_bdd import given, parsers, scenario, then, when"
    if marker not in content:
        marker = "from pytest_bdd import"
    if marker not in content:
        raise RuntimeError("Could not find pytest_bdd import to inject _MAT_CHANNEL / _MAT_STEM")
    inj = f"\n\n_MAT_CHANNEL = {channel!r}\n_MAT_STEM = {stem!r}\n"
    return content.replace(marker, marker + inj, 1)


def _patch_step_file(content: str, channel: str, stem: str) -> str:
    """Replace stub step bodies with execute_materialized_step(...). Uses _FW from generator."""
    content = _inject_mat_constants(content, channel, stem)
    fw_name = "_FW" if re.search(r"^_FW\s*=", content, re.MULTILINE) else "_MAT_FW"
    if fw_name == "_MAT_FW" and "_MAT_FW" not in content:
        insert_at = content.find("from pytest_bdd import")
        if insert_at == -1:
            raise RuntimeError("Cannot resolve framework root variable")
        line_end = content.find("\n", insert_at)
        after = content.find("\n", line_end + 1)
        content = (
            content[:after]
            + "\n_MAT_FW = Path(__file__).resolve().parents[3]\n"
            + content[after:]
        )

    pattern = re.compile(
        r"(@(given|when|then)\(parsers\.parse\(\s*\"((?:[^\"\\]|\\.)*)\"\s*\)\)\s*\n)"
        r"(def\s+(step_\w+)\(\)\s*->\s*None:\s*\n)"
        r"(?:\s*_.*?\n)*?\s*pass\s*\n",
        re.MULTILINE,
    )

    def repl(m: re.Match[str]) -> str:
        prefix = m.group(1)
        step_literal = m.group(3)
        func_name = m.group(5)
        rep = repr(step_literal)
        return (
            f"{prefix}"
            f"def {func_name}(ui_driver):\n"
            f"    if ui_driver is None:\n"
            f"        import pytest\n"
            f"        pytest.skip('Web driver required for this step')\n"
            f"    from common.utils.bdd_step_runner import execute_materialized_step\n"
            f"    execute_materialized_step(ui_driver, {rep}, {fw_name}, _MAT_CHANNEL, _MAT_STEM)\n"
        )

    new_content, n = pattern.subn(repl, content)
    if n == 0:
        raise RuntimeError(
            "No stub steps matched. Expected @given/@when/@then with parsers.parse and body `pass` "
            "as produced by manual_tc_to_bdd."
        )
    return new_content


def run(
    framework_root: Path,
    channel: str,
    stem: str,
    base_url: str,
    secondary_url: str | None,
    browser: str,
    headless: bool,
    min_score: float,
    patch_only: bool,
) -> None:
    stem = stem.lower().replace("-", "_")
    feat = framework_root / channel / "Features" / "nm" / f"{stem}.feature"
    steps_py = framework_root / channel / "stepdefination" / "nm" / f"test_{stem}_steps.py"
    out_json = framework_root / channel / "pageobject" / "nm" / f"{stem}_dom_materialized.json"

    if not feat.is_file():
        raise SystemExit(f"Feature not found: {feat}")
    if not steps_py.is_file():
        raise SystemExit(f"Step file not found: {steps_py}")

    step_texts = extract_step_strings_from_steps_py(steps_py)
    if not step_texts:
        raise SystemExit(f"No parsers.parse steps found in {steps_py}")

    urls = [base_url]
    if secondary_url:
        urls.append(secondary_url)

    materialized_steps: dict[str, dict[str, str]] = {}
    old_self_heal = os.environ.get("SELF_HEAL")
    old_headless = os.environ.get("HEADLESS")

    if patch_only and out_json.is_file():
        try:
            prev = json.loads(out_json.read_text(encoding="utf-8"))
            materialized_steps = dict(prev.get("steps") or {})
        except (json.JSONDecodeError, OSError):
            materialized_steps = {}
    elif not patch_only:
        os.environ["SELF_HEAL"] = "1"
        os.environ["HEADLESS"] = "0" if not headless else os.environ.get("HEADLESS", "1")
        wrap = SeleniumBase(browser=browser, headless=headless)
        drv = wrap.start()
        try:
            materialized_steps = _scan_steps_on_pages(drv, step_texts, urls, min_score=min_score)
        finally:
            wrap.stop()
            if old_headless is None:
                os.environ.pop("HEADLESS", None)
            else:
                os.environ["HEADLESS"] = old_headless
            if old_self_heal is None:
                os.environ.pop("SELF_HEAL", None)
            else:
                os.environ["SELF_HEAL"] = old_self_heal

    payload: dict[str, object] = {
        "base_url": base_url,
        "secondary_url": secondary_url or "",
        "channel": channel,
        "stem": stem,
        "steps": materialized_steps,
    }
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote DOM materialization: {out_json} ({len(materialized_steps)} steps with locators)")

    raw = steps_py.read_text(encoding="utf-8")
    if "@scenario(" not in raw:
        raise SystemExit("Unexpected step file format (missing @scenario)")

    if not re.search(r"def step_\w+\(\)\s*->\s*None:", raw):
        print(f"Step file already wired (no stub steps); skipping patch: {steps_py}")
    else:
        new_raw = _patch_step_file(raw, channel, stem)
        if new_raw != raw:
            bak = steps_py.with_suffix(".py.bak")
            bak.write_text(raw, encoding="utf-8")
            steps_py.write_text(new_raw, encoding="utf-8")
            print(f"Patched: {steps_py} (backup: {bak})")
        else:
            print(f"No step text changes: {steps_py}")

    first_lines = "\n".join(feat.read_text(encoding="utf-8").splitlines()[:3])
    if "@web" not in first_lines:
        fcontent = feat.read_text(encoding="utf-8")
        feat.write_text("@web\n" + fcontent, encoding="utf-8")
        print(f"Prepended @web tag to: {feat}")


def main() -> None:
    p = argparse.ArgumentParser(description="DOM-scan and materialize BDD steps after manual→BDD generation")
    p.add_argument("-c", "--channel", required=True, choices=["Netbanking", "MobileBanking", "API", "CrossChannel"])
    p.add_argument("-p", "--stem", required=True, help="File stem, e.g. nb_homefinance_emicalc_manual")
    p.add_argument("--base-url", required=True, help="Primary URL to load for DOM scan")
    p.add_argument("--secondary-url", default=None, help="Optional second URL (e.g. EMI calculator page)")
    p.add_argument("--browser", default="chrome")
    p.add_argument("--headed", action="store_true", help="Run browser headed (HEADLESS=0)")
    p.add_argument("--min-score", type=float, default=0.22, help="Minimum DOM match score (0-1)")
    p.add_argument(
        "--patch-only",
        action="store_true",
        help="Skip Selenium scan; keep or initialize steps from existing JSON, still patch stubs",
    )
    p.add_argument("--framework-root", type=Path, default=None)
    args = p.parse_args()

    fw = args.framework_root or Path(__file__).resolve().parents[2]

    run(
        fw,
        args.channel,
        args.stem,
        args.base_url,
        args.secondary_url,
        args.browser,
        headless=not args.headed,
        min_score=args.min_score,
        patch_only=args.patch_only,
    )


if __name__ == "__main__":
    main()
