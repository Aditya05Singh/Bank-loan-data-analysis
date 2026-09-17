# Comprehensive SQL Engineering Manual

This technical manual details every SQL technique, clause, function, and design pattern implemented across the 9 SQL scripts in `sql/`.

---

## 1. DDL & Data Modeling Techniques

### `CREATE DATABASE` & Character Encoding
- **Implementation**: `01_database_setup.sql`
- **Technique**: Sets `DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci` to guarantee complete Unicode support for international borrower names, employer strings, and text characters without truncation.

### Strict Data Typing (`DECIMAL`, `DATE`, `INT`)
- **Implementation**: `02_schema.sql`
- **Technique**: Avoids imprecise `FLOAT` or `DOUBLE` types for financial calculations. Uses `DECIMAL(12,2)` for monetary values (`loan_amount`, `total_payment`, `annual_income`) and `DECIMAL(6,4)` for percentages (`int_rate`, `dti`). Dates use native `DATE` format (`YYYY-MM-DD`).

### High-Performance B-Tree Indexes
- **Implementation**: `02_schema.sql`
- **Technique**:
  - Single-column indexes (`idx_loan_status`, `idx_issue_date`, `idx_purpose`, `idx_address_state`, `idx_home_ownership`, `idx_verification_status`).
  - Composite index (`idx_grade_subgrade` on `(grade, sub_grade)`) to optimize hierarchical credit rating lookups and group-by operations.

---

## 2. Filtering & Conditional Logic

### `WHERE` Filtering
- **Implementation**: `03_data_quality.sql`, `04_kpi_analysis.sql`, `07_risk_analysis.sql`
- **Technique**: Filters subsets such as `WHERE loan_status = 'Charged Off'` or `WHERE issue_date BETWEEN '2021-01-01' AND '2021-12-31'`.

### Conditional Aggregation with `CASE WHEN`
- **Implementation**: Across all scripts (`03_data_quality.sql` through `09_tableau_views.sql`)
- **Technique**: Used inside aggregate functions to compute cohort metrics in a single pass over the table:
  ```sql
  SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS charged_off_funded_amount
  COUNT(CASE WHEN loan_status = 'Fully Paid' THEN 1 END) AS fully_paid_count
  ```

### Binning & Bucket Categorization with `CASE`
- **Implementation**: `05_portfolio_analysis.sql`, `06_customer_analysis.sql`, `07_risk_analysis.sql`
- **Technique**: Transforms continuous measures into discrete business tiers:
  - Loan Amount Bins: `<$5k`, `$5k-$10k`, `$10k-$15k`, `$15k-$20k`, `$20k-$25k`, `>=$25k`.
  - Income Tiers: `Under $30,000`, `$30k-$60k`, `$60k-$90k`, `$90k-$120k`, `$120k+`.
  - DTI Ranges: `<10%`, `10-15%`, `15-20%`, `20-25%`, `>=25%`.

---

## 3. Aggregations & Grouping

### Aggregate Functions (`COUNT`, `COUNT DISTINCT`, `SUM`, `AVG`, `MIN`, `MAX`)
- **Implementation**: Across all analytical scripts.
- **Examples**:
  - `COUNT(id)`: Evaluates total loan volume.
  - `COUNT(DISTINCT id)`: Confirms uniqueness in data quality assertion 2.
  - `SUM(loan_amount)`: Calculates total funded principal capital.
  - `AVG(int_rate)`: Calculates mean borrower interest rate.
  - `MIN(loan_amount)`, `MAX(loan_amount)`: Determines capital ticket range.

### Null & Division Safety (`NULLIF`)
- **Implementation**: `04_kpi_analysis.sql`, `07_risk_analysis.sql`, `08_time_series_analysis.sql`
- **Technique**: Prevents fatal runtime `DIVISION BY ZERO` errors when computing recovery rates:
  ```sql
  ROUND(
      SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) * 100.0 /
      NULLIF(SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END), 0),
      2
  ) AS recovery_rate_pct
  ```

### `GROUP BY` & `ORDER BY`
- **Implementation**: All analytical scripts.
- **Technique**: Groups rows by discrete dimensions (`grade`, `purpose`, `home_ownership`, `address_state`, `MONTH(issue_date)`), sorting results by volume or default rate descending (`ORDER BY total_funded_amount DESC`).

---

## 4. Date Functions & Chronological Formatting
- **Implementation**: `05_portfolio_analysis.sql`, `08_time_series_analysis.sql`, `09_tableau_views.sql`
- **Functions Used**:
  - `MONTH(issue_date)`: Extracts integer month (1 to 12) for chronological ordering.
  - `MONTHNAME(issue_date)`: Returns English month name (`January`, `February`, etc.) for visual labels.
  - `QUARTER(issue_date)`: Extracts financial quarter (1, 2, 3, 4).
  - `YEAR(issue_date)`: Extracts calendar year (`2021`).
  - `DATE_FORMAT(issue_date, '%Y-%m')`: Creates formatted year-month string (`'2021-01'`) for time-series axis keys.

---

## 5. Advanced SQL: CTEs, Subqueries, & Window Functions

### Common Table Expressions (CTEs)
- **Implementation**: `04_kpi_analysis.sql`, `05_portfolio_analysis.sql`, `08_time_series_analysis.sql`
- **Technique**: Encapsulates intermediate aggregations into clean, readable logical blocks before joining or applying analytical functions:
  ```sql
  WITH monthly_cohorts AS (
      SELECT 
          MONTH(issue_date) AS issue_month,
          COUNT(id) AS monthly_applications,
          SUM(loan_amount) AS monthly_funded
      FROM loan_data
      GROUP BY MONTH(issue_date)
  )
  SELECT ... FROM monthly_cohorts;
  ```

### Window Function: Month-over-Month Growth with `LAG()`
- **Implementation**: `08_time_series_analysis.sql`
- **Technique**: Accesses preceding row values without self-joins to compute MoM velocity:
  ```sql
  LAG(applications, 1) OVER (ORDER BY month_num) AS prev_month_applications,
  ROUND(
      (applications - LAG(applications, 1) OVER (ORDER BY month_num)) * 100.0 / 
      LAG(applications, 1) OVER (ORDER BY month_num), 
      2
  ) AS mom_applications_growth_pct
  ```

### Window Function: Running Totals with `SUM() OVER ()`
- **Implementation**: `05_portfolio_analysis.sql`, `08_time_series_analysis.sql`
- **Technique**: Computes cumulative loan disbursement and collections over time:
  ```sql
  SUM(monthly_funded) OVER (ORDER BY month_num) AS cumulative_funded_amount
  ```
- Also used for calculating percentage of total portfolio without separate scalar queries:
  ```sql
  ROUND(SUM(loan_amount) * 100.0 / SUM(SUM(loan_amount)) OVER (), 2) AS pct_of_total_funded
  ```

### Window Function: Ranking with `DENSE_RANK()`
- **Implementation**: `05_portfolio_analysis.sql`
- **Technique**: Ranks loan purposes by funded volume:
  ```sql
  DENSE_RANK() OVER (ORDER BY SUM(loan_amount) DESC) AS ranking
  ```

---

## 6. Analytical MySQL Views
- **Implementation**: `09_tableau_views.sql`
- **Technique**: Exposes 10 pre-aggregated views (`vw_loan_kpis`, `vw_monthly_loan_summary`, `vw_loan_status_distribution`, `vw_grade_analysis`, `vw_purpose_analysis`, `vw_customer_analysis`, `vw_risk_analysis`, `vw_state_analysis`, `vw_income_analysis`, `vw_recovery_analysis`).
- **Benefit**: Decouples presentation layers, accelerates BI queries, and guarantees consistent KPI logic across all dashboards.

