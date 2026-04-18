@web @web @generated
Feature: Auto-generated from nm_homefinance_calculate_monthly_emi_functional.md

  Scenario: TC-HL-CALC-001 Navigate to monthly EMI calculator
    Given Browser cache cleared or normal session; network available.
    When Open the home loans landing page (base URL for your environment).
    And Locate the section “Calculate Your Home Loan” (or equivalent).
    And Select “Calculate monthly EMI” (or the control that opens the monthly EMI calculator).
    Then Page loads without a blocking error (no 5xx for a healthy environment).
    And The monthly EMI calculator is visible with inputs for loan amount, tenure, and interest rate (labels may vary slightly).

  Scenario: TC-HL-CALC-002 Enter valid inputs and view EMI output
    Given TC-HL-CALC-001 passed; calculator is on screen.
    When Set loan amount to a mid-range value (e.g. ₹50,00,000) using slider or input, within the UI’s allowed range (e.g. ₹1 lakh–₹10 crore as per product).
    And Set tenure to 10 years (within 1–30 if that is the published range).
    And Set interest rate to a valid value within the UI range (e.g. 8.5% p.a.).
    And Observe displayed results (EMI, principal, interest / total interest as shown).
    Then All inputs accept the values without a generic error.
    And Monthly EMI is displayed as a positive amount (currency formatted).
    And Principal and interest (or total interest) are shown and are consistent with the inputs (no obvious arithmetic contradiction — e.g. EMI not zero when amount and rate are positive).
    And Changing one input updates the outputs without a full page error.

  Scenario: TC-HL-CALC-003 Recalculate when changing each input independently
    Given Calculator visible with valid baseline values (reuse TC-HL-CALC-002).
    When Note current EMI value.
    And Increase loan amount only; note new EMI.
    And Revert loan amount; increase tenure only; note new EMI.
    And Revert tenure; change interest rate only; note new EMI.
    Then Each change produces a new EMI (unless change is below UI precision — document if so).
    And Typically: higher loan amount → higher EMI; longer tenure → lower EMI; higher rate → higher EMI (sanity check).
    And No script error pop-ups or blank result area.

  Scenario: TC-HL-CALC-004 Boundary values (min / max) for sliders or inputs
    Given Calculator visible.
    When Set loan amount to the minimum allowed by the UI (e.g. ₹1 lakh).
    And Set tenure to 1 year and interest rate to a valid low value in range.
    And Record EMI output.
    And Set loan amount to the maximum allowed (e.g. ₹10 crore) or the highest the slider allows.
    And Set tenure to 30 years and rate to a valid value.
    And Record EMI output.
    Then Min and max values are accepted or the UI clearly prevents invalid entry.
    And EMI displays for both cases without crash.
    And If a value is not allowed, user sees a clear message (not silent failure).

  Scenario: TC-HL-CALC-005 Amortization / “View details” / schedule (if offered)
    Given Valid EMI result on screen.
    When Locate View details, Amortization schedule, EMI break-down chart, or similar.
    And Open the detailed view.
    And Scroll or navigate first few periods (month/year as applicable).
    And Close or navigate back to calculator.
    Then Detailed view opens without login if the product advertises guest access.
    And Schedule or chart shows period-wise split (principal vs interest) or equivalent breakdown.
    And User is not forced into loan application to view the breakdown (per story scope).
    And Returning to calculator preserves inputs or behaviour is clearly explained if reset.

  Scenario: TC-HL-CALC-006 Disclaimer visibility and content
    Given Calculator section is visible.
    When Scroll within the calculator module and adjacent area.
    And Read the Note / Disclaimer text associated with the calculator.
    Then Disclaimer states calculators are planning tools / self-help (wording may vary).
    And Text indicates results depend on assumptions and may not match final sanctioned terms.
    And Text is readable (contrast, font size) on desktop and mobile.

  Scenario: TC-HL-CALC-007 Apply Now from calculator context (optional path)
    Given Valid EMI result; **Apply Now** or equivalent is visible.
    When From the calculator result area, select Apply Now (or equivalent).
    And Observe landing page (domain, title, login/register prompt).
    Then Browser navigates to the online application entry or a documented intermediary page.
    And No broken link (404) in production/SIT as applicable.
    And HTTPS is used for the application entry point.

  Scenario: TC-HL-CALC-008 Mobile viewport layout
    Given Real device or emulator; typical mobile width (e.g. 390px).
    When Open the same home loans URL on mobile browser.
    And Open Calculate monthly EMI flow.
    And Adjust all three inputs using touch.
    And Open amortization/details if available.
    Then Inputs and results are visible without horizontal scroll (or acceptable scroll per design).
    And Sliders/inputs respond to touch; no overlapping labels that block input.
    And Disclaimer remains accessible (scroll to view if needed).

  Scenario: TC-HL-CALC-009 Invalid or extreme input handling
    Given Calculator visible.
    When Attempt to enter loan amount below minimum or above maximum (if free-text exists).
    And Attempt tenure 0 years or &gt; 30 years if the UI allows typing.
    And Attempt interest rate outside 0.5%–15% (or the published range on screen).
    Then UI prevents invalid values or shows validation message; EMI does not show misleading numbers.
    And No unhandled error page (500) from client-side validation.
