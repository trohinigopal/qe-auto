"""Load BDD step fixtures from shared step_defs (pytest only collects fixtures from conftest/test modules)."""

pytest_plugins = ("API.stepdefination.nm.api_my_feature_step_defs",)
