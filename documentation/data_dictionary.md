# Bank Loan Lending Data Dictionary

This data dictionary documents every column in the 24-feature dataset (`loan_data_raw.csv` and `loan_data_cleaned.csv`).
Total Records: **38,576** | Entity: **Consumer Loan Origination Fact Table** | Primary Key: **`id`**

---

| Column Name | SQL Data Type | Measure / Dimension | Description & Purpose | Example Value | Business Meaning & Analytical Utility |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **`id`** | `INT` | Dimension (PK) | Unique identifier for each originated loan application. | `1077430` | System primary key used for counting total loan volume and ensuring record uniqueness. |
| **`address_state`** | `VARCHAR(2)` | Dimension | Two-letter US state postal abbreviation of borrower's residence. | `CA` | Used for geographic segmentation, state-level exposure limits, and regional default rates. |
| **`application_type`** | `VARCHAR(50)` | Dimension | Classification of borrower application filing. | `INDIVIDUAL` | Identifies individual vs joint obligations. (All 38,576 records in this portfolio are INDIVIDUAL). |
| **`emp_length`** | `VARCHAR(20)` | Dimension | Employment tenure of applicant at the time of origination. | `10+ years` | Proxy for job stability and income consistency; evaluates default risk across career tenure. |
| **`emp_title`** | `VARCHAR(255)` | Dimension | Stated job title or employer name of the applicant. | `Ryder` | Borrower profession metadata (3.71% unspecified; standardized during data cleaning). |
| **`grade`** | `VARCHAR(2)` | Dimension | High-level credit rating assigned by lender underwriting. | `B` | Core credit risk tier (A through G). Directly dictates interest rate pricing and risk capital. |
| **`sub_grade`** | `VARCHAR(5)` | Dimension | Granular credit sub-rating within each major credit grade. | `B2` | Finer 35-tier credit scoring ladder (A1 to G5) used for precision risk-based loan pricing. |
| **`home_ownership`** | `VARCHAR(20)` | Dimension | Residential tenure status of borrower. | `RENT` | Evaluates borrower collateral and fixed living overhead (`RENT`, `MORTGAGE`, `OWN`, `OTHER`, `NONE`). |
| **`issue_date`** | `DATE` | Dimension (Temporal) | Formal origination/funding date of the loan contract. | `2021-02-11` | Primary temporal dimension driving monthly cohorts, quarterly pacing, MTD, and MoM tracking. |
| **`last_credit_pull_date`**| `DATE` | Dimension (Temporal) | Date the credit reporting agency profile was most recently accessed. | `2021-09-13` | Credit surveillance timestamp used to audit recent credit bureau activity. |
| **`last_payment_date`** | `DATE` | Dimension (Temporal) | Date the most recent payment was recorded from the borrower. | `2021-04-13` | Operational servicing timestamp for delinquency aging and payment recency monitoring. |
| **`loan_status`** | `VARCHAR(50)` | Dimension | Operational and credit status of the loan contract. | `Fully Paid` | Key outcome variable: `Fully Paid` (settled), `Current` (performing), `Charged Off` (default/loss). |
| **`next_payment_date`** | `DATE` | Dimension (Temporal) | Next scheduled installment due date. | `2021-05-13` | Cash-flow forecasting timestamp for upcoming receivable installments. |
| **`member_id`** | `INT` | Dimension | Unique identifier assigned to the borrower customer profile. | `1314167` | Customer-level foreign key; enables customer relationship and repeat borrower analysis. |
| **`purpose`** | `VARCHAR(50)` | Dimension | Primary stated objective/category for loan proceeds. | `Debt Consolidation` | Segment classification (14 categories) used for underwriting risk appetite and marketing. |
| **`term`** | `VARCHAR(20)` | Dimension | Contractual repayment duration in months. | `36 months` | Structural contract duration (`36 months` vs `60 months`), influencing amortization and pricing. |
| **`verification_status`**| `VARCHAR(50)` | Dimension | Level of income and asset verification performed by underwriting. | `Source Verified` | Underwriting control measure: `Verified`, `Source Verified`, or `Not Verified`. |
| **`annual_income`** | `DECIMAL(12,2)` | Measure | Self-reported annual gross income in USD. | `65000.00` | Baseline measure of borrower repayment capacity and debt-service ability. |
| **`dti`** | `DECIMAL(6,4)` | Measure | Debt-to-Income ratio (monthly non-mortgage debt / gross income). | `0.1330` | Core leverage metric. (Expressed as decimal: 0.1330 = 13.30%; max in dataset is 0.2999). |
| **`installment`** | `DECIMAL(10,2)` | Measure | Contractual monthly payment amount owed in USD. | `326.86` | Recurring cash commitment owed by borrower each billing cycle. |
| **`int_rate`** | `DECIMAL(6,4)` | Measure | Contractual annual interest rate expressed as a decimal. | `0.1205` | Pricing yield measure (e.g. 0.1205 = 12.05%). Reflects lender return and risk premium. |
| **`loan_amount`** | `DECIMAL(12,2)` | Measure | Principal capital disbursed to the applicant at origination. | `12000.00` | Core portfolio size measure (Funded Amount). Total portfolio volume = $435,757,075. |
| **`total_acc`** | `INT` | Measure | Total number of credit lines ever opened on applicant profile. | `22` | Depth of credit experience and past credit market participation. |
| **`total_payment`** | `DECIMAL(12,2)` | Measure | Cumulative cash collected to date (principal + interest + fees). | `14120.50` | Cash inflow metric. Used to calculate Net Default Loss and Loss Recovery Rates. |

