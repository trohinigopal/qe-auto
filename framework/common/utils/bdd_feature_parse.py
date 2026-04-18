"""Extract Gherkin step texts from a .feature file."""

from __future__ import annotations

import re
from pathlib import Path


def normalize_step_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def extract_step_texts_from_feature(feature_path: Path) -> list[str]:
    content = feature_path.read_text(encoding="utf-8")
    texts: list[str] = []
    seen: set[str] = set()
    for line in content.splitlines():
        raw = line.strip()
        if not raw.startswith("#") and re.match(
            r"^(Given|When|Then|And)\s+",
            raw,
            re.IGNORECASE,
        ):
            rest = re.sub(r"^(Given|When|Then|And)\s+", "", raw, flags=re.IGNORECASE).strip()
            if not rest:
                continue
            key = normalize_step_text(rest)
            if key not in seen:
                seen.add(key)
                texts.append(key)
    return texts
