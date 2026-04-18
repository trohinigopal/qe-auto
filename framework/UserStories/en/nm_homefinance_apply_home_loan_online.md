# User Story: Apply for a home loan online

**ID:** US-HL-APPLY-001  
**Epic:** Home finance — acquisition & onboarding  
**Feature:** Apply for home loan online  
**Source (reviewed):** Public HDFC Bank home loans portal (`https://homeloans.hdfc.bank.in/`).  
**Note:** `https://homeloans.hdfc.com/` was not reachable (HTTP 503) at documentation time; behaviour described here matches the live home-loans journey (e.g. **Apply Now** to `https://portal.hdfc.bank.in/?ref_code=HDFC_W`).

---

## Story

**As a** customer who wants HDFC Bank home finance,  
**I want to** start an **online application** after choosing my product (for example housing vs non-housing vs refinance) and complete registration, application, document upload, and fees as required,  
**So that** I can move toward approval without visiting a branch first.

## Background

The landing experience includes **product type** selection (e.g. Housing Loans, Non Housing Loans, Refinance), **Apply Now** entry, and supporting journeys such as **“Let Us Contact You”** / **Instant Call Back** for expert assistance. Industry-standard online home loan flows typically include: sign-up/register, application form, document upload, processing fee payment, and then status/approval steps.

## Acceptance criteria

1. Given I am on the home loans entry page, I can **select product type** (e.g. Housing / Non Housing / Refinance) and a **specific product** where applicable before starting an application.
2. When I choose **Apply Now**, I am taken to the **online application** entry (external portal URL as published on the site) and can **register or sign in** as required.
3. I can complete the **application form** with the mandatory fields defined by the bank for that product.
4. I can **upload** required **KYC and income/property** documents per the journey (formats and size limits as per UI).
5. I can **pay the processing fee** (or see clear next steps if payment is deferred) where the product flow requires it.
6. I receive **confirmation** of submission (on-screen message, reference ID, email/SMS if applicable) so I can track progress.
7. Alternative path: From the same area, I can request **“Let Us Contact You”** / **Instant Call Back** with **name, mobile, email, pincode** (and NRI fields if applicable) and see **success** or **error** handling.

## Non-functional

- Application pages load over HTTPS; PII fields are handled per site security patterns.
- Mobile and desktop layouts remain usable for core apply and contact flows.

## Out of scope (for this story)

- Underwriting, legal verification, and disbursement (separate stories).
- Branch-only or doorstep variants except where linked from the same landing page.
