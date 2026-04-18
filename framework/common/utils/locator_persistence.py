"""Persist healed locators to JSON next to the page object module."""

from __future__ import annotations

import json
import logging
import threading
from pathlib import Path

_logger = logging.getLogger("framework.self_heal")
_lock = threading.Lock()
_last_heal_updated = False


def locator_json_path(page_object_file: Path) -> Path:
    return page_object_file.parent / f"{page_object_file.stem}_locators.json"


def load_overrides(page_object_file: Path) -> dict[str, list[str]]:
    """Load { key: ['xpath', '//...'] } as [by_name, selector]."""
    path = locator_json_path(page_object_file)
    if not path.is_file():
        return {}
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    out: dict[str, list[str]] = {}
    for k, v in raw.items():
        if isinstance(v, list) and len(v) == 2:
            out[k] = [str(v[0]), str(v[1])]
    return out


def save_override(page_object_file: Path, key: str, by_name: str, selector: str) -> None:
    global _last_heal_updated
    path = locator_json_path(page_object_file)
    with _lock:
        data = {}
        if path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                data = {}
        data[key] = [by_name, selector]
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        _last_heal_updated = True
        _logger.warning("Self-heal persisted locator %r → %s / %s", key, by_name, path)


def merge_with_class_defaults(
    defaults: dict[str, tuple[str, str]],
    page_object_file: Path,
) -> dict[str, tuple[str, str]]:
    from selenium.webdriver.common.by import By

    by_name_map = {
        "xpath": By.XPATH,
        "css selector": By.CSS_SELECTOR,
        "id": By.ID,
        "name": By.NAME,
        "link text": By.LINK_TEXT,
        "partial link text": By.PARTIAL_LINK_TEXT,
        "tag name": By.TAG_NAME,
        "class name": By.CLASS_NAME,
    }
    merged = dict(defaults)
    overrides = load_overrides(page_object_file)
    for key, pair in overrides.items():
        by_n, sel = pair[0].lower(), pair[1]
        by_const = by_name_map.get(by_n, By.XPATH)
        merged[key] = (by_const, sel)
    return merged


def consume_heal_happened() -> bool:
    """Return True once if any locator was healed this session (for logging/rerun hints)."""
    global _last_heal_updated
    with _lock:
        v = _last_heal_updated
        _last_heal_updated = False
        return v


def heal_flag_set() -> bool:
    with _lock:
        return _last_heal_updated
