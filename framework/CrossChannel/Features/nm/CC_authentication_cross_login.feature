@cross @smoke @generated
Feature: Cross Channel Unified Login — web EMI flow then API lead check

  Scenario: Navigate to monthly EMI calculator and check api
    Given Browser cache cleared or normal session; network available.
    When Open the home loans landing page (base URL for your environment).
    And Locate the section “Calculate Your Home Loan” (or equivalent).
    And Select “Calculate monthly EMI” (or the control that opens the monthly EMI calculator).
    Then Page loads without a blocking error (no 5xx for a healthy environment).
    And The monthly EMI calculator is visible with inputs for loan amount, tenure, and interest rate (labels may vary slightly).
    Given Test data and environment access per team standards; story prerequisites met.
    When Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
    And Execute the scenario for acceptance criterion 1: align request body/path with published schema.
    And Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).
    Then Response status is in 2xx family for valid requests as documented.
    And Observed behaviour matches the acceptance criterion text.
    And Errors return structured response as per contract when validation fails.
