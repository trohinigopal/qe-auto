"""
Convert a user story markdown file to manual functional test cases.

Run from framework directory:
  python -m common.utils.user_story_to_manual -i UserStories/en/foo.md -o ManualTestCases/en/nm_foo_manual.md
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from common.utils.user_story_parser import UserStoryDoc, parse_user_story_markdown, tc_prefix_from_story_id


def _is_api_story(doc: UserStoryDoc) -> bool:
    """Detect API/integration stories; avoid matching 'api' inside unrelated words."""
    blob = f"{doc.epic} {doc.feature} {doc.title} {' '.join(doc.acceptance_criteria)}"
    bl = blob.lower()
    if re.search(r"\bapi\b", bl):
        return True
    return bool(
        re.search(r"\b(json|rest|graphql|oauth|endpoint|payload|grpc)\b", bl)
        or "crm lead" in bl
        or "lead status" in bl
        or "http 2xx" in bl
        or "4xx" in bl
    )


def _short_title(criterion: str, max_len: int = 70) -> str:
    t = re.sub(r"\*\*", "", criterion)
    t = re.sub(r"\s+", " ", t).strip()
    if len(t) <= max_len:
        return t
    return t[: max_len - 3] + "..."


def _steps_for_criterion(doc: UserStoryDoc, criterion: str, index: int, api: bool) -> tuple[list[str], list[str]]:
    """Return (steps, expected) lists."""
    crit_lower = criterion.lower()
    if api:
        steps = [
            "Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.",
            f"Execute the scenario for acceptance criterion {index + 1}: align request body/path with published schema.",
            "Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).",
        ]
        expected = [
            "Observed behaviour matches the acceptance criterion text.",
            "Errors return structured response as per contract when validation fails.",
        ]
        if "2xx" in crit_lower or "success" in crit_lower:
            expected.insert(0, "Response status is in 2xx family for valid requests as documented.")
        if "4xx" in crit_lower or "invalid" in crit_lower:
            expected.insert(0, "Invalid inputs yield 4xx with parseable error payload.")
        if "https" in crit_lower:
            expected.append("Transport is HTTPS only.")
        if "status" in crit_lower or "query" in crit_lower or "inquiry" in crit_lower:
            steps.insert(1, "Invoke status/query API with documented identifiers (mobile, lead id, etc.).")
        return steps, expected

    # UI / journey
    steps = [
        "Open the application under test (correct environment URL).",
        f"Perform actions to satisfy: {_short_title(criterion, 100)}",
        "Observe UI state, labels, and any server responses visible to the user.",
    ]
    if "calculator" in crit_lower or "emi" in crit_lower:
        steps = [
            "Navigate to the relevant calculator or screen described in the user story.",
            "Adjust inputs (loan amount, tenure, rate, etc.) as applicable to this criterion.",
            "Observe displayed results, disclaimers, and navigation options.",
        ]
    expected = [
        "UI matches the acceptance criterion (visible elements, values, or messages).",
        "No unhandled error pages (5xx) for healthy environments.",
    ]
    if "disclaimer" in crit_lower:
        expected.append("Disclaimer text is visible and readable.")
    if "amortization" in crit_lower or "view details" in crit_lower:
        expected.append("Detail or schedule view opens without forcing unrelated flows.")
    return steps, expected


def build_manual_markdown(
    doc: UserStoryDoc,
    source_rel_path: str,
    app_under_test: str | None,
) -> str:
    api = _is_api_story(doc)
    prefix = tc_prefix_from_story_id(doc.story_id or "US-GEN")
    env = (
        "API — SIT/UAT base URL from developer portal / internal config (never commit secrets)."
        if api
        else "Web — latest Chrome / Edge / Safari (mobile + desktop where applicable)."
    )
    if app_under_test:
        env_line = app_under_test
    else:
        blob = f"{doc.source_note} {doc.background}"
        urls = re.findall(r"https://[^\s\)`\"]+", blob)
        env_line = urls[0] if urls else "See user story source section for environment URLs."

    lines: list[str] = [
        f"# Functional manual test cases — {doc.feature or doc.title}",
        "",
        f"**Traces to user story:** `{doc.story_id}` (`{source_rel_path}`)",
        f"**Suggested test environment:** {env}",
        f"**Application / system under test:** {env_line}",
        "",
        f"**User story summary:** As a {doc.as_a[:120]}… — I want to {doc.i_want[:200]}…",
        "",
        "---",
        "",
    ]

    for i, criterion in enumerate(doc.acceptance_criteria):
        tc_num = f"{prefix}-{i + 1:03d}"
        title = _short_title(criterion, 85)
        steps, expected = _steps_for_criterion(doc, criterion, i, api)

        lines.extend(
            [
                f"## {tc_num} — {title}",
                "",
                "| Field | Details |",
                "|--------|---------|",
                f"| **Objective** | Verify: {_short_title(criterion, 400)} |",
                "| **Priority** | High |",
                "| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |",
                "",
                "**Steps**",
                "",
            ]
        )
        for j, st in enumerate(steps, 1):
            lines.append(f"{j}. {st}")
        lines.append("")
        lines.append("**Expected results**")
        lines.append("")
        for j, ex in enumerate(expected, 1):
            lines.append(f"{j}. {ex}")
        lines.append("")
        lines.append("**Pass / Fail** | **Tester** | **Date** | **Notes**")
        lines.append("")
        lines.append("---")
        lines.append("")

    if doc.non_functional:
        lines.append("## Non-functional checks (from user story)")
        lines.append("")
        for nf in doc.non_functional:
            lines.append(f"- {nf}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def run(input_path: Path, output_path: Path, app_under_test: str | None) -> None:
    text = input_path.read_text(encoding="utf-8")
    doc = parse_user_story_markdown(text)
    if not doc.acceptance_criteria:
        raise SystemExit(
            "No acceptance criteria found. Expected '## Acceptance criteria' with numbered lines (1. ...)."
        )
    rel = input_path.as_posix()
    if "UserStories" in rel:
        rel = rel[rel.index("UserStories") :]
    else:
        rel = input_path.name

    out = build_manual_markdown(doc, rel, app_under_test)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(out, encoding="utf-8")
    print(f"Wrote: {output_path}")


def main() -> None:
    p = argparse.ArgumentParser(description="Convert user story markdown to manual testcase markdown")
    p.add_argument(
        "--input",
        "-i",
        required=True,
        type=Path,
        help="Path to user story .md (e.g. UserStories/en/nm_foo.md)",
    )
    p.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Output manual testcase path (default: ManualTestCases/en/<stem>_manual.md)",
    )
    p.add_argument(
        "--app",
        type=str,
        default=None,
        help='Override "Application under test" one-liner',
    )
    p.add_argument(
        "--framework-root",
        type=Path,
        default=None,
        help="Framework root (default: parent of common/)",
    )
    args = p.parse_args()

    fw = args.framework_root or Path(__file__).resolve().parents[2]
    inp = args.input.resolve()
    if not inp.is_file():
        raise SystemExit(f"Input not found: {inp}")

    if args.output:
        out = args.output.resolve()
    else:
        stem = inp.stem
        out = fw / "ManualTestCases" / "en" / f"{stem}_manual.md"

    run(inp, out, args.app)


if __name__ == "__main__":
    main()
