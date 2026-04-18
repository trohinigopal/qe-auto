# User Story: Calculate monthly home loan EMI

**ID:** US-HL-CALC-001  
**Epic:** Home finance — planning & calculators  
**Feature:** Calculate monthly EMI  
**Source (reviewed):** Public HDFC Bank home loans portal (`https://homeloans.hdfc.bank.in/`).  
**Note:** `https://homeloans.hdfc.com/` was not reachable (HTTP 503) at documentation time; behaviour described here matches the live home-loans journey above.

---

## Story

**As a** prospective home loan customer,  
**I want to** enter my loan amount, tenure, and interest rate and see my estimated monthly EMI plus principal/interest split,  
**So that** I can plan my cash flows before I apply for a home loan.

## Background

The portal presents a **“Calculate Your Home Loan”** area with **“Calculate monthly EMI”**, sliders/inputs for loan amount (approximately ₹1 lakh–₹10 crore), tenure (1–30 years), and interest rate (about 0.5%–15% p.a.), and shows derived values such as monthly EMI, total interest, and principal. Users can also view **amortization** / EMI breakdown visuals and use **“Apply Now”** when ready.

## Acceptance criteria

1. Given I am on the home loan landing page, when I choose **Calculate monthly EMI**, I can enter or adjust **loan amount**, **tenure (years)**, and **interest rate (% p.a.)** within the published ranges.
2. When I change any input, the system **recalculates** and displays at least: **monthly EMI**, **principal component**, **interest component** (and/or total interest), consistent with the inputs.
3. I can open **view details** / **amortization** (or equivalent) to see how EMI splits over time, without submitting a loan application.
4. A **disclaimer** is visible stating that calculators are **self-help planning tools**, results depend on assumptions, and **accuracy is not guaranteed** for my final offer (aligned with on-page copy).
5. Optional: From the calculator outcome, I can navigate to **Apply Now** (e.g. to the online application entry point) without losing context where the product allows it.

## Non-functional

- Calculator works on common desktop and mobile browsers supported by the site.
- Inputs reject or clearly message out-of-range values per UI rules.

## Out of scope (for this story)

- Credit decision, sanction amount, or final interest rate.
- Saving calculator state to logged-in profile (unless product explicitly provides it).
