"""
Convert a manual testcase markdown file into:
- Gherkin feature (Features/nm/<stem>.feature)
- Page object with placeholder locators (pageobject/nm/<stem>_page.py)
- Step definitions (stepdefination/nm/test_<stem>_steps.py)

Run from the framework directory:
  python -m common.utils.manual_tc_to_bdd -i ManualTestCases/en/foo.md -c Netbanking -p NB_homefinance_foo

Next (optional): scan DOM and wire steps — python -m common.utils.bdd_dom_materialize -c <channel> -p <stem> --base-url ...
API channel: materialize REST contract — python -m common.utils.api_bdd_materialize -c API -p <stem> --api-base-url ...
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from common.utils.manual_tc_parser import ManualTestCase, extract_locator_candidates, parse_manual_markdown

STEP_MAX_LEN = 400


def _slug_key(label: str) -> str:
    s = re.sub(r"[^a-zA-Z0-9]+", "_", label.lower()).strip("_")
    return s[:60] or "element"


def _shorten(s: str, max_len: int = STEP_MAX_LEN) -> str:
    s = re.sub(r"\s+", " ", s.strip())
    return s if len(s) <= max_len else s[: max_len - 3] + "..."


def _escape_parse_pattern(s: str) -> str:
    """Brace-escape for pytest_bdd parsers.parse (literal { } in manual text)."""
    return s.replace("\\", "\\\\").replace('"', '\\"').replace("{", "{{").replace("}", "}}")


def _scenario_lines(tc: ManualTestCase) -> list[str]:
    """Build Gherkin lines using the same canonical strings as registered step definitions."""
    lines: list[str] = []

    if tc.preconditions:
        lines.append(f"    Given {_shorten(tc.preconditions)}")
    else:
        lines.append("    Given the manual testcase preconditions are satisfied")

    if not tc.steps:
        lines.append("    When no steps were recorded in the manual testcase")
    else:
        lines.append(f"    When {_shorten(tc.steps[0])}")
        for s in tc.steps[1:]:
            lines.append(f"    And {_shorten(s)}")

    if not tc.expected:
        lines.append("    Then the outcome matches the manual expected results")
    else:
        lines.append(f"    Then {_shorten(tc.expected[0])}")
        for e in tc.expected[1:]:
            lines.append(f"    And {_shorten(e)}")
    return lines


def build_feature_content(
    cases: list[ManualTestCase],
    feature_title: str,
    tags: list[str],
) -> str:
    tag_line = " ".join(f"@{t}" for t in tags)
    parts = [f"{tag_line}", f"Feature: {feature_title}", ""]
    for tc in cases:
        scen_name = _shorten(f"{tc.tc_id} {tc.title}", 120)
        parts.append(f"  Scenario: {scen_name}")
        parts.extend(_scenario_lines(tc))
        parts.append("")
    return "\n".join(parts).rstrip() + "\n"


def build_page_object(class_name: str, candidates: list[str]) -> str:
    lines = [
        '"""Auto-generated page object — replace LOCATORS with real selectors from DevTools."""',
        "",
        "from selenium.webdriver.common.by import By",
        "",
        "",
        f"class {class_name}:",
        '    """Placeholder locators extracted from manual testcase wording (quoted phrases)."""',
        "",
        "    LOCATORS: dict[str, tuple[str, str]] = {",
    ]
    for label in candidates:
        key = _slug_key(label)
        safe_comment = label[:80].replace("\n", " ")
        lines.append(f'        "{key}": (By.CSS_SELECTOR, "[data-testid=\\"TODO-{key}\\"]"),  # {safe_comment}')
    if not candidates:
        lines.append('        "page_root": (By.TAG_NAME, "body"),')
    lines.extend(
        [
            "    }",
            "",
            "    def __init__(self, driver) -> None:",
            "        self.driver = driver",
            "",
        ]
    )
    return "\n".join(lines)


def _unique_step_texts(cases: list[ManualTestCase]) -> list[tuple[str, str]]:
    """(kind, text) in order — includes placeholder steps for empty manual rows."""
    seen: set[str] = set()
    ordered: list[tuple[str, str]] = []

    def add(kind: str, text: str) -> None:
        t = _shorten(text, STEP_MAX_LEN)
        if t in seen:
            return
        seen.add(t)
        ordered.append((kind, t))

    for tc in cases:
        if tc.preconditions:
            add("given", tc.preconditions)
        else:
            add("given", "the manual testcase preconditions are satisfied")

        if tc.steps:
            for s in tc.steps:
                add("when", s)
        else:
            add("when", "no steps were recorded in the manual testcase")

        if tc.expected:
            for e in tc.expected:
                add("then", e)
        else:
            add("then", "the outcome matches the manual expected results")

    return ordered


def build_step_definitions_file(
    feature_filename: str,
    cases: list[ManualTestCase],
    channel: str,
    stem: str,
    class_name: str,
) -> str:
    """Scenario bindings + step stubs; imports page object after sys.path fix."""
    fw_parent_import = (
        "import sys\n"
        "from pathlib import Path\n"
        "_FW = Path(__file__).resolve().parents[3]\n"
        "if str(_FW) not in sys.path:\n"
        "    sys.path.insert(0, str(_FW))\n"
    )
    import_line = f"from {channel}.pageobject.nm.{stem}_page import {class_name}\n"

    scenario_blocks: list[str] = []
    for tc in cases:
        safe_name = re.sub(r"[^a-zA-Z0-9_]", "_", f"test_{tc.tc_id}_{tc.title}")[:120]
        scen_title = _shorten(f"{tc.tc_id} {tc.title}", 120)
        obj = (tc.objective or "").replace('"""', "'")
        scenario_blocks.append(
            f'@scenario("../../Features/nm/{feature_filename}", "{scen_title}")\n'
            f"def {safe_name}() -> None:\n"
            f'    """{obj[:280]}"""\n'
            f"    pass\n"
        )

    step_blocks: list[str] = []
    for kind, text in _unique_step_texts(cases):
        pat = _escape_parse_pattern(text)
        fn = f"step_{_slug_key(text)[:50]}"
        if kind == "given":
            dec = f'@given(parsers.parse("{pat}"))'
        elif kind == "when":
            dec = f'@when(parsers.parse("{pat}"))'
        else:
            dec = f'@then(parsers.parse("{pat}"))'
        step_blocks.append(
            f"{dec}\n"
            f"def {fn}() -> None:\n"
            f"    _ = {class_name}.LOCATORS  # map to Selenium/Appium using driver\n"
            f"    pass\n"
        )

    return (
        '"""Auto-generated from manual testcase — implement body using LOCATORS and driver."""\n\n'
        f"{fw_parent_import}\n"
        "from pytest_bdd import given, parsers, scenario, then, when\n\n"
        f"{import_line}\n"
        + "\n".join(step_blocks)
        + "\n"
        + "\n".join(scenario_blocks)
    )


def run(
    input_path: Path,
    channel: str,
    prefix: str,
    framework_root: Path,
    tags: list[str],
) -> None:
    text = input_path.read_text(encoding="utf-8")
    cases = parse_manual_markdown(text)
    if not cases:
        raise SystemExit(
            f"No test cases parsed from {input_path}. Expected ## TC-... headers and **Steps** / **Expected results** sections."
        )

    loc_candidates = extract_locator_candidates(
        sum([tc.steps for tc in cases], []),
        sum([tc.expected for tc in cases], []),
    )

    stem = prefix.lower().replace("-", "_")
    feature_file = f"{stem}.feature"
    parts = stem.split("_")
    class_name = "".join(p[:1].upper() + p[1:] if p else "" for p in parts) + "Page"
    if not class_name[0].isalpha():
        class_name = "Generated" + class_name

    channel_dir = framework_root / channel
    feat_dir = channel_dir / "Features" / "nm"
    po_dir = channel_dir / "pageobject" / "nm"
    sd_dir = channel_dir / "stepdefination" / "nm"
    feat_dir.mkdir(parents=True, exist_ok=True)
    po_dir.mkdir(parents=True, exist_ok=True)
    sd_dir.mkdir(parents=True, exist_ok=True)

    title = f"Auto-generated from {input_path.name}"
    feature_tags = list(tags) + ["generated"]
    feat_content = build_feature_content(cases, title, feature_tags)
    (feat_dir / feature_file).write_text(feat_content, encoding="utf-8")

    po_content = build_page_object(class_name, loc_candidates)
    (po_dir / f"{stem}_page.py").write_text(po_content, encoding="utf-8")

    sd_content = build_step_definitions_file(feature_file, cases, channel, stem, class_name)
    (sd_dir / f"test_{stem}_steps.py").write_text(sd_content, encoding="utf-8")

    print(f"Wrote:\n  {(feat_dir / feature_file)}\n  {(po_dir / f'{stem}_page.py')}\n  {(sd_dir / f'test_{stem}_steps.py')}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert manual testcase markdown to feature file, page object (locators), and step definitions."
    )
    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=Path,
        help="Path to manual testcase markdown under ManualTestCases/",
    )
    parser.add_argument(
        "--channel",
        "-c",
        default="Netbanking",
        choices=["Netbanking", "MobileBanking", "API", "CrossChannel"],
        help="Target channel folder under framework",
    )
    parser.add_argument(
        "--prefix",
        "-p",
        required=True,
        help="Output file stem, e.g. NB_homefinance_emicalc (nm_epic_feature style)",
    )
    parser.add_argument(
        "--framework-root",
        type=Path,
        default=None,
        help="Path to framework folder (default: parent of common/)",
    )
    parser.add_argument(
        "--tag",
        action="append",
        default=["web"],
        help="Gherkin tag(s); repeat for multiple (default: web)",
    )
    args = parser.parse_args()

    fw = args.framework_root or Path(__file__).resolve().parents[2]
    inp = args.input.resolve()
    if not inp.is_file():
        raise SystemExit(f"Input not found: {inp}")

    run(inp, args.channel, args.prefix, fw, args.tag)


if __name__ == "__main__":
    main()
