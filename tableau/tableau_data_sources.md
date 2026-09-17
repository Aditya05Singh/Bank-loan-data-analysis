# Tableau Data Sources Mapping

This document details the exact mapping between MySQL views/tables in the `bank_loan_analytics` database and each visualization sheet across the 3 Tableau dashboards.

---

## 1. Data Source Architecture Overview
Tableau connects to MySQL using the native MySQL connector or via cleaned CSV exports.
The analytical data architecture is divided into two primary connection patterns:
1. **Aggregated Analytical Views**: Pre-aggregated, high-performance views for executive KPI cards, monthly trends, and state choropleths.
2. **Granular Fact Table (`loan_data`)**: Used for multi-dimensional cross-filtering, interactive ledger drill-downs, and customer demographics.

---

## 2. Dashboard 1: Loan Portfolio Overview (11 Areas)

| Visualization Area | Worksheet Name | Primary Source | Granularity | Key Metrics / Columns |
| :--- | :--- | :--- | :--- | :--- |
| **Area 1: Total Loan Applications** | `kpi_total_applications` | `vw_loan_kpis` | Portfolio Single-Row | `total_loan_applications`, `mtd_applications` |
| **Area 2: Total Funded Amount** | `kpi_total_funded` | `vw_loan_kpis` | Portfolio Single-Row | `total_funded_amount`, `mtd_funded_amount` |
| **Area 3: Total Received Amount** | `kpi_total_received` | `vw_loan_kpis` | Portfolio Single-Row | `total_received_amount`, `mtd_received_amount` |
| **Area 4: Average Interest Rate** | `kpi_avg_int_rate` | `vw_loan_kpis` | Portfolio Single-Row | `avg_interest_rate_pct`, `mtd_avg_int_rate_pct` |
| **Area 5: Average Loan Amount** | `kpi_avg_loan_amount` | `vw_loan_kpis` | Portfolio Single-Row | `avg_loan_amount` |
| **Area 6: Default / Charged-Off Rate** | `kpi_default_rate` | `vw_loan_kpis` | Portfolio Single-Row | `bad_loan_pct`, `bad_loan_applications` |
| **Area 7: Loan Status Distribution** | `viz_loan_status_distribution` | `vw_loan_status_distribution` | By Loan Status | `loan_status`, `total_applications`, `total_funded_amount`, `total_received_amount` |
| **Area 8: Funded Amount by Month** | `viz_monthly_funded_trend` | `vw_monthly_loan_summary` | By Month (1-12) | `month_number`, `total_funded_amount`, `total_received_amount` |
| **Area 9: Loan Amount by Quarter** | `viz_quarterly_funded` | `vw_monthly_loan_summary` | By Quarter (Q1-Q4) | `issue_quarter`, `total_funded_amount` |
| **Area 10: Applications by Year** | `viz_applications_by_year` | `vw_monthly_loan_summary` | By Year (2021) | `issue_year`, `total_applications` |
| **Area 11: Top 10 States by Funded Amount** | `viz_top10_states_funded` | `vw_state_analysis` | By US State Code | `state_code`, `total_funded_amount`, `total_applications` |

---

## 3. Dashboard 2: Customer & Loan Analysis (11 Areas)

| Visualization Area | Worksheet Name | Primary Source | Granularity | Key Metrics / Columns |
| :--- | :--- | :--- | :--- | :--- |
| **Area 1: Loans by Home Ownership** | `viz_cust_home_ownership` | `vw_customer_analysis` | By Home Ownership | `home_ownership`, `COUNT(loan_id)`, `SUM(loan_amount)` |
| **Area 2: Loans by Employment Length** | `viz_cust_emp_length` | `vw_customer_analysis` | By Employment Tenure | `emp_length`, `COUNT(loan_id)`, `default_rate_pct` |
| **Area 3: Loans by Verification Status** | `viz_cust_verification_status` | `vw_customer_analysis` | By Verification Status | `verification_status`, `COUNT(loan_id)`, `avg_annual_income` |
| **Area 4: Avg Loan by Income Range** | `viz_avg_loan_by_income` | `vw_income_analysis` | By Income Tier | `income_bracket`, `avg_loan_amount` |
| **Area 5: Total Loan by Income Range** | `viz_total_loan_by_income` | `vw_income_analysis` | By Income Tier | `income_bracket`, `total_funded_amount` |
| **Area 6: Loans by Repayment Term** | `viz_cust_term_split` | `vw_customer_analysis` | By Term (36 vs 60 mos) | `term`, `COUNT(loan_id)`, `SUM(loan_amount)` |
| **Area 7: Top 5 Purposes by Avg Interest** | `viz_top5_purposes_by_rate` | `vw_purpose_analysis` | By Purpose | `purpose`, `avg_interest_rate_pct` |
| **Area 8: Avg DTI by Income Range** | `viz_avg_dti_by_income` | `vw_income_analysis` | By Income Tier | `income_bracket`, `avg_dti_pct` |
| **Area 9: Loan Count by Grade** | `viz_loan_count_by_grade` | `vw_grade_analysis` | By Grade (A-G) | `grade`, `total_loans` |
| **Area 10: Avg Loan Amount by Grade** | `viz_avg_loan_by_grade` | `vw_grade_analysis` | By Grade (A-G) | `grade`, `avg_loan_amount` |
| **Area 11: Top 10 States by Loan Count** | `viz_top10_states_count` | `vw_state_analysis` | By US State Code | `state_code`, `total_applications` |

---

## 4. Dashboard 3: Risk Analysis (11 Areas)

| Visualization Area | Worksheet Name | Primary Source | Granularity | Key Metrics / Columns |
| :--- | :--- | :--- | :--- | :--- |
| **Area 1: Default Rate by Grade** | `viz_risk_default_rate_by_grade` | `vw_grade_analysis` | By Grade (A-G) | `grade`, `default_rate_pct`, `default_count` |
| **Area 2: Default Rate by Purpose** | `viz_risk_default_by_purpose` | `vw_purpose_analysis` | By Purpose | `purpose`, `default_rate_pct`, `default_count` |
| **Area 3: Default Rate by DTI Range** | `viz_risk_default_by_dti` | `vw_risk_analysis` | By DTI Tier | `dti_range`, `is_default`, `COUNT(loan_id)` |
| **Area 4: Default Rate by Interest Rate** | `viz_risk_default_by_int_rate` | `vw_risk_analysis` | By Rate Tier | `interest_rate_bracket`, `is_default` |
| **Area 5: Charged-Off Amount by Year** | `viz_risk_charged_off_by_year` | `vw_recovery_analysis` | By Year (2021) | `issue_year`, `gross_charged_off_amount` |
| **Area 6: Recovery Rate by Year** | `viz_risk_recovery_rate_by_year` | `vw_recovery_analysis` | By Year (2021) | `issue_year`, `recovery_rate_pct`, `total_recoveries_received` |
| **Area 7: Default Rate by Home Ownership** | `viz_risk_default_by_home` | `vw_customer_analysis` | By Home Ownership | `home_ownership`, `is_default`, `loan_id` |
| **Area 8: Default Rate by Emp Length** | `viz_risk_default_by_emp_length` | `vw_customer_analysis` | By Employment Tenure | `emp_length`, `is_default`, `loan_id` |
| **Area 9: Default Rate by Income Range** | `viz_risk_default_by_income` | `vw_income_analysis` | By Income Tier | `income_bracket`, `default_rate_pct` |
| **Area 10: High-Risk Loan KPIs** | `kpi_high_risk_summary` | `vw_risk_analysis` | High-Risk Subset | `risk_segment`, `high_risk_count`, `high_risk_funded`, `high_risk_default_rate` |
| **Area 11: Risk Distribution & Ledger** | `viz_risk_segment_distribution` | `vw_risk_analysis` | Granular Loan Level | `loan_id`, `grade`, `purpose`, `dti`, `loan_status`, `net_loss_amount` |

