"""API contract for this feature — paths and payloads live in api_my_feature_api_materialized.json (materialize with api_bdd_materialize)."""

from __future__ import annotations


class ApiMyFeaturePage:
    """
    Logical endpoint keys match api_bdd_step_runner + api_my_feature_api_materialized.json.
    Override paths/payloads via: python -m common.utils.api_bdd_materialize ... --config overrides.json
    """

    ENDPOINT_KEYS: tuple[str, ...] = ("lead_save", "lead_status", "health")
    PAYLOAD_KEYS: tuple[str, ...] = ("valid_lead", "invalid_lead", "duplicate_lead")

    @staticmethod
    def materialized_path_hint() -> str:
        return f"API/pageobject/nm/api_my_feature_api_materialized.json"
