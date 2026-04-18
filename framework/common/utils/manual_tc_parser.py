"""Parse manual testcase markdown (framework ManualTestCases format)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class ManualTestCase:
    tc_id: str
    title: str
    objective: str
    priority: str
    preconditions: str
    steps: list[str] = field(default_factory=list)
    expected: list[str] = field(default_factory=list)


TC_HEADER_RE = re.compile(r"^##\s+(TC-[A-Z0-9-]+)\s*[—\-]\s*(.+?)\s*$", re.MULTILINE)
TABLE_OBJECTIVE_RE = re.compile(
    r"\|\s*\*\*Objective\*\*\s*\|\s*(.+?)\s*\|", re.MULTILINE | re.DOTALL
)
TABLE_PRIORITY_RE = re.compile(r"\|\s*\*\*Priority\*\*\s*\|\s*(\w+)\s*\|", re.MULTILINE)
TABLE_PRECOND_RE = re.compile(
    r"\|\s*\*\*Preconditions\*\*\s*\|\s*(.+?)\s*\|", re.MULTILINE | re.DOTALL
)
NUMBERED_LINE_RE = re.compile(r"^\s*(\d+)\.\s+(.+?)\s*$")


def _clean_cell(text: str) -> str:
    t = text.strip()
    t = re.sub(r"\s+", " ", t)
    return t


def parse_manual_markdown(content: str) -> list[ManualTestCase]:
    """Split document into manual test cases."""
    blocks = re.split(r"\n---\s*\n", content)
    cases: list[ManualTestCase] = []

    for block in blocks:
        block = block.strip()
        if not block.startswith("## TC-"):
            continue
        m = TC_HEADER_RE.search(block)
        if not m:
            continue
        tc_id, title = m.group(1), _clean_cell(m.group(2))

        obj_m = TABLE_OBJECTIVE_RE.search(block)
        objective = _clean_cell(obj_m.group(1)) if obj_m else ""

        pri_m = TABLE_PRIORITY_RE.search(block)
        priority = pri_m.group(1) if pri_m else ""

        pre_m = TABLE_PRECOND_RE.search(block)
        preconditions = _clean_cell(pre_m.group(1)) if pre_m else ""

        steps = _extract_numbered_section(block, "**Steps**", "**Expected results**")
        expected = _extract_numbered_section(block, "**Expected results**", "**Pass")

        cases.append(
            ManualTestCase(
                tc_id=tc_id,
                title=title,
                objective=objective,
                priority=priority,
                preconditions=preconditions,
                steps=steps,
                expected=expected,
            )
        )
    return cases


def _extract_numbered_section(block: str, start_marker: str, end_marker: str) -> list[str]:
    try:
        start = block.index(start_marker) + len(start_marker)
        end = block.index(end_marker, start)
    except ValueError:
        return []
    section = block[start:end]
    lines: list[str] = []
    for line in section.splitlines():
        nm = NUMBERED_LINE_RE.match(line)
        if nm:
            lines.append(_clean_step_text(nm.group(2)))
    return lines


def _clean_step_text(text: str) -> str:
    """Strip markdown bold ** and normalize quotes for Gherkin."""
    t = text.strip()
    t = re.sub(r"\*\*(.+?)\*\*", r"\1", t)
    t = re.sub(r"\s+", " ", t)
    return t


def extract_locator_candidates(steps: list[str], expected: list[str]) -> list[str]:
    """Pull quoted phrases and bold-like tokens as UI labels for placeholder locators."""
    texts = " ".join(steps + expected)
    quoted = re.findall(r"[\"“]([^\"”]+)[\"”]", texts)
    # Dedupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for q in quoted:
        q = q.strip()
        if len(q) > 2 and q not in seen:
            seen.add(q)
            out.append(q)
    return out[:40]
