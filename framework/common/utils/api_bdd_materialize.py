"""
After manual_tc_to_bdd for API channel, write contract JSON (base URL, paths, payloads) and
patch step definitions to call api_bdd_step_runner.execute_api_materialized_step.

Usage (from framework directory):
  python -m common.utils.api_bdd_materialize -c API -p api_my_feature \\
    --api-base-url https://sandbox-api.example.bank.in \\
    --config path/to/contract_overrides.json

Optional env for auth placeholders in JSON: API_KEY, API_TOKEN, etc.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from common.utils.bdd_dom_materialize import extract_step_strings_from_steps_py


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


def _stem_to_page_class(stem: str) -> str:
    return "".join(part.capitalize() for part in stem.split("_")) + "Page"


def _default_materialized(
    api_base_url: str,
    channel: str,
    stem: str,
    overrides: dict | None,
) -> dict:
    base: dict = {
        "api_base_url": api_base_url.rstrip("/"),
        "channel": channel,
        "stem": stem,
        "default_headers": {
            "Content-Type": "application/json",
            "Authorization": "Bearer ${API_TOKEN}",
        },
        "endpoints": {
            "lead_save": {
                "method": "POST",
                "path": "crm-lead/v1/save",
                "headers": {},
            },
            "lead_save_4xx": {
                "method": "POST",
                "path": "crm-lead/v1/save",
                "headers": {},
            },
            "lead_status": {
                "method": "GET",
                "path": "crm-lead/v1/status",
                "headers": {},
            },
            "health": {"method": "GET", "path": "/", "headers": {}},
        },
        "payloads": {
            "valid_lead": {
                "product": "HOME_LOAN",
                "mobile": "9876543210",
                "consent": True,
                "source": "QE_AUTO",
            },
            "invalid_lead": {
                "product": "HOME_LOAN",
            },
            "duplicate_lead": {
                "product": "HOME_LOAN",
                "mobile": "9876543210",
                "consent": True,
                "source": "QE_AUTO",
            },
        },
        "query_params": {
            "lead_status": {"mobile": "9876543210"},
        },
    }
    if overrides:
        _deep_merge(base, overrides)
    return base


def _deep_merge(dst: dict, src: dict) -> None:
    for k, v in src.items():
        if k in dst and isinstance(dst[k], dict) and isinstance(v, dict):
            _deep_merge(dst[k], v)
        else:
            dst[k] = v


def _patch_api_step_file(content: str, channel: str, stem: str) -> str:
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
            f"def {func_name}(api_client):\n"
            f"    if api_client is None:\n"
            f"        import pytest\n"
            f"        pytest.skip('API client required for this step')\n"
            f"    from common.utils.api_bdd_step_runner import execute_api_materialized_step\n"
            f"    execute_api_materialized_step(api_client, {rep}, {fw_name}, _MAT_CHANNEL, _MAT_STEM)\n"
        )

    new_content, n = pattern.subn(repl, content)
    if n == 0:
        raise RuntimeError(
            "No stub steps matched. Expected @given/@when/@then with parsers.parse and body `pass`."
        )
    return new_content


def _ensure_api_tag_on_feature(feat: Path) -> None:
    lines = feat.read_text(encoding="utf-8").splitlines()
    if not lines:
        return
    parts = lines[0].split()
    out: list[str] = []
    seen_api = False
    for p in parts:
        if p == "@web":
            continue
        if p == "@api":
            seen_api = True
        out.append(p)
    if not seen_api:
        out.insert(0, "@api")
    lines[0] = " ".join(out)
    feat.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run(
    framework_root: Path,
    channel: str,
    stem: str,
    api_base_url: str,
    config_path: Path | None,
) -> None:
    stem = stem.lower().replace("-", "_")
    feat = framework_root / channel / "Features" / "nm" / f"{stem}.feature"
    steps_py = framework_root / channel / "stepdefination" / "nm" / f"test_{stem}_steps.py"
    out_json = framework_root / channel / "pageobject" / "nm" / f"{stem}_api_materialized.json"
    page_py = framework_root / channel / "pageobject" / "nm" / f"{stem}_page.py"

    if not feat.is_file():
        raise SystemExit(f"Feature not found: {feat}")
    if not steps_py.is_file():
        raise SystemExit(f"Step file not found: {steps_py}")

    overrides: dict | None = None
    if config_path and config_path.is_file():
        overrides = json.loads(config_path.read_text(encoding="utf-8"))

    payload = _default_materialized(api_base_url, channel, stem, overrides)
    out_json.parent.mkdir(parents=True, exist_ok=True)
    out_json.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote API materialization: {out_json}")

    if page_py.is_file():
        page_py.write_text(_page_object_content(stem, _stem_to_page_class(stem)), encoding="utf-8")
        print(f"Updated page object: {page_py}")

    raw = steps_py.read_text(encoding="utf-8")
    if not re.search(r"def step_\w+\(\)\s*->\s*None:", raw):
        print(f"Step file already wired; skipping patch: {steps_py}")
    else:
        new_raw = _patch_api_step_file(raw, channel, stem)
        if new_raw != raw:
            bak = steps_py.with_suffix(".py.bak")
            bak.write_text(raw, encoding="utf-8")
            steps_py.write_text(new_raw, encoding="utf-8")
            print(f"Patched: {steps_py} (backup: {bak})")

    _ensure_api_tag_on_feature(feat)
    print(f"Tagged feature with @api: {feat}")


def _page_object_content(stem: str, class_name: str) -> str:
    json_name = f"{stem}_api_materialized.json"
    return f'''"""API contract for this feature — paths and payloads live in {json_name} (materialize with api_bdd_materialize)."""

from __future__ import annotations


class {class_name}:
    """
    Logical endpoint keys match api_bdd_step_runner + {json_name}.
    Override paths/payloads via: python -m common.utils.api_bdd_materialize ... --config overrides.json
    """

    ENDPOINT_KEYS: tuple[str, ...] = ("lead_save", "lead_status", "health")
    PAYLOAD_KEYS: tuple[str, ...] = ("valid_lead", "invalid_lead", "duplicate_lead")

    @staticmethod
    def materialized_path_hint() -> str:
        return f"API/pageobject/nm/{json_name}"
'''


def main() -> None:
    p = argparse.ArgumentParser(description="Materialize API BDD contract JSON and patch step definitions")
    p.add_argument("-c", "--channel", default="API", choices=["Netbanking", "MobileBanking", "API", "CrossChannel"])
    p.add_argument("-p", "--stem", required=True, help="File stem, e.g. api_my_feature")
    p.add_argument("--api-base-url", required=True, help="Sandbox or SIT base URL (no trailing slash required)")
    p.add_argument("--config", type=Path, default=None, help="Optional JSON merged into materialized contract")
    p.add_argument("--framework-root", type=Path, default=None)
    args = p.parse_args()

    fw = args.framework_root or Path(__file__).resolve().parents[2]
    run(fw, args.channel, args.stem, args.api_base_url, args.config)


if __name__ == "__main__":
    main()
