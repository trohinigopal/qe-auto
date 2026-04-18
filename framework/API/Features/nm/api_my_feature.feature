@api @generated
Feature: Auto-generated from nm_homefinance_crm_lead_generation_api_manual.md

  Scenario: TC-HL-API-LEAD-001 Given a valid client credential (API key / OAuth as mandated by the portal for the...
    Given Test data and environment access per team standards; story prerequisites met.
    When Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
    And Execute the scenario for acceptance criterion 1: align request body/path with published schema.
    And Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).
    Then Response status is in 2xx family for valid requests as documented.
    And Observed behaviour matches the acceptance criterion text.
    And Errors return structured response as per contract when validation fails.

  Scenario: TC-HL-API-LEAD-002 Mandatory attributes (e.g. product = home loan, contact, consent flags as per cont...
    Given Test data and environment access per team standards; story prerequisites met.
    When Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
    And Execute the scenario for acceptance criterion 2: align request body/path with published schema.
    And Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).
    Then Invalid inputs yield 4xx with parseable error payload.
    And Observed behaviour matches the acceptance criterion text.
    And Errors return structured response as per contract when validation fails.

  Scenario: TC-HL-API-LEAD-003 Idempotency or duplicate handling behaves as documented (e.g. same mobile + produc...
    Given Test data and environment access per team standards; story prerequisites met.
    When Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
    And Execute the scenario for acceptance criterion 3: align request body/path with published schema.
    And Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).
    Then Observed behaviour matches the acceptance criterion text.
    And Errors return structured response as per contract when validation fails.

  Scenario: TC-HL-API-LEAD-004 ADV Query / Lead Status Inquiry (or equivalent named on portal) can retrieve statu...
    Given Test data and environment access per team standards; story prerequisites met.
    When Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
    And Invoke status/query API with documented identifiers (mobile, lead id, etc.).
    And Execute the scenario for acceptance criterion 4: align request body/path with published schema.
    And Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).
    Then Observed behaviour matches the acceptance criterion text.
    And Errors return structured response as per contract when validation fails.

  Scenario: TC-HL-API-LEAD-005 Calls use HTTPS only; secrets are not logged in application logs.
    Given Test data and environment access per team standards; story prerequisites met.
    When Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
    And Execute the scenario for acceptance criterion 5: align request body/path with published schema.
    And Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).
    Then Observed behaviour matches the acceptance criterion text.
    And Errors return structured response as per contract when validation fails.
    And Transport is HTTPS only.

  Scenario: TC-HL-API-LEAD-006 Rate limits and IP allowlists (if any) are documented and enforced in tests via co...
    Given Test data and environment access per team standards; story prerequisites met.
    When Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
    And Execute the scenario for acceptance criterion 6: align request body/path with published schema.
    And Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).
    Then Observed behaviour matches the acceptance criterion text.
    And Errors return structured response as per contract when validation fails.
