"""Load BDD step fixtures from shared step_defs (pytest only collects fixtures from conftest/test modules)."""

pytest_plugins = ("Netbanking.stepdefination.nm.nb_homefinance_emicalc_manual_step_defs",)
