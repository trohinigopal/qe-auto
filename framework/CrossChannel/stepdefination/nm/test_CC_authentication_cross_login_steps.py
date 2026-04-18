"""
Cross-channel scenario only — steps come from Netbanking + API step_defs (see CrossChannel/conftest.py).
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_FW = Path(__file__).resolve().parents[3]
if str(_FW) not in sys.path:
    sys.path.insert(0, str(_FW))

from pytest_bdd import scenario

pytestmark = pytest.mark.cross


@scenario("../../Features/nm/CC_authentication_cross_login.feature", "Navigate to monthly EMI calculator and check api")
def test_cross_channel_emi_then_api_lead() -> None:
    """Reuse materialized Netbanking DOM steps + API contract steps in one journey."""
    pass
