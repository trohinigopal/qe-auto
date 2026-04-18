"""BDD step definitions for api_my_feature (shared with CrossChannel).

Originally generated from manual testcase; materialized via api_bdd_materialize.
"""

import sys
from pathlib import Path
_FW = Path(__file__).resolve().parents[3]
if str(_FW) not in sys.path:
    sys.path.insert(0, str(_FW))

from pytest_bdd import given, parsers, scenario, then, when

_MAT_CHANNEL = 'API'
_MAT_STEM = 'api_my_feature'

@given(parsers.parse("Test data and environment access per team standards; story prerequisites met."))
def step_test_data_and_environment_access_per_team_standard(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Test data and environment access per team standards; story prerequisites met.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract."))
def step_configure_base_url_credentials_and_headers_per_env(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Execute the scenario for acceptance criterion 1: align request body/path with published schema."))
def step_execute_the_scenario_for_acceptance_criterion_1_al(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Execute the scenario for acceptance criterion 1: align request body/path with published schema.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text)."))
def step_capture_http_status_response_body_and_correlation_(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Response status is in 2xx family for valid requests as documented."))
def step_response_status_is_in_2xx_family_for_valid_request(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Response status is in 2xx family for valid requests as documented.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Observed behaviour matches the acceptance criterion text."))
def step_observed_behaviour_matches_the_acceptance_criterio(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Observed behaviour matches the acceptance criterion text.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Errors return structured response as per contract when validation fails."))
def step_errors_return_structured_response_as_per_contract_(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Errors return structured response as per contract when validation fails.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Execute the scenario for acceptance criterion 2: align request body/path with published schema."))
def step_execute_the_scenario_for_acceptance_criterion_2_al(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Execute the scenario for acceptance criterion 2: align request body/path with published schema.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Invalid inputs yield 4xx with parseable error payload."))
def step_invalid_inputs_yield_4xx_with_parseable_error_payl(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Invalid inputs yield 4xx with parseable error payload.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Execute the scenario for acceptance criterion 3: align request body/path with published schema."))
def step_execute_the_scenario_for_acceptance_criterion_3_al(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Execute the scenario for acceptance criterion 3: align request body/path with published schema.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Invoke status/query API with documented identifiers (mobile, lead id, etc.)."))
def step_invoke_status_query_api_with_documented_identifier(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Invoke status/query API with documented identifiers (mobile, lead id, etc.).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Execute the scenario for acceptance criterion 4: align request body/path with published schema."))
def step_execute_the_scenario_for_acceptance_criterion_4_al(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Execute the scenario for acceptance criterion 4: align request body/path with published schema.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Execute the scenario for acceptance criterion 5: align request body/path with published schema."))
def step_execute_the_scenario_for_acceptance_criterion_5_al(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Execute the scenario for acceptance criterion 5: align request body/path with published schema.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Transport is HTTPS only."))
def step_transport_is_https_only(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Transport is HTTPS only.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Execute the scenario for acceptance criterion 6: align request body/path with published schema."))
def step_execute_the_scenario_for_acceptance_criterion_6_al(api_client):
    if api_client is None:
        import pytest
        pytest.skip('API client required for this step')
    from common.utils.api_bdd_step_runner import execute_api_materialized_step
    execute_api_materialized_step(api_client, 'Execute the scenario for acceptance criterion 6: align request body/path with published schema.', _FW, _MAT_CHANNEL, _MAT_STEM)
