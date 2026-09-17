# Data Cleaning & Transformation Report

## 1. Executive Summary
This document outlines the end-to-end data cleaning, standardization, and quality assurance process applied to the raw Bank Loan Lending dataset (`data/raw/loan_data_raw.csv`) to produce the analysis-ready dataset (`data/cleaned/loan_data_cleaned.csv`).

The cleaning pipeline is fully automated and reproducible via the Python script [`scripts/clean_data.py`](file:///Users/dineshkumarsingh/Documents/antigravity/goofy-mendeleev/BANK_LOAN_LENDING_DATA_ANALYTICS/scripts/clean_data.py).

---

## 2. Audit Metrics & Record Counts

| Metric | Pre-Cleaning Count | Post-Cleaning Count | Variance | Notes / Rationale |
| :--- | :--- | :--- | :--- | :--- |
| **Total Rows** | 38,576 | 38,576 | 0 | 100% of rows contained valid IDs, amounts, and dates. |
| **Total Columns** | 24 | 24 | 0 | All 24 business columns retained; no empty columns existed. |
| **Duplicate Records** | 0 | 0 | 0 | `id` and `member_id` are strictly unique across all rows. |
| **Invalid Records Removed**| 0 | 0 | 0 | Zero rows failed fundamental financial sanity bounds. |
| **Missing Financial Values**| 0 | 0 | 0 | No NULLs existed in `loan_amount`, `int_rate`, `dti`, etc. |
| **Standardized Text Nulls** | 1,433 | 0 | -1,433 | 1,433 missing `emp_title` values filled with `'Unspecified'`. |

---

## 3. Transformations Applied

### 3.1 Date Standardization
- **Raw Issue**: Date columns (`issue_date`, `last_credit_pull_date`, `last_payment_date`, `next_payment_date`) were formatted inconsistently as non-padded month strings (e.g. `2/11/2021`, `1/1/2021`).
- **Transformation**: Parsed using `%m/%d/%Y` and formatted into ISO-8601 standard `YYYY-MM-DD` (e.g., `2021-02-11`, `2021-01-01`).
- **Benefit**: Ensures direct compatibility with MySQL `DATE` columns, facilitates index seeks, and guarantees chronological sorting in Tableau.

### 3.2 Whitespace Stripping & Categorical Normalization
- **Term Standardization**: The raw `term` field contained leading whitespace (e.g. `' 36 months'`). Stripped to `'36 months'` and `'60 months'`.
- **Purpose Standardization**: The raw `purpose` field contained mixed casing and underscores (e.g. `'Debt consolidation'`, `'renewable_energy'`, `'credit card'`). Standardized to clean Title Case: `'Debt Consolidation'`, `'Credit Card'`, `'Home Improvement'`, `'Renewable Energy'`, etc.
- **State Codes & Application Type**: Converted to standardized uppercase (`'CA'`, `'NY'`, `'INDIVIDUAL'`).

### 3.3 Employment Title Imputation
- **Raw Issue**: 1,433 records (3.71%) lacked an applicant job title (`emp_title`).
- **Transformation**: Imputed with `'Unspecified'` to preserve meaningful borrower records without dropping valid loans or corrupting aggregations.

### 3.4 Decimal Precision & Numeric Types
- Financial figures (`loan_amount`, `total_payment`, `annual_income`, `installment`) rounded and formatted to 2 decimal places (`DECIMAL(12,2)`).
- Rate figures (`int_rate`, `dti`) rounded and formatted to 4 decimal places (`DECIMAL(6,4)`).

---

## 4. Range & Sanity Validation Checks

All 38,576 records were verified against strict domain logic:
1. **Loan Amount**: `loan_amount > 0` (Observed range: $500 to $35,000; avg: $11,296.07).
2. **Total Payment**: `total_payment >= 0` (Observed range: $34.00 to $58,564.00; avg: $12,263.35).
3. **Annual Income**: `annual_income > 0` (Observed range: $4,000 to $6,000,000; avg: $69,644.54).
4. **Interest Rate**: `0.01 <= int_rate <= 0.40` (Observed range: 5.42% to 24.59%; avg: 12.05%).
5. **Debt-to-Income (DTI)**: `0.00 <= dti <= 1.00` (Observed range: 0.00% to 29.99%; avg: 13.33%).
6. **Date Chronology**: Ensured `issue_date <= last_payment_date` across all active contracts.

---

## 5. Dataset Limitations

1. **Origination Year Restriction**: All 38,576 loans in this dataset were originated in calendar year 2021. Long-term multi-year macro-economic cycle tracking is limited to within-year seasonality and multi-year repayment histories.
2. **DTI Truncation / Upper Bound**: In this dataset, the maximum recorded DTI is 0.2999 (29.99%). Analyses referencing DTI > 40% yield 0 records; empirical thresholds are adjusted to `DTI >= 20.0%` for risk segmentation.
3. **Individual Applications Only**: All records represent `INDIVIDUAL` applications; joint application dynamics cannot be evaluated.
4. **Self-Reported Income**: Borrower annual income is self-reported, although 35.8% were fully verified and 27.8% source-verified by underwriting.

