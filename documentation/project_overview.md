# Project Overview - Bank Loan Lending Data Analytics

## 1. Business Problem
Commercial and consumer retail banks face significant challenges in optimizing their lending portfolios. Key risks include:
- Uncontrolled credit default rates eroding net interest margins (NIM).
- Capital concentration in high-risk geographic regions or high-risk borrower segments.
- Sub-optimal risk-based pricing where interest rates fail to compensate for expected credit loss (ECL).
- Inefficient cash recovery workflows on charged-off assets.

To maintain regulatory compliance, manage capital adequacy ratios (CAR), and enhance profitability, executive stakeholders (Chief Credit Officer, Chief Risk Officer, Treasury Committees) require a unified, single-source-of-truth analytical dashboard system to monitor portfolio health, track origination velocity, and isolate risk drivers.

---

## 2. Project Objectives
1. **Data Ingestion & Integrity**: Process, clean, and validate 38,576 consumer loan records from raw origination extracts into an enterprise-grade MySQL relational database.
2. **Comprehensive Data Quality Framework**: Deploy 14 rigorous SQL assertions to ensure 100% data integrity before reporting.
3. **Core Financial KPI Measurement**: Calculate essential banking KPIs including Total Applications, Total Funded Capital, Total Cash Collections, Average Interest Rates, Average DTI, Default Rates, and Loss Given Default (LGD).
4. **Multi-Dimensional Portfolio Segmentation**: Evaluate loan distributions across credit grades (A-G), borrowing purposes (14 categories), customer demographics, and US geography.
5. **Interactive Executive BI Delivery**: Design a 3-dashboard Tableau suite encompassing 33 distinct visualization areas with synchronized cross-filtering, highlight actions, and drill-down capabilities.
6. **Data-Driven Strategic Recommendations**: Deliver observational credit policy insights to optimize underwriting cutoffs and loan restructuring strategies.

---

## 3. Dataset Profile
- **Entity**: Bells Bank / LendingClub consumer loan origination portfolio.
- **Total Records**: 38,576 approved loan contracts.
- **Features**: 24 distinct attributes covering loan parameters, borrower demographics, credit bureau scores, and payment histories.
- **Total Capital Funded**: $435,757,075 ($435.8M).
- **Total Cash Collected**: $473,070,933 ($473.1M).
- **Portfolio Health Split**:
  - **Good Loans (Fully Paid + Current)**: 33,243 applications (86.18%), $370.2M funded, $435.8M received.
  - **Bad Loans (Charged Off)**: 5,333 applications (13.82%), $65.5M funded, $37.3M recovered ($28.2M net credit loss).

---

## 4. End-to-End Analytical Pipeline
The project follows a structured, enterprise data analytics lifecycle:
```
Raw Public Dataset (CSV)
         ↓
Python Profiling & Cleaning Pipeline (clean_data.py)
         ↓
Standardized Clean CSV (loan_data_cleaned.csv)
         ↓
MySQL 8.0 Database (bank_loan_analytics)
         ↓
Schema & High-Performance Indexing (02_schema.sql)
         ↓
Data Quality Verification (03_data_quality.sql)
         ↓
Core Financial KPIs & Portfolio Analysis (04 - 08 SQL)
         ↓
Production Analytical Views (09_tableau_views.sql)
         ↓
Tableau BI Suite (3 Dashboards, 33 Visualization Areas)
         ↓
Executive Business Insights & Underwriting Strategy
```

---

## 5. Technology Stack
- **Database / SQL**: MySQL 8.0+ (DDL, DML, Indexes, CTEs, Window Functions `LAG()`, `SUM() OVER()`, Views).
- **Data Engineering & Automation**: Python 3 (standard libraries: `csv`, `datetime`, `os`, `sys`).
- **Data Visualization & BI**: Tableau Desktop & Tableau Public (Dual-axis charts, Geographic maps, Calculated Fields, Actions).
- **Data Storage**: Comma-Separated Values (`CSV`), UTF-8 encoded.
- **Version Control & Documentation**: Git, GitHub, Markdown.

---

## 6. Analytical Focus Areas
- **Portfolio Health & Pacing**: Month-to-Date (MTD) and Month-over-Month (MoM) loan velocity.
- **Credit Grading Matrix**: Evaluating default risk and interest rate spreads from Grade A to Grade G.
- **Demographic Underwriting**: Assessing how homeowner status, career tenure, and income brackets impact borrowing behavior.
- **Loss Given Default & Recovery**: Tracking gross defaults ($65.5M) against recoveries ($37.3M) yielding a 56.89% recovery rate.

---

## 7. Dashboards Overview
1. **Dashboard 1: Loan Portfolio Overview (Summary)**: 6 KPI cards, Good vs Bad loan portfolio split, monthly funded/received trends, quarterly pacing, and top 10 states by capital.
2. **Dashboard 2: Customer & Loan Analysis (Overview)**: Demographic breakdown by home ownership, employment length, verification status, income bands, loan terms, and borrowing purposes.
3. **Dashboard 3: Risk Analysis (Details & Risk Matrix)**: Default rate sensitivity across credit grades, loan purposes, DTI tiers, interest rate brackets, and high-risk concentration audit.

---

## 8. Limitations & Constraints
- **Origination Timeframe**: All loans originated in calendar year 2021.
- **DTI Ceiling**: The maximum observed DTI is 29.99%.
- **Single Loan per Member**: In this snapshot, each borrower has a single loan contract.
- **Observational Nature**: Findings reflect historical statistical correlations; causal relationships require controlled A/B experimentation or structural econometric modeling.

