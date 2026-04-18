# Functional manual test cases — Calculate monthly EMI

**Traces to user story:** `US-HL-CALC-001` (`UserStories/en/nm_homefinance_calculate_monthly_emi.md`)
**Suggested test environment:** Web — latest Chrome / Edge / Safari (mobile + desktop where applicable).
**Application / system under test:** https://homeloans.hdfc.bank.in/

**User story summary:** As a prospective home loan customer,… — I want to enter my loan amount, tenure, and interest rate and see my estimated monthly EMI plus principal/interest split,…

---

## TC-HL-CALC-001 — Given I am on the home loan landing page, when I choose Calculate monthly EMI, I c...

| Field | Details |
|--------|---------|
| **Objective** | Verify: Given I am on the home loan landing page, when I choose Calculate monthly EMI, I can enter or adjust loan amount, tenure (years), and interest rate (% p.a.) within the published ranges. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Navigate to the relevant calculator or screen described in the user story.
2. Adjust inputs (loan amount, tenure, rate, etc.) as applicable to this criterion.
3. Observe displayed results, disclaimers, and navigation options.

**Expected results**

1. UI matches the acceptance criterion (visible elements, values, or messages).
2. No unhandled error pages (5xx) for healthy environments.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-002 — When I change any input, the system recalculates and displays at least: monthly EM...

| Field | Details |
|--------|---------|
| **Objective** | Verify: When I change any input, the system recalculates and displays at least: monthly EMI, principal component, interest component (and/or total interest), consistent with the inputs. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Navigate to the relevant calculator or screen described in the user story.
2. Adjust inputs (loan amount, tenure, rate, etc.) as applicable to this criterion.
3. Observe displayed results, disclaimers, and navigation options.

**Expected results**

1. UI matches the acceptance criterion (visible elements, values, or messages).
2. No unhandled error pages (5xx) for healthy environments.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-003 — I can open view details / amortization (or equivalent) to see how EMI splits over ...

| Field | Details |
|--------|---------|
| **Objective** | Verify: I can open view details / amortization (or equivalent) to see how EMI splits over time, without submitting a loan application. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Navigate to the relevant calculator or screen described in the user story.
2. Adjust inputs (loan amount, tenure, rate, etc.) as applicable to this criterion.
3. Observe displayed results, disclaimers, and navigation options.

**Expected results**

1. UI matches the acceptance criterion (visible elements, values, or messages).
2. No unhandled error pages (5xx) for healthy environments.
3. Detail or schedule view opens without forcing unrelated flows.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-004 — A disclaimer is visible stating that calculators are self-help planning tools, res...

| Field | Details |
|--------|---------|
| **Objective** | Verify: A disclaimer is visible stating that calculators are self-help planning tools, results depend on assumptions, and accuracy is not guaranteed for my final offer (aligned with on-page copy). |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Navigate to the relevant calculator or screen described in the user story.
2. Adjust inputs (loan amount, tenure, rate, etc.) as applicable to this criterion.
3. Observe displayed results, disclaimers, and navigation options.

**Expected results**

1. UI matches the acceptance criterion (visible elements, values, or messages).
2. No unhandled error pages (5xx) for healthy environments.
3. Disclaimer text is visible and readable.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## TC-HL-CALC-005 — Optional: From the calculator outcome, I can navigate to Apply Now (e.g. to the on...

| Field | Details |
|--------|---------|
| **Objective** | Verify: Optional: From the calculator outcome, I can navigate to Apply Now (e.g. to the online application entry point) without losing context where the product allows it. |
| **Priority** | High |
| **Preconditions** | Test data and environment access per team standards; story prerequisites met. |

**Steps**

1. Navigate to the relevant calculator or screen described in the user story.
2. Adjust inputs (loan amount, tenure, rate, etc.) as applicable to this criterion.
3. Observe displayed results, disclaimers, and navigation options.

**Expected results**

1. UI matches the acceptance criterion (visible elements, values, or messages).
2. No unhandled error pages (5xx) for healthy environments.

**Pass / Fail** | **Tester** | **Date** | **Notes**

---

## Non-functional checks (from user story)

- Calculator works on common desktop and mobile browsers supported by the site.
- Inputs reject or clearly message out-of-range values per UI rules.
