from __future__ import annotations

from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Iterable

# Re-export DOM-based healing (preferred)
from common.utils.dom_self_heal import heal_locator as heal_locator_from_dom  # noqa: F401


@dataclass
class CandidateLocator:
    locator: str
    score: float


def find_best_locator(broken_locator: str, candidate_locators: Iterable[str]) -> CandidateLocator | None:
    ranked = [
        CandidateLocator(locator=c, score=SequenceMatcher(None, broken_locator, c).ratio())
        for c in candidate_locators
    ]
    ranked.sort(key=lambda x: x.score, reverse=True)
    return ranked[0] if ranked and ranked[0].score >= 0.65 else None
