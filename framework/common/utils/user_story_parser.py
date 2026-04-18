"""Parse user story markdown (UserStories/en format)."""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class UserStoryDoc:
    title: str
    story_id: str
    epic: str
    feature: str
    source_note: str
    as_a: str
    i_want: str
    so_that: str
    background: str
    acceptance_criteria: list[str] = field(default_factory=list)
    non_functional: list[str] = field(default_factory=list)
    raw_header_lines: list[str] = field(default_factory=list)


def _clean_line(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip())


def parse_user_story_markdown(content: str) -> UserStoryDoc:
    lines = content.splitlines()
    title = ""
    story_id = ""
    epic = ""
    feature = ""
    source_note = ""
    as_a, i_want, so_that = "", "", ""
    background = ""
    acceptance: list[str] = []
    non_functional: list[str] = []
    header_accum: list[str] = []

    if lines and lines[0].startswith("#"):
        title = lines[0].lstrip("#").strip()

    in_story = False
    in_background = False
    in_ac = False
    in_nf = False
    story_lines: list[str] = []

    for i, line in enumerate(lines):
        if line.startswith("**ID:**"):
            m = re.search(r"\*\*ID:\*\*\s*(.+)", line)
            if m:
                story_id = _clean_line(m.group(1))
        elif line.startswith("**Epic:**"):
            m = re.search(r"\*\*Epic:\*\*\s*(.+)", line)
            if m:
                epic = _clean_line(m.group(1))
        elif line.startswith("**Feature:**"):
            m = re.search(r"\*\*Feature:\*\*\s*(.+)", line)
            if m:
                feature = _clean_line(m.group(1))
        elif line.startswith("**Source") or line.startswith("**Sources"):
            header_accum.append(line)
        elif line.strip().startswith("**Note:**"):
            header_accum.append(line)

        if line.strip() == "## Story":
            in_story = True
            in_background = in_ac = in_nf = False
            continue
        if line.strip() == "## Background":
            in_story = False
            in_background = True
            in_ac = in_nf = False
            continue
        if line.strip() == "## Acceptance criteria":
            in_story = in_background = False
            in_ac = True
            in_nf = False
            continue
        if line.strip() == "## Non-functional":
            in_ac = in_story = in_background = False
            in_nf = True
            continue
        if line.startswith("## ") and line.strip() not in (
            "## Story",
            "## Background",
            "## Acceptance criteria",
            "## Non-functional",
        ):
            if line.strip().startswith("## Out of scope"):
                in_ac = in_nf = in_story = in_background = False
            elif in_nf:
                in_nf = False

        if in_story:
            story_lines.append(line)
        elif in_background:
            if line.strip() and not line.startswith("##"):
                background += line.strip() + " "
        elif in_ac:
            m = re.match(r"^\s*(\d+)\.\s+(.+)$", line)
            if m:
                acceptance.append(_clean_line(m.group(2)))
        elif in_nf:
            if line.strip().startswith("-"):
                non_functional.append(_clean_line(line.lstrip("-").strip()))

    # Parse As a / I want / So that from story_lines
    blob = "\n".join(story_lines)
    ma = re.search(r"\*\*As a\*\*\s+(.+?)(?=\*\*I want|\Z)", blob, re.DOTALL | re.IGNORECASE)
    mw = re.search(r"\*\*I want to\*\*\s+(.+?)(?=\*\*So that|\Z)", blob, re.DOTALL | re.IGNORECASE)
    ms = re.search(r"\*\*So that\*\*\s+(.+?)(?=\n##|\Z)", blob, re.DOTALL | re.IGNORECASE)
    if ma:
        as_a = _clean_line(ma.group(1))
    if mw:
        i_want = _clean_line(mw.group(1))
    if ms:
        so_that = _clean_line(ms.group(1))

    source_note = _clean_line(" ".join(header_accum)) if header_accum else ""

    return UserStoryDoc(
        title=title,
        story_id=story_id,
        epic=epic,
        feature=feature,
        source_note=source_note,
        as_a=as_a,
        i_want=i_want,
        so_that=so_that,
        background=_clean_line(background),
        acceptance_criteria=acceptance,
        non_functional=non_functional,
        raw_header_lines=header_accum,
    )


def tc_prefix_from_story_id(story_id: str) -> str:
    """US-HL-CALC-001 -> TC-HL-CALC"""
    s = story_id.strip()
    if s.upper().startswith("US-"):
        s = s[3:]
    # drop trailing -001 numeric suffix for series
    s = re.sub(r"-\d+\s*$", "", s)
    return f"TC-{s}" if s else "TC-GEN"
