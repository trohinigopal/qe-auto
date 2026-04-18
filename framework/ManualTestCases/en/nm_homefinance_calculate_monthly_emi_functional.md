# Functional manual test cases — Calculate monthly home loan EMI

**Traces to user story:** `US-HL-CALC-001` (`UserStories/en/nm_homefinance_calculate_monthly_emi.md`)  
**Suggested test environment:** Web — latest Chrome / Edge / Safari (mobile + desktop).  
**Application under test:** HDFC Bank home loans public portal (e.g. `https://homeloans.hdfc.bank.in/` — adjust if your SIT/UAT URL differs).

---

## TC-HL-CALC-001 — Navigate to monthly EMI calculator

| Field | Details |
|--------|---------|
| **Objective** | Verify a user can reach the “Calculate monthly EMI” experience from the home loan entry page. |
| **Priority** | High |
| **Preconditions** | Browser cache cleared or normal session; network available. |

**Steps**

1. Open the home loans landing page (base URL for your environment).
2. Locate the section **“Calculate Your Home Loan”** (or equivalent).
3. Select **“Calculate monthly EMI”** (or the control that opens the monthly EMI calculator).

**Expected results**

1. Page loads without a blocking error (no 5xx for a healthy environment).
2. The monthly EMI calculator is visible with inputs for **loan amount**, **tenure**, and **interest rate** (labels may vary slightly).

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-002 — Enter valid inputs and view EMI output

| Field | Details |
|--------|---------|
| **Objective** | Verify EMI and related outputs update for valid in-range values. |
| **Priority** | High |
| **Preconditions** | TC-HL-CALC-001 passed; calculator is on screen. |

**Steps**

1. Set **loan amount** to a mid-range value (e.g. ₹50,00,000) using slider or input, within the UI’s allowed range (e.g. ₹1 lakh–₹10 crore as per product).
2. Set **tenure** to **10 years** (within 1–30 if that is the published range).
3. Set **interest rate** to a valid value within the UI range (e.g. **8.5% p.a.**).
4. Observe displayed results (EMI, principal, interest / total interest as shown).

**Expected results**

1. All inputs accept the values without a generic error.
2. **Monthly EMI** is displayed as a positive amount (currency formatted).
3. **Principal** and **interest** (or **total interest**) are shown and are consistent with the inputs (no obvious arithmetic contradiction — e.g. EMI not zero when amount and rate are positive).
4. Changing one input **updates** the outputs without a full page error.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-003 — Recalculate when changing each input independently

| Field | Details |
|--------|---------|
| **Objective** | Verify outputs **recalculate** when loan amount, tenure, or rate changes. |
| **Priority** | High |
| **Preconditions** | Calculator visible with valid baseline values (reuse TC-HL-CALC-002). |

**Steps**

1. Note current **EMI** value.
2. Increase **loan amount** only; note new EMI.
3. Revert loan amount; increase **tenure** only; note new EMI.
4. Revert tenure; change **interest rate** only; note new EMI.

**Expected results**

1. Each change produces a **new** EMI (unless change is below UI precision — document if so).
2. Typically: higher loan amount → higher EMI; longer tenure → lower EMI; higher rate → higher EMI (sanity check).
3. No script error pop-ups or blank result area.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-004 — Boundary values (min / max) for sliders or inputs

| Field | Details |
|--------|---------|
| **Objective** | Verify behaviour at published minimum and maximum ranges. |
| **Priority** | Medium |
| **Preconditions** | Calculator visible. |

**Steps**

1. Set **loan amount** to the **minimum** allowed by the UI (e.g. ₹1 lakh).
2. Set **tenure** to **1 year** and **interest rate** to a valid low value in range.
3. Record EMI output.
4. Set **loan amount** to the **maximum** allowed (e.g. ₹10 crore) or the highest the slider allows.
5. Set **tenure** to **30 years** and **rate** to a valid value.
6. Record EMI output.

**Expected results**

1. Min and max values are accepted or the UI clearly prevents invalid entry.
2. EMI displays for both cases without crash.
3. If a value is not allowed, user sees a **clear message** (not silent failure).

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-005 — Amortization / “View details” / schedule (if offered)

| Field | Details |
|--------|---------|
| **Objective** | User can see EMI split over time **without** applying for a loan. |
| **Priority** | High |
| **Preconditions** | Valid EMI result on screen. |

**Steps**

1. Locate **View details**, **Amortization schedule**, **EMI break-down chart**, or similar.
2. Open the detailed view.
3. Scroll or navigate first few periods (month/year as applicable).
4. Close or navigate back to calculator.

**Expected results**

1. Detailed view opens **without** login if the product advertises guest access.
2. Schedule or chart shows **period-wise** split (principal vs interest) or equivalent breakdown.
3. User is **not** forced into loan application to view the breakdown (per story scope).
4. Returning to calculator preserves inputs or behaviour is clearly explained if reset.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-006 — Disclaimer visibility and content

| Field | Details |
|--------|---------|
| **Objective** | Verify planning-tool disclaimer is visible near the calculator. |
| **Priority** | High |
| **Preconditions** | Calculator section is visible. |

**Steps**

1. Scroll within the calculator module and adjacent area.
2. Read the **Note** / **Disclaimer** text associated with the calculator.

**Expected results**

1. Disclaimer states calculators are **planning tools** / **self-help** (wording may vary).
2. Text indicates results **depend on assumptions** and may not match final sanctioned terms.
3. Text is readable (contrast, font size) on desktop and mobile.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-007 — Apply Now from calculator context (optional path)

| Field | Details |
|--------|---------|
| **Objective** | Verify optional navigation to **Apply Now** from calculator outcome area. |
| **Priority** | Medium |
| **Preconditions** | Valid EMI result; **Apply Now** or equivalent is visible. |

**Steps**

1. From the calculator result area, select **Apply Now** (or equivalent).
2. Observe landing page (domain, title, login/register prompt).

**Expected results**

1. Browser navigates to the **online application** entry or a documented intermediary page.
2. No broken link (404) in production/SIT as applicable.
3. HTTPS is used for the application entry point.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-008 — Mobile viewport layout

| Field | Details |
|--------|---------|
| **Objective** | Calculator is usable on a mobile browser. |
| **Priority** | Medium |
| **Preconditions** | Real device or emulator; typical mobile width (e.g. 390px). |

**Steps**

1. Open the same home loans URL on mobile browser.
2. Open **Calculate monthly EMI** flow.
3. Adjust all three inputs using touch.
4. Open amortization/details if available.

**Expected results**

1. Inputs and results are visible without horizontal scroll (or acceptable scroll per design).
2. Sliders/inputs respond to touch; no overlapping labels that block input.
3. Disclaimer remains accessible (scroll to view if needed).

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-009 — Invalid or extreme input handling

| Field | Details |
|--------|---------|
| **Objective** | Out-of-range or invalid input is blocked or messaged clearly. |
| **Priority** | Medium |
| **Preconditions** | Calculator visible. |

**Steps**

1. Attempt to enter **loan amount** below minimum or above maximum (if free-text exists).
2. Attempt **tenure** 0 years or &gt; 30 years if the UI allows typing.
3. Attempt **interest rate** outside 0.5%–15% (or the published range on screen).

**Expected results**

1. UI prevents invalid values **or** shows validation message; EMI does not show misleading numbers.
2. No unhandled error page (500) from client-side validation.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## Summary

| Test ID | Title | Priority |
|---------|--------|----------|
| TC-HL-CALC-001 | Navigate to monthly EMI calculator | High |
| TC-HL-CALC-002 | Valid inputs → EMI output | High |
| TC-HL-CALC-003 | Recalculate on each input change | High |
| TC-HL-CALC-004 | Min / max boundaries | Medium |
| TC-HL-CALC-005 | Amortization / view details | High |
| TC-HL-CALC-006 | Disclaimer | High |
| TC-HL-CALC-007 | Apply Now (optional) | Medium |
| TC-HL-CALC-008 | Mobile layout | Medium |
| TC-HL-CALC-009 | Invalid / extreme input | Medium |
