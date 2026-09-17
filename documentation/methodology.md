# Project Methodology & Financial Framework

This document details the analytical, mathematical, and architectural methodology underpinning the Bank Loan Lending Data Analytics project.

---

## 1. Data Ingestion & Transformation Methodology
1. **Raw Source Auditing**:
   - Ingested 38,576 records from the public Bells Bank / LendingClub domain (`loan_data_raw.csv`).
   - Profiled column distributions, null frequencies, and primary key candidate uniqueness.
2. **Deterministic Cleaning Pipeline**:
   - Automated via `scripts/clean_data.py`.
   - ISO-8601 date parsing (`YYYY-MM-DD`).
   - Whitespace stripping on contractual terms (`'36 months'`, `'60 months'`).
   - Purpose categorization normalized to clean Title Case.
   - Preserved all 38,576 records (0 dropped) to maintain complete portfolio reconciliation.

---

## 2. Core Financial Accounting Definitions

### 2.1 Loan Amount & Funded Amount
- **Definition**: The principal balance disbursed by the lender to the borrower at origination.
- **SQL Representation**: `loan_amount` (DECIMAL(12,2)).
- **Portfolio Total**: $435,757,075 ($435.8M).

### 2.2 Total Payment & Cash Received
- **Definition**: The cumulative cash inflow collected by the bank from the borrower, comprising principal amortization, interest payments, late charges, and post-delinquency recoveries.
- **SQL Representation**: `total_payment` (DECIMAL(12,2)).
- **Portfolio Total**: $473,070,933 ($473.1M).

### 2.3 Loan Performance Status & Default Definition
Loans are partitioned into two operational segments:
1. **Good Loans (Performing / Settled)**:
   - `Fully Paid`: All contractual principal and interest satisfied. (32,145 loans; 83.33%).
   - `Current`: Obligation actively paying on schedule within the contractual grace period. (1,098 loans; 2.85%).
   - **Combined Good Loans**: 33,243 loans (86.18%), representing $370,224,850 funded and $435,786,170 received.
2. **Bad Loans (Defaulted / Written-Off)**:
   - `Charged Off`: Severe delinquency where the lender considers debt collection unfeasible and writes off the balance as an accounting credit loss. (5,333 loans; 13.82%).
   - **Default Rate Formula**:
     $$\text{Default Rate} = \frac{\text{Count}(\text{Charged Off})}{\text{Total Applications}} = \frac{5,333}{38,576} = 13.82\%$$

### 2.4 Loss Given Default (LGD) & Recovery Rate
- **Gross Charged-Off Capital**: The total principal disbursed to borrowers who subsequently defaulted.
  $$\text{Gross Default Funded} = \sum_{\text{Charged Off}} \text{loan\_amount} = \$65,532,225$$
- **Recoveries Received**: Total cash collected from defaulted loans (via collections, repayments prior to charge-off, or recovery sales).
  $$\text{Recoveries} = \sum_{\text{Charged Off}} \text{total\_payment} = \$37,284,763$$
- **Recovery Rate**:
  $$\text{Recovery Rate} = \frac{\text{Recoveries}}{\text{Gross Default Funded}} = \frac{\$37,284,763}{\$65,532,225} = 56.89\%$$
- **Net Credit Loss**:
  $$\text{Net Credit Loss} = \text{Gross Default Funded} - \text{Recoveries} = \$65,532,225 - \$37,284,763 = \$28,247,462$$

### 2.5 Debt-to-Income (DTI) Ratio & Empirical High-Risk Threshold
- In consumer banking, DTI represents the monthly debt service obligations divided by gross monthly income.
- **Dataset Scale**: Stored as a decimal ratio between `0.0000` and `0.2999` (0.0% to 29.99%).
- **High-Risk Threshold**: Because the maximum DTI in this actual dataset is 29.99%, setting a filter of `DTI > 40%` yields 0 records. High risk is empirically defined as:
  $$\text{High Risk} = (\text{DTI} \ge 20.0\%) \lor (\text{Grade} \in \{\text{'D'}, \text{'E'}, \text{'F'}, \text{'G'}\})$$
  This captures 12,842 loans (~33.3% of the portfolio) experiencing an observed default rate of 22.41%.

### 2.6 Month-to-Date (MTD) & Month-over-Month (MoM) Growth
- In calendar year 2021, Month 12 (December) serves as the reporting Month-to-Date (MTD) period, and Month 11 (November) serves as the Previous Month-to-Date (PMTD) baseline.
$$\text{MoM Growth} = \frac{\text{MTD}_{\text{Dec}} - \text{PMTD}_{\text{Nov}}}{\text{PMTD}_{\text{Nov}}} \times 100$$
- Applications grew +6.91% (4,035 to 4,314).
- Funded capital grew +13.04% ($47,754,825 to $53,981,425).
- Cash collections grew +15.84% ($50,132,030 to $58,074,380).

---

## 3. Database Modeling & Indexing Strategy
- **Engine**: MySQL InnoDB for ACID transactions and row-level locking.
- **Precision**: `DECIMAL(12,2)` avoids floating-point inaccuracies in currency calculations; `DECIMAL(6,4)` preserves 4 decimal places for rates.
- **Performance Indexes**:
  - Filter columns (`loan_status`, `grade`, `purpose`, `home_ownership`) indexed with B-Tree indexes for fast `WHERE` clauses.
  - Temporal indexing (`issue_date`) supports range scans and chronological grouping without full table scans.
- **Decoupled Analytical Views**: 10 analytical views isolate complex business logic from presentation layers, allowing Tableau to execute clean queries without recalculating CTEs on every drag-and-drop.

