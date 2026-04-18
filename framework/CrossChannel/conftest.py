"""
Cross-channel tests reuse BDD step definitions from Netbanking and API packages.

`pytest_plugins` ensures step implementations are registered when only CrossChannel tests
are collected (so the scenario module does not need to duplicate @given/@when/@then).
"""

from __future__ import annotations

pytest_plugins = (
    "Netbanking.stepdefination.nm.nb_homefinance_emicalc_manual_step_defs",
    "API.stepdefination.nm.api_my_feature_step_defs",
)
