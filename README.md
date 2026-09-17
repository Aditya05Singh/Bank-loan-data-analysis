# Bank Loan Lending Data Analytics

[![SQL](https://img.shields.io/badge/SQL-MySQL%208.0-blue.svg)](https://www.mysql.com/)
[![Tableau](https://img.shields.io/badge/Tableau-3%20Dashboards%20%7C%2033%20Visualizations-E97627.svg)](https://public.tableau.com/)
[![Records](https://img.shields.io/badge/Records-38%2C576%20Validated-brightgreen.svg)](data/cleaned/loan_data_cleaned.csv)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)](documentation/final_audit_report.md)

An end-to-end, enterprise-grade financial data analytics and business intelligence solution evaluating loan portfolio health, capital disbursement, borrower creditworthiness, and loss given default (LGD) for a retail commercial bank.

---

## Project Overview
This project delivers a complete financial analytics lifecycle across **38,576** consumer loan originations representing **$435.8M** in funded capital and **$473.1M** in cash collections. Utilizing **MySQL 8.0** and **Tableau**, the system models credit risk distributions, tracks Month-over-Month (MoM) origination velocity, enforces 14 automated data quality assertions, and provides executive decision-makers with a synchronized 3-dashboard reporting suite containing **33** distinct visualization areas.

---

## Business Problem
Commercial lending institutions operate in high-risk environments where uncontrolled defaults directly compress Net Interest Margins (NIM). Executive leadership (Chief Credit Officer, Chief Risk Officer, Treasury Committees) faced several operational challenges:
- **Lack of Unified Portfolio Visibility**: Fragmented loan originations and servicing data scattered across operational silos.
- **Unidentified Subprime Concentrations**: Hidden risk pockets in specific borrowing purposes (e.g. Small Business) and lower credit tiers (Grades D through G).
- **Sub-optimal Risk-Based Pricing**: Inadequate interest rate spreads failing to offset elevated default loss incidence on high-leverage borrowers.
- **Recovery Tracking Gaps**: Incomplete visibility into post-charge-off collections and net credit loss severity.

---

## Objectives
1. **Data Engineering & Standardization**: Build a reproducible Python pipeline to clean, format, and audit 38,576 raw loan contracts into a normalized MySQL schema.
2. **Data Quality Governance**: Deploy 14 deterministic SQL assertions verifying primary key uniqueness, non-negative amounts, date chronology, and domain validity.
3. **Financial KPI Measurement**: Quantify primary banking metrics including Total Applications, Capital Funded, Cash Collections, Default Rate, Recovery Rate, and Net Credit Loss.
4. **Multi-Dimensional Credit Analysis**: Evaluate portfolio allocations across credit grades (A-G), loan purposes (14 categories), customer demographics, and US geography.
5. **Interactive Executive BI Delivery**: Design a 3-dashboard Tableau suite encompassing 33 visualization areas with cross-filtering, highlight actions, and detailed ledger drill-downs.

---

## Dataset
- **Domain**: Bells Bank / LendingClub Consumer Credit Originations.
- **Record Volume**: Exactly **38,576** approved loan applications (100% verified, 0 fabricated rows).
- **Feature Dimension**: **24** business features spanning contract parameters, borrower demographics, credit grading, and payment histories.
- **Temporal Coverage**: Calendar Year 2021 (January 1, 2021 to December 31, 2021).
- **Primary Key**: `id` (100% unique, 0 duplicates).
- **Documentation**: Full column metadata available in [`documentation/data_dictionary.md`](documentation/data_dictionary.md).

---

## Data Cleaning
Executed deterministically via [`scripts/clean_data.py`](scripts/clean_data.py):
- **Date Standardization**: Parsed un-padded date formats (`%m/%d/%Y`) to ISO-8601 `YYYY-MM-DD` for native MySQL `DATE` indexing.
- **Whitespace & Format Normalization**: Stripped leading spaces from contractual terms (`' 36 months'` → `'36 months'`).
- **Categorical Standardization**: Normalized loan purposes to uniform Title Case (`'Debt Consolidation'`, `'Credit Card'`, `'Small Business'`).
- **Missing Value Handling**: Standardized 1,433 missing `emp_title` values to `'Unspecified'`. Core financial fields contained 0 NULLs.
- **Reconciliation**: 38,576 raw rows → 38,576 cleaned rows (0 valid records dropped). Full audit report in [`documentation/data_cleaning.md`](documentation/data_cleaning.md).

---

## MySQL Database
- **Database**: `bank_loan_analytics`
- **Storage Engine**: InnoDB (ACID compliant, row-level locking, foreign key support).
- **Data Types**: Strict `DECIMAL(12,2)` for monetary values, `DECIMAL(6,4)` for percentages, `DATE` for timestamps, and `VARCHAR` for categories.
- **Performance Indexes**:
  - `idx_loan_status` on `(loan_status)`
  - `idx_grade_subgrade` on `(grade, sub_grade)`
  - `idx_issue_date` on `(issue_date)`
  - `idx_purpose` on `(purpose)`
  - `idx_address_state` on `(address_state)`
  - `idx_home_ownership` on `(home_ownership)`
  - `idx_verification_status` on `(verification_status)`
  - `idx_member_id` on `(member_id)`
- **DDL & Loading Instructions**: See [`sql/01_database_setup.sql`](sql/01_database_setup.sql) and [`sql/02_schema.sql`](sql/02_schema.sql).

---

## SQL Analysis
Structured across 9 modular SQL scripts in [`sql/`](sql/):
1. **`01_database_setup.sql`**: Database creation, UTF-8 character encoding, session parameters.
2. **`02_schema.sql`**: Table DDL, column data types, constraints, indexes, bulk import syntax.
3. **`03_data_quality.sql`**: 14 automated data quality assertions.
4. **`04_kpi_analysis.sql`**: Core financial KPIs, Good vs Bad portfolio splits, MTD and MoM growth.
5. **`05_portfolio_analysis.sql`**: Allocations by status, term, grade, purpose, loan size, and states.
6. **`06_customer_analysis.sql`**: Demographics (employment tenure, income tiers, home ownership).
7. **`07_risk_analysis.sql`**: Credit risk sensitivity, default rates by tier, high-risk concentration.
8. **`08_time_series_analysis.sql`**: Monthly/quarterly cohorts, MoM velocity via `LAG()`, cumulative cash flows.
9. **`09_tableau_views.sql`**: 10 production views feeding the Tableau reporting suite.

Full technical documentation in [`documentation/sql_explanation.md`](documentation/sql_explanation.md).

---

## Tableau Dashboards
A unified 3-dashboard BI suite comprising **33 distinct visualization areas**:

### [Dashboard 1: Loan Portfolio Overview (Summary)](tableau/dashboard_1_loan_portfolio.md)
*Target: Chief Credit Officer & Treasury Committees*
1. **Total Loan Applications** (KPI Card: 38,576 | MTD: 4,314 | MoM: +6.91%)
2. **Total Funded Amount** (KPI Card: $435.8M | MTD: $54.0M | MoM: +13.04%)
3. **Total Cash Received** (KPI Card: $473.1M | MTD: $58.1M | MoM: +15.84%)
4. **Average Interest Rate** (KPI Card: 12.05% | MTD: 12.36% | MoM: +3.52%)
5. **Average Loan Amount** (KPI Card: $11,296 | Min: $500 | Max: $35,000)
6. **Default Rate** (KPI Card: 13.82% | 5,333 Charged Off Loans)
7. **Loan Status Distribution** (Multi-metric grid: Fully Paid, Current, Charged Off)
8. **Total Funded Amount by Month** (Dual-axis area and line trend)
9. **Total Loan Amount by Quarter** (Q1–Q4 capital pacing)
10. **Loan Applications by Year** (2021 annual volume summary)
11. **Total Loan Amount by State - Top 10** (Ranked state volume lead by CA, NY, TX, FL)
*(Also incorporates: Top 5 Purposes, Top 5 Grades, Loan Size Buckets, Rate Distribution, and Grade Pricing).*

### [Dashboard 2: Customer & Loan Analysis (Overview)](tableau/dashboard_2_customer_loan_analysis.md)
*Target: Retail Lending Product Managers & Underwriting Teams*
12. **Loans by Home Ownership** (Renters: 47.8%, Mortgages: 44.6%, Owners: 7.4%)
13. **Loans by Employment Length** (10+ years tenure represents largest cohort at 23.0%)
14. **Loans by Verification Status** (Verified: 35.8%, Source Verified: 27.8%, Not Verified: 36.4%)
15. **Average Loan Amount by Income Range** (Scales from $6.5k to $15.8k)
16. **Total Loan Amount by Income Range** (Capital allocation by borrower earnings)
17. **Loans by Repayment Term** (Donut: 73.2% 36-month vs 26.8% 60-month)
18. **Top 5 Purposes by Average Interest Rate** (Renewable Energy, Small Business, House)
19. **Average DTI by Income Range** (Inverse debt-burden relationship)
20. **Loan Count by Credit Grade** (Grade B highest at 11.6k loans; Grade A at 9.9k loans)
21. **Average Loan Amount by Grade** (Subprime grades command higher loan balances)
22. **Loan Count by State - Top 10** (Application volume ranking)

### [Dashboard 3: Risk Analysis (Details & Risk Matrix)](tableau/dashboard_3_risk_analysis.md)
*Target: Chief Risk Officer, Credit Risk Committee, Workout Teams*
23. **Default Rate by Loan Grade** (Monotonic rise from Grade A 5.98% to Grade G 33.78%)
24. **Default Rate by Purpose - Top 10** (Small Business highest at 27.08%)
25. **Default Rate by DTI Range** (Scales from 12.2% for DTI <10% to 16.8% for DTI >25%)
26. **Default Rate by Interest Rate Range** (Pricing tier risk sensitivity)
27. **Charged-Off Amount by Year** ($65.53M gross default principal)
28. **Recovery Rate by Year** (56.89% cash recovery rate on defaulted loans)
29. **Default Rate by Home Ownership** (Renters 14.61% vs Mortgages 12.98%)
30. **Default Rate by Employment Length** (Career tenure default curve)
31. **Default Rate by Income Range** (Under $30k: 18.25% vs $120k+: 10.42%)
32. **High-Risk Loan KPIs** (12,842 high-risk loans, $164.2M funded, 22.41% default rate)
33. **Risk Distribution & Granular Drill-Down Ledger** (Interactive multi-filter borrower audit)

---

## Key KPIs
| Financial Metric | Portfolio Total | MTD (Dec 2021) | MoM Growth | Business Interpretation |
| :--- | :--- | :--- | :--- | :--- |
| **Total Applications** | **38,576** | 4,314 | **+6.91%** | Total approved borrower contracts |
| **Total Funded Amount** | **$435,757,075** | $53,981,425 | **+13.04%** | Total principal capital disbursed |
| **Total Cash Received** | **$473,070,933** | $58,074,380 | **+15.84%** | Total cash collected from all loans |
| **Average Interest Rate**| **12.05%** | 12.36% | **+3.52%** | Mean portfolio yield / borrower rate |
| **Average Loan Amount** | **$11,296.07** | $12,513.08 | **+5.73%** | Mean principal ticket size |
| **Default Rate** | **13.82%** | — | — | 5,333 Charged Off loans / 38,576 total |
| **Gross Defaults** | **$65,532,225** | — | — | Principal capital in default |
| **Recoveries Collected**| **$37,284,763** | — | — | Cash recouped on defaulted loans |
| **Recovery Rate** | **56.89%** | — | — | Recoveries / Gross Defaults |
| **Net Credit Loss** | **$28,247,462** | — | — | Unrecovered principal loss |

---

## Business Questions
The analysis answers over 26 core banking business questions across capital allocation, product structures, borrower capacity, regional exposure, credit risk sensitivity, and loss recoveries. Detailed questions and findings are documented in [`documentation/business_questions.md`](documentation/business_questions.md).

---

## Key Insights
1. **Steady Growth Throughout 2021**: Originations expanded consistently from 2,332 applications ($25.0M funded) in January to 4,314 applications ($54.0M funded) in December, showing strong portfolio expansion.
2. **Credit Grade Monotonic Default Risk**: The observed default rate increases predictably across credit ratings (Grade A: 5.98%, B: 12.21%, C: 17.15%, D: 21.08%, E: 26.85%, F: 32.68%, G: 33.78%), confirming effective underwriting risk differentiation.
3. **Under-Priced Subprime Lending**: Grade G loans yield an average interest rate of 20.91% but suffer a 33.78% default rate, resulting in severe net capital losses after accounting for recovery lag.
4. **Small Business Volatility**: Small business loans suffer the highest default rate among all borrowing categories at 27.08%, requiring stricter debt service coverage (DSCR) underwriting.
5. **Term Structure Risk**: 60-month loans exhibit an observed default rate of 22.59%, more than double the 10.61% default rate observed on 36-month loans.
6. **Substantial Loss Recovery**: The bank successfully recouped $37.28M of the $65.53M in gross defaulted principal (56.89% recovery rate), reducing net economic credit loss to $28.25M.

---

## Project Architecture
```
Raw Data (CSV)
      ↓
Cleaning Pipeline (clean_data.py)
      ↓
Cleaned CSV (loan_data_cleaned.csv)
      ↓
MySQL Database (bank_loan_analytics)
      ↓
Data Quality Assertions (03_data_quality.sql)
      ↓
SQL Analysis & Aggregations (04 - 08 SQL)
      ↓
Analytical Views (09_tableau_views.sql)
      ↓
Tableau Visual Suite (tableau_guide.md)
      ↓
3 Dashboards (Portfolio, Customer, Risk)
      ↓
33 Visualization Areas
      ↓
Executive Business Insights & Credit Strategy
```

---

## Folder Structure
```
BANK_LOAN_LENDING_DATA_ANALYTICS/
├── data/
│   ├── raw/
│   │   └── loan_data_raw.csv               # 38,576 raw records downloaded from source
│   ├── cleaned/
│   │   └── loan_data_cleaned.csv           # Normalized, ISO-dated cleaned dataset
│   └── exports/                            # Aggregation summaries
│
├── scripts/
│   └── clean_data.py                       # Automated cleaning and validation script
│
├── sql/
│   ├── 01_database_setup.sql              # Database setup and privileges
│   ├── 02_schema.sql                      # DDL, indexes, and loading instructions
│   ├── 03_data_quality.sql                # 14 data quality checks
│   ├── 04_kpi_analysis.sql                # Core KPIs, Good vs Bad, MTD/MoM
│   ├── 05_portfolio_analysis.sql          # Portfolio breakdown queries
│   ├── 06_customer_analysis.sql           # Borrower demographics and underwriting
│   ├── 07_risk_analysis.sql               # Default rates, LGD, risk tiers
│   ├── 08_time_series_analysis.sql        # Monthly/quarterly trends and window metrics
│   └── 09_tableau_views.sql               # 10 production views for BI consumption
│
├── tableau/
│   ├── dashboard_1_loan_portfolio.md      # Blueprint: Portfolio Overview (11 areas)
│   ├── dashboard_2_customer_loan_analysis.md # Blueprint: Customer Analysis (11 areas)
│   ├── dashboard_3_risk_analysis.md       # Blueprint: Risk Analysis (11 areas)
│   ├── calculated_fields.md               # Tableau calculation formulas
│   ├── tableau_data_sources.md            # Mapping worksheets to SQL views
│   └── tableau_guide.md                   # Complete step-by-step build manual
│
├── documentation/
│   ├── project_overview.md                # High-level architecture and scope
│   ├── data_dictionary.md                 # 24-column metadata dictionary
│   ├── data_cleaning.md                   # Cleaning methodology and audits
│   ├── business_questions.md              # 26 commercial banking questions answered
│   ├── methodology.md                     # Financial formulas and accounting framework
│   ├── sql_explanation.md                 # Technical SQL manual
│   ├── tableau_guide.md                   # Tableau step-by-step reproduction guide
│   ├── interview_questions.md             # 65 interview Q&As across 10 domains
│   └── final_audit_report.md              # Technical audit and resume validation
│
├── screenshots/                           # UI layouts and wireframes
├── requirements.txt                       # Minimal dependencies (pandas, numpy)
├── .gitignore                             # Git exclusion configuration
└── README.md                              # Main project documentation
```

---

## Technologies
- **SQL / RDBMS**: MySQL 8.0+ (DDL, DML, Indexes, CTEs, Window Functions `LAG()`, `SUM() OVER()`, Views)
- **Data Engineering**: Python 3.9+ (`csv`, `datetime`, `os`, `sys`)
- **Business Intelligence**: Tableau Desktop / Tableau Public (Calculated fields, Dual-axis charts, Parameter controls, Actions)
- **Data Storage**: Comma-Separated Values (CSV), UTF-8 encoded
- **Version Control**: Git / GitHub

---

## How to Run

### 1. Data Cleaning
Ensure Python 3 is installed, then run the cleaning pipeline:
```bash
python3 scripts/clean_data.py
```
This reads `data/raw/loan_data_raw.csv` and outputs `data/cleaned/loan_data_cleaned.csv`.

### 2. MySQL Database Setup & Loading
Connect to your MySQL server:
```bash
mysql -u root -p < sql/01_database_setup.sql
mysql -u root -p bank_loan_analytics < sql/02_schema.sql
```
Load the cleaned CSV using `LOAD DATA LOCAL INFILE` or MySQL Workbench Table Import Wizard (see instructions in `sql/02_schema.sql`).

### 3. Data Quality & Analytics
Execute data quality checks and analytical queries:
```bash
mysql -u root -p bank_loan_analytics < sql/03_data_quality.sql
mysql -u root -p bank_loan_analytics < sql/04_kpi_analysis.sql
mysql -u root -p bank_loan_analytics < sql/09_tableau_views.sql
```

---

## Tableau Setup
Follow the comprehensive build guide in [`tableau/tableau_guide.md`](tableau/tableau_guide.md):
1. Connect Tableau to MySQL database `bank_loan_analytics` (or connect directly to `data/cleaned/loan_data_cleaned.csv`).
2. Add the 10 production views or the base table onto the canvas.
3. Create the calculated fields as documented in [`tableau/calculated_fields.md`](tableau/calculated_fields.md).
4. Construct the 33 worksheets following the shelf configurations in the dashboard blueprints.
5. Assemble Dashboard 1, 2, and 3 using fixed desktop containers (`1600 x 1000`).
6. Configure filter and highlight actions under **Dashboard -> Actions**.
7. Validate on-screen numbers against `sql/04_kpi_analysis.sql` baseline metrics.

---

## Limitations
- **Origination Year Restriction**: All loans originated within calendar year 2021; macroeconomic multi-year business cycle comparisons are restricted to within-year trends.
- **DTI Distribution**: The maximum recorded DTI in this dataset is 29.99%. High-risk leverage thresholds are set at `DTI >= 20.0%`.
- **Individual Borrowers**: All applications represent individual filings; co-borrower/guarantor dynamics are not captured.
- **Observational Findings**: Risk insights describe historical empirical correlations; causal inferences require controlled A/B testing or structural econometric modeling.

