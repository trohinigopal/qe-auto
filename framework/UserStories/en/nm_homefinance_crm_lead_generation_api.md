# User Story: Create home-loan inquiry via CRM lead API (partner integration)

**ID:** US-HL-API-LEAD-001  
**Epic:** Home finance — digital acquisition & CRM  
**Feature:** CRM lead generation (JSON) for home loan interest  
**Sources (reviewed):**  
- HDFC Bank API Portal — **Lead Creation** product (describes **CRM Lead Generation Save API (JSON)** and related lead/status APIs): [Lead Creation](https://developer.hdfc.bank.in/lead-creation)  
- **Lead Forms Journey** (Adobe lead forms for loan products including home loans; includes **CRM Lead Creation**): [Lead Forms Journey](https://developer.hdfcbank.com/lead-forms-journey) (UAT mirror lists same product family)  
- Public home-loans digital entry (same product line; `homeloans.hdfc.com` may redirect or mirror): [HDFC home loans](https://homeloans.hdfc.bank.in/) and **Apply Online** to [portal](https://portal.hdfc.bank.in/?ref_code=HDFC_W) / [apply online home loan form](https://applyonline.hdfc.bank.in/loan/home-loan-form.html)

**Note:** Public marketing sites do not publish raw REST paths in HTML. Contract, base URL, auth, and request/response schemas are provided **after registration** on the HDFC Bank developer portal. This story describes **behaviour** and **acceptance** for testing once credentials and sandbox URLs are available.

---

## Story

**As a** partner integrator or internal channel owner,  
**I want to** submit a **home loan lead** to HDFC Bank’s CRM using the documented **CRM Lead Generation** APIs (JSON/XML variants per portal),  
**So that** prospects who start on **homeloans** / **Apply Online** journeys can be captured consistently in CRM with traceability and status lookup.

## Background

The developer portal groups **“CRM Lead Generation Save API (JSON)”** (and related save/processing APIs) under **Lead Creation**, for creating leads in the bank’s CRM. A parallel product, **Lead Forms Journey**, includes **CRM Lead Creation** and OTP flows used with Adobe lead forms for loan products **including Home Loans**. These APIs complement the browser journeys (OTP, consent, reference number on submission).

## Acceptance criteria

1. Given a valid **client credential** (API key / OAuth as mandated by the portal for the chosen API), when the client sends a **valid JSON payload** per published schema for **CRM Lead Generation Save** (or the JSON variant named in the portal), then the API returns **success** (HTTP 2xx) and a **lead identifier** or confirmation token as documented.
2. Mandatory attributes (e.g. product = home loan, contact, consent flags as per contract) are **validated**; invalid payloads return **4xx** with a **machine-readable** error body.
3. Idempotency or duplicate handling behaves as documented (e.g. same mobile + product within a window) — document observed behaviour in SIT.
4. **ADV Query / Lead Status Inquiry** (or equivalent named on portal) can retrieve **status** using mobile number or lead id as per API contract.
5. Calls use **HTTPS** only; secrets are not logged in application logs.
6. Rate limits and IP allowlists (if any) are documented and enforced in tests via configurable base URL.

## Non-functional

- Response time SLA for synchronous lead save: align with portal / NFR for batch vs real-time.
- Audit: correlation id or request id returned or logged for support.

## Out of scope

- OTP generation/validation flows (separate APIs under Lead Forms Journey — own stories).
- NetBanking login APIs.

## Test hints (for API automation)

- Obtain **sandbox base URL** and **CRM Lead Generation Save (JSON)** path from subscribed developer docs (not repeated here).
- Store credentials in CI secrets; never commit.
- Negative cases: malformed JSON, missing consent, invalid mobile format.
