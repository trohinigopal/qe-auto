"""BDD step definitions for nb_homefinance_emicalc_manual (shared with CrossChannel).

Originally generated from manual testcase; materialized via bdd_dom_materialize.
"""

import sys
from pathlib import Path
_FW = Path(__file__).resolve().parents[3]
if str(_FW) not in sys.path:
    sys.path.insert(0, str(_FW))

from pytest_bdd import given, parsers, scenario, then, when

_MAT_CHANNEL = 'Netbanking'
_MAT_STEM = 'nb_homefinance_emicalc_manual'


@given(parsers.parse("Browser cache cleared or normal session; network available."))
def step_browser_cache_cleared_or_normal_session_network_av(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Browser cache cleared or normal session; network available.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Open the home loans landing page (base URL for your environment)."))
def step_open_the_home_loans_landing_page_base_url_for_your(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Open the home loans landing page (base URL for your environment).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Locate the section “Calculate Your Home Loan” (or equivalent)."))
def step_locate_the_section_calculate_your_home_loan_or_equ(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Locate the section “Calculate Your Home Loan” (or equivalent).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Select “Calculate monthly EMI” (or the control that opens the monthly EMI calculator)."))
def step_select_calculate_monthly_emi_or_the_control_that_o(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Select “Calculate monthly EMI” (or the control that opens the monthly EMI calculator).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Page loads without a blocking error (no 5xx for a healthy environment)."))
def step_page_loads_without_a_blocking_error_no_5xx_for_a_h(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Page loads without a blocking error (no 5xx for a healthy environment).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("The monthly EMI calculator is visible with inputs for loan amount, tenure, and interest rate (labels may vary slightly)."))
def step_the_monthly_emi_calculator_is_visible_with_inputs_(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'The monthly EMI calculator is visible with inputs for loan amount, tenure, and interest rate (labels may vary slightly).', _FW, _MAT_CHANNEL, _MAT_STEM)
@given(parsers.parse("TC-HL-CALC-001 passed; calculator is on screen."))
def step_tc_hl_calc_001_passed_calculator_is_on_screen(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'TC-HL-CALC-001 passed; calculator is on screen.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Set loan amount to a mid-range value (e.g. ₹50,00,000) using slider or input, within the UI’s allowed range (e.g. ₹1 lakh–₹10 crore as per product)."))
def step_set_loan_amount_to_a_mid_range_value_e_g_50_00_000(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Set loan amount to a mid-range value (e.g. ₹50,00,000) using slider or input, within the UI’s allowed range (e.g. ₹1 lakh–₹10 crore as per product).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Set tenure to 10 years (within 1–30 if that is the published range)."))
def step_set_tenure_to_10_years_within_1_30_if_that_is_the_(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Set tenure to 10 years (within 1–30 if that is the published range).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Set interest rate to a valid value within the UI range (e.g. 8.5% p.a.)."))
def step_set_interest_rate_to_a_valid_value_within_the_ui_r(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Set interest rate to a valid value within the UI range (e.g. 8.5% p.a.).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Observe displayed results (EMI, principal, interest / total interest as shown)."))
def step_observe_displayed_results_emi_principal_interest_t(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Observe displayed results (EMI, principal, interest / total interest as shown).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("All inputs accept the values without a generic error."))
def step_all_inputs_accept_the_values_without_a_generic_err(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'All inputs accept the values without a generic error.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Monthly EMI is displayed as a positive amount (currency formatted)."))
def step_monthly_emi_is_displayed_as_a_positive_amount_curr(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Monthly EMI is displayed as a positive amount (currency formatted).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Principal and interest (or total interest) are shown and are consistent with the inputs (no obvious arithmetic contradiction — e.g. EMI not zero when amount and rate are positive)."))
def step_principal_and_interest_or_total_interest_are_shown(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Principal and interest (or total interest) are shown and are consistent with the inputs (no obvious arithmetic contradiction — e.g. EMI not zero when amount and rate are positive).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Changing one input updates the outputs without a full page error."))
def step_changing_one_input_updates_the_outputs_without_a_f(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Changing one input updates the outputs without a full page error.', _FW, _MAT_CHANNEL, _MAT_STEM)
@given(parsers.parse("Calculator visible with valid baseline values (reuse TC-HL-CALC-002)."))
def step_calculator_visible_with_valid_baseline_values_reus(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Calculator visible with valid baseline values (reuse TC-HL-CALC-002).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Note current EMI value."))
def step_note_current_emi_value(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Note current EMI value.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Increase loan amount only; note new EMI."))
def step_increase_loan_amount_only_note_new_emi(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Increase loan amount only; note new EMI.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Revert loan amount; increase tenure only; note new EMI."))
def step_revert_loan_amount_increase_tenure_only_note_new_e(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Revert loan amount; increase tenure only; note new EMI.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Revert tenure; change interest rate only; note new EMI."))
def step_revert_tenure_change_interest_rate_only_note_new_e(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Revert tenure; change interest rate only; note new EMI.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Each change produces a new EMI (unless change is below UI precision — document if so)."))
def step_each_change_produces_a_new_emi_unless_change_is_be(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Each change produces a new EMI (unless change is below UI precision — document if so).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Typically: higher loan amount → higher EMI; longer tenure → lower EMI; higher rate → higher EMI (sanity check)."))
def step_typically_higher_loan_amount_higher_emi_longer_ten(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Typically: higher loan amount → higher EMI; longer tenure → lower EMI; higher rate → higher EMI (sanity check).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("No script error pop-ups or blank result area."))
def step_no_script_error_pop_ups_or_blank_result_area(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'No script error pop-ups or blank result area.', _FW, _MAT_CHANNEL, _MAT_STEM)
@given(parsers.parse("Calculator visible."))
def step_calculator_visible(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Calculator visible.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Set loan amount to the minimum allowed by the UI (e.g. ₹1 lakh)."))
def step_set_loan_amount_to_the_minimum_allowed_by_the_ui_e(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Set loan amount to the minimum allowed by the UI (e.g. ₹1 lakh).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Set tenure to 1 year and interest rate to a valid low value in range."))
def step_set_tenure_to_1_year_and_interest_rate_to_a_valid_(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Set tenure to 1 year and interest rate to a valid low value in range.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Record EMI output."))
def step_record_emi_output(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Record EMI output.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Set loan amount to the maximum allowed (e.g. ₹10 crore) or the highest the slider allows."))
def step_set_loan_amount_to_the_maximum_allowed_e_g_10_cror(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Set loan amount to the maximum allowed (e.g. ₹10 crore) or the highest the slider allows.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Set tenure to 30 years and rate to a valid value."))
def step_set_tenure_to_30_years_and_rate_to_a_valid_value(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Set tenure to 30 years and rate to a valid value.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Min and max values are accepted or the UI clearly prevents invalid entry."))
def step_min_and_max_values_are_accepted_or_the_ui_clearly_(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Min and max values are accepted or the UI clearly prevents invalid entry.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("EMI displays for both cases without crash."))
def step_emi_displays_for_both_cases_without_crash(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'EMI displays for both cases without crash.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("If a value is not allowed, user sees a clear message (not silent failure)."))
def step_if_a_value_is_not_allowed_user_sees_a_clear_messag(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'If a value is not allowed, user sees a clear message (not silent failure).', _FW, _MAT_CHANNEL, _MAT_STEM)
@given(parsers.parse("Valid EMI result on screen."))
def step_valid_emi_result_on_screen(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Valid EMI result on screen.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Locate View details, Amortization schedule, EMI break-down chart, or similar."))
def step_locate_view_details_amortization_schedule_emi_brea(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Locate View details, Amortization schedule, EMI break-down chart, or similar.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Open the detailed view."))
def step_open_the_detailed_view(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Open the detailed view.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Scroll or navigate first few periods (month/year as applicable)."))
def step_scroll_or_navigate_first_few_periods_month_year_as(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Scroll or navigate first few periods (month/year as applicable).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Close or navigate back to calculator."))
def step_close_or_navigate_back_to_calculator(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Close or navigate back to calculator.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Detailed view opens without login if the product advertises guest access."))
def step_detailed_view_opens_without_login_if_the_product_a(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Detailed view opens without login if the product advertises guest access.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Schedule or chart shows period-wise split (principal vs interest) or equivalent breakdown."))
def step_schedule_or_chart_shows_period_wise_split_principa(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Schedule or chart shows period-wise split (principal vs interest) or equivalent breakdown.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("User is not forced into loan application to view the breakdown (per story scope)."))
def step_user_is_not_forced_into_loan_application_to_view_t(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'User is not forced into loan application to view the breakdown (per story scope).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Returning to calculator preserves inputs or behaviour is clearly explained if reset."))
def step_returning_to_calculator_preserves_inputs_or_behavi(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Returning to calculator preserves inputs or behaviour is clearly explained if reset.', _FW, _MAT_CHANNEL, _MAT_STEM)
@given(parsers.parse("Calculator section is visible."))
def step_calculator_section_is_visible(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Calculator section is visible.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Scroll within the calculator module and adjacent area."))
def step_scroll_within_the_calculator_module_and_adjacent_a(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Scroll within the calculator module and adjacent area.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Read the Note / Disclaimer text associated with the calculator."))
def step_read_the_note_disclaimer_text_associated_with_the_(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Read the Note / Disclaimer text associated with the calculator.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Disclaimer states calculators are planning tools / self-help (wording may vary)."))
def step_disclaimer_states_calculators_are_planning_tools_s(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Disclaimer states calculators are planning tools / self-help (wording may vary).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Text indicates results depend on assumptions and may not match final sanctioned terms."))
def step_text_indicates_results_depend_on_assumptions_and_m(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Text indicates results depend on assumptions and may not match final sanctioned terms.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Text is readable (contrast, font size) on desktop and mobile."))
def step_text_is_readable_contrast_font_size_on_desktop_and(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Text is readable (contrast, font size) on desktop and mobile.', _FW, _MAT_CHANNEL, _MAT_STEM)
@given(parsers.parse("Valid EMI result; **Apply Now** or equivalent is visible."))
def step_valid_emi_result_apply_now_or_equivalent_is_visibl(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Valid EMI result; **Apply Now** or equivalent is visible.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("From the calculator result area, select Apply Now (or equivalent)."))
def step_from_the_calculator_result_area_select_apply_now_o(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'From the calculator result area, select Apply Now (or equivalent).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Observe landing page (domain, title, login/register prompt)."))
def step_observe_landing_page_domain_title_login_register_p(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Observe landing page (domain, title, login/register prompt).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Browser navigates to the online application entry or a documented intermediary page."))
def step_browser_navigates_to_the_online_application_entry_(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Browser navigates to the online application entry or a documented intermediary page.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("No broken link (404) in production/SIT as applicable."))
def step_no_broken_link_404_in_production_sit_as_applicable(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'No broken link (404) in production/SIT as applicable.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("HTTPS is used for the application entry point."))
def step_https_is_used_for_the_application_entry_point(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'HTTPS is used for the application entry point.', _FW, _MAT_CHANNEL, _MAT_STEM)
@given(parsers.parse("Real device or emulator; typical mobile width (e.g. 390px)."))
def step_real_device_or_emulator_typical_mobile_width_e_g_3(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Real device or emulator; typical mobile width (e.g. 390px).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Open the same home loans URL on mobile browser."))
def step_open_the_same_home_loans_url_on_mobile_browser(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Open the same home loans URL on mobile browser.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Open Calculate monthly EMI flow."))
def step_open_calculate_monthly_emi_flow(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Open Calculate monthly EMI flow.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Adjust all three inputs using touch."))
def step_adjust_all_three_inputs_using_touch(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Adjust all three inputs using touch.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Open amortization/details if available."))
def step_open_amortization_details_if_available(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Open amortization/details if available.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Inputs and results are visible without horizontal scroll (or acceptable scroll per design)."))
def step_inputs_and_results_are_visible_without_horizontal_(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Inputs and results are visible without horizontal scroll (or acceptable scroll per design).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Sliders/inputs respond to touch; no overlapping labels that block input."))
def step_sliders_inputs_respond_to_touch_no_overlapping_lab(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Sliders/inputs respond to touch; no overlapping labels that block input.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("Disclaimer remains accessible (scroll to view if needed)."))
def step_disclaimer_remains_accessible_scroll_to_view_if_ne(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Disclaimer remains accessible (scroll to view if needed).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Attempt to enter loan amount below minimum or above maximum (if free-text exists)."))
def step_attempt_to_enter_loan_amount_below_minimum_or_abov(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Attempt to enter loan amount below minimum or above maximum (if free-text exists).', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Attempt tenure 0 years or &gt; 30 years if the UI allows typing."))
def step_attempt_tenure_0_years_or_gt_30_years_if_the_ui_al(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Attempt tenure 0 years or &gt; 30 years if the UI allows typing.', _FW, _MAT_CHANNEL, _MAT_STEM)
@when(parsers.parse("Attempt interest rate outside 0.5%–15% (or the published range on screen)."))
def step_attempt_interest_rate_outside_0_5_15_or_the_publis(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'Attempt interest rate outside 0.5%–15% (or the published range on screen).', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("UI prevents invalid values or shows validation message; EMI does not show misleading numbers."))
def step_ui_prevents_invalid_values_or_shows_validation_mes(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'UI prevents invalid values or shows validation message; EMI does not show misleading numbers.', _FW, _MAT_CHANNEL, _MAT_STEM)
@then(parsers.parse("No unhandled error page (500) from client-side validation."))
def step_no_unhandled_error_page_500_from_client_side_valid(ui_driver):
    if ui_driver is None:
        import pytest
        pytest.skip('Web driver required for this step')
    from common.utils.bdd_step_runner import execute_materialized_step
    execute_materialized_step(ui_driver, 'No unhandled error page (500) from client-side validation.', _FW, _MAT_CHANNEL, _MAT_STEM)
