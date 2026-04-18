"""DOM scan + locator suggestion when a selector fails (self-healing)."""

from __future__ import annotations

import json
import os
import re
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Any

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

# Disable healing entirely
SELF_HEAL_ENABLED = os.environ.get("SELF_HEAL", "1").strip() not in ("0", "false", "no")


@dataclass
class ElementCandidate:
    by: str
    selector: str
    score: float
    tag: str
    snippet: str


def _similarity(a: str, b: str) -> float:
    a, b = (a or "").lower().strip(), (b or "").lower().strip()
    if not a or not b:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def _visible_text(el: WebElement, max_len: int = 120) -> str:
    try:
        t = el.text or ""
        if not t.strip():
            t = el.get_attribute("value") or el.get_attribute("aria-label") or ""
        return t.strip()[:max_len]
    except Exception:
        return ""


def _attrs_blob(el: WebElement) -> str:
    parts = []
    for attr in ("id", "name", "class", "aria-label", "placeholder", "title", "data-testid", "role"):
        try:
            v = el.get_attribute(attr)
            if v:
                parts.append(v)
        except Exception:
            pass
    return " ".join(parts)


def _xpath_by_id(eid: str) -> str | None:
    eid = eid.strip()
    if eid and not re.search(r"['\[\]]", eid):
        return f'//*[@id="{eid}"]'
    return None


def build_candidate_locators(el: WebElement) -> list[tuple[str, str]]:
    """Produce several (by, selector) options for an element."""
    out: list[tuple[str, str]] = []
    try:
        eid = el.get_attribute("id")
        if eid:
            xp = _xpath_by_id(eid)
            if xp:
                out.append((By.XPATH, xp))
            out.append((By.ID, eid))
    except Exception:
        pass
    try:
        tid = el.get_attribute("data-testid")
        if tid:
            out.append((By.CSS_SELECTOR, f'[data-testid="{tid}"]'))
    except Exception:
        pass
    try:
        name = el.get_attribute("name")
        if name:
            out.append((By.CSS_SELECTOR, f'[name="{name}"]'))
    except Exception:
        pass
    tag = el.tag_name.lower()
    txt = _visible_text(el, 200)
    if txt and len(txt) > 2 and "'" not in txt[:80]:
        out.append((By.XPATH, f"//{tag}[contains(normalize-space(.), '{txt[:80]}')]"))
    try:
        cls = el.get_attribute("class")
        if cls and " " not in cls[:40]:
            out.append((By.CSS_SELECTOR, f"{tag}.{cls.split()[0]}"))
    except Exception:
        pass
    return out


def scan_interactive_elements(driver: WebDriver, limit: int = 250) -> list[WebElement]:
    """Collect likely interactive / label elements for scoring."""
    sel = (
        "a, button, input, select, textarea, h1, h2, h3, h4, "
        '[role="button"], [role="tab"], label, span, div[data-testid]'
    )
    try:
        nodes = driver.find_elements(By.CSS_SELECTOR, sel)
    except Exception:
        return []
    out: list[WebElement] = []
    for el in nodes:
        try:
            if not el.is_displayed():
                continue
            out.append(el)
            if len(out) >= limit:
                break
        except Exception:
            continue
    return out


def score_element_for_hints(el: WebElement, hints: list[str]) -> float:
    blob = _visible_text(el) + " " + _attrs_blob(el)
    best = 0.0
    for h in hints:
        if not h:
            continue
        best = max(best, _similarity(blob, h))
        for word in h.split():
            if len(word) > 3:
                best = max(best, _similarity(blob, word))
    return best


def suggest_locator_from_dom(
    driver: WebDriver,
    hints: list[str],
    min_score: float = 0.28,
    previous_selector: str | None = None,
) -> tuple[str, str] | None:
    """
    Scan visible DOM, score elements against hints, return best new (By, selector).
    `hints` should include visible label text, aria labels, etc.
    """
    if not SELF_HEAL_ENABLED:
        return None
    hints = [h for h in hints if h]
    if not hints:
        return None

    elements = scan_interactive_elements(driver)
    best: tuple[WebElement, float] | None = None
    for el in elements:
        try:
            sc = score_element_for_hints(el, hints)
            if best is None or sc > best[1]:
                best = (el, sc)
        except Exception:
            continue

    if not best or best[1] < min_score:
        return None

    el, score = best
    candidates = build_candidate_locators(el)
    # Deprioritize same broken selector
    for by, sel in candidates:
        if previous_selector and sel == previous_selector:
            continue
        try:
            found = driver.find_elements(by, sel)
            if found and found[0].is_displayed():
                return (by, sel)
        except Exception:
            continue
    for by, sel in candidates:
        try:
            found = driver.find_elements(by, sel)
            if found and found[0].is_displayed():
                return (by, sel)
        except Exception:
            continue
    return None


def heal_locator(
    driver: WebDriver,
    hints: list[str],
    old_by: str,
    old_selector: str,
) -> tuple[str, str] | None:
    """Try to find a working locator; returns None if healing failed."""
    return suggest_locator_from_dom(driver, hints, previous_selector=old_selector)
