# Functional manual test cases — CRM lead generation (JSON) for home loan interest

**Traces to user story:** `US-HL-API-LEAD-001` (`UserStories/en/nm_homefinance_crm_lead_generation_api.md`)
**Suggested test environment:** API — SIT/UAT base URL from developer portal / internal config (never commit secrets).
**Application / system under test:** See user story source section for environment URLs.

**User story summary:** As a partner integrator or internal channel owner,… — I want to submit a **home loan lead** to HDFC Bank’s CRM using the documented **CRM Lead Generation** APIs (JSON/XML variants per portal),…

---

## TC-HL-API-LEAD-001 — Given a valid client credential (API key / OAuth as mandated by the portal for the...

| Field | Details |
|--------|---------|
| **Objective** | Verify: Given a valid client credential (API key / OAuth as mandated by the portal for the chosen API), when the client sends a valid JSON payload per published schema for CRM Lead Generation Save (or the JSON variant named in the portal), then the API returns success (HTTP 2xx) and a lead identifier or confirmation token as documented. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
2. Execute the scenario for acceptance criterion 1: align request body/path with published schema.
3. Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).

**Expected results**

1. Response status is in 2xx family for valid requests as documented.
2. Observed behaviour matches the acceptance criterion text.
3. Errors return structured response as per contract when validation fails.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-API-LEAD-002 — Mandatory attributes (e.g. product = home loan, contact, consent flags as per cont...

| Field | Details |
|--------|---------|
| **Objective** | Verify: Mandatory attributes (e.g. product = home loan, contact, consent flags as per contract) are validated; invalid payloads return 4xx with a machine-readable error body. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
2. Execute the scenario for acceptance criterion 2: align request body/path with published schema.
3. Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).

**Expected results**

1. Invalid inputs yield 4xx with parseable error payload.
2. Observed behaviour matches the acceptance criterion text.
3. Errors return structured response as per contract when validation fails.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-API-LEAD-003 — Idempotency or duplicate handling behaves as documented (e.g. same mobile + produc...

| Field | Details |
|--------|---------|
| **Objective** | Verify: Idempotency or duplicate handling behaves as documented (e.g. same mobile + product within a window) — document observed behaviour in SIT. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
2. Execute the scenario for acceptance criterion 3: align request body/path with published schema.
3. Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).

**Expected results**

1. Observed behaviour matches the acceptance criterion text.
2. Errors return structured response as per contract when validation fails.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-API-LEAD-004 — ADV Query / Lead Status Inquiry (or equivalent named on portal) can retrieve statu...

| Field | Details |
|--------|---------|
| **Objective** | Verify: ADV Query / Lead Status Inquiry (or equivalent named on portal) can retrieve status using mobile number or lead id as per API contract. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
2. Invoke status/query API with documented identifiers (mobile, lead id, etc.).
3. Execute the scenario for acceptance criterion 4: align request body/path with published schema.
4. Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).

**Expected results**

1. Observed behaviour matches the acceptance criterion text.
2. Errors return structured response as per contract when validation fails.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-API-LEAD-005 — Calls use HTTPS only; secrets are not logged in application logs.

| Field | Details |
|--------|---------|
| **Objective** | Verify: Calls use HTTPS only; secrets are not logged in application logs. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
2. Execute the scenario for acceptance criterion 5: align request body/path with published schema.
3. Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).

**Expected results**

1. Observed behaviour matches the acceptance criterion text.
2. Errors return structured response as per contract when validation fails.
3. Transport is HTTPS only.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-API-LEAD-006 — Rate limits and IP allowlists (if any) are documented and enforced in tests via co...

| Field | Details |
|--------|---------|
| **Objective** | Verify: Rate limits and IP allowlists (if any) are documented and enforced in tests via configurable base URL. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Configure base URL, credentials, and headers per environment (SIT/UAT) and API contract.
2. Execute the scenario for acceptance criterion 6: align request body/path with published schema.
3. Capture HTTP status, response body, and correlation/reference ids from logs (no secrets in plain text).

**Expected results**

1. Observed behaviour matches the acceptance criterion text.
2. Errors return structured response as per contract when validation fails.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## Non-functional checks (from user story)

- Response time SLA for synchronous lead save: align with portal / NFR for batch vs real-time.
- Audit: correlation id or request id returned or logged for support.
