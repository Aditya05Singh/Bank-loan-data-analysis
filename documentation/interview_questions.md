# 65 Comprehensive Project Interview Questions & Defensible Answers

This document provides 65 rigorous, project-specific interview questions and concise, defensible answers tailored for Senior Data Analyst, Financial Data Analyst, and Analytics Engineer roles.

---

### Part 1: Project Overview & Architecture (Questions 1–6)

1. **Can you walk me through the high-level architecture of this project?**
   - *Answer*: The project ingests 38,576 raw loan origination records from the Bells Bank / LendingClub domain, executes an automated Python cleaning pipeline (`scripts/clean_data.py`), loads into a MySQL 8.0 relational database (`bank_loan_analytics`), enforces 14 SQL data quality assertions, calculates core financial KPIs across 5 analytical SQL scripts, creates 10 production views, and delivers a 3-dashboard, 33-visualization Tableau reporting suite.

2. **Why was this specific dataset chosen?**
   - *Answer*: It represents real-world consumer credit origination data with 24 multi-dimensional features spanning loan contracts, borrower demographics, credit grading (A-G), debt leverage (DTI), and actual payment outcomes (`Fully Paid`, `Charged Off`, `Current`), providing realistic modeling of credit risk and cash recoveries.

3. **Why did you use SQL and MySQL instead of doing all calculations directly inside Tableau?**
   - *Answer*: Doing heavy transformations in SQL establishes a centralized, version-controlled single source of truth, prevents "garbage in, garbage out", improves query performance, allows automated data quality assertions, and avoids duplicating complex calculation logic across multiple Tableau workbooks.

4. **What business problem does this project solve for bank executives?**
   - *Answer*: It provides executive visibility into capital deployment ($435.8M), monitors default risk (13.82% default rate across 5,333 loans), tracks Loss Given Default ($28.2M net credit loss), and identifies high-risk borrower concentrations to optimize underwriting guidelines.

5. **Who are the primary target users of the 3 dashboards?**
   - *Answer*: Dashboard 1 targets Chief Credit Officers and Treasury Committees (portfolio health & cash collections); Dashboard 2 targets Retail Lending Product Managers and Underwriting teams (customer demographics & pricing); Dashboard 3 targets Chief Risk Officers and Workout Teams (default drivers & recovery tracking).

6. **What is the most significant strategic recommendation derived from this analysis?**
   - *Answer*: Re-underwrite or adjust risk-based pricing on Grade G and Small Business loans. Grade G loans exhibit a 33.78% default rate against a 20.91% average interest rate, and Small Business loans default at 27.08%, eroding net interest margin.

---

### Part 2: Dataset & Profiling (Questions 7–12)

7. **How many records and features are in the dataset, and what is the primary key?**
   - *Answer*: Exactly 38,576 records and 24 columns. The primary key is `id`, an integer loan application identifier verified to be 100% unique (0 duplicates).

8. **What is the date range of loan originations in this dataset?**
   - *Answer*: All 38,576 loans were originated across the 12 months of calendar year 2021 (January 1, 2021 to December 31, 2021).

9. **What are the loan statuses present, and what is their breakdown?**
   - *Answer*: `Fully Paid`: 32,145 loans (83.33%); `Charged Off`: 5,333 loans (13.82%); `Current`: 1,098 loans (2.85%).

10. **What is the range and average of loan amounts in the portfolio?**
    - *Answer*: Minimum loan amount is $500, maximum is $35,000, and the portfolio mean ticket size is $11,296.07.

11. **How is Debt-to-Income (DTI) scaled in this dataset?**
    - *Answer*: DTI is scaled as a decimal ratio between 0.0000 and 0.2999 (0.0% to 29.99%), with an average of 0.1333 (13.33%).

12. **Were there any duplicate records or multiple loans per member?**
    - *Answer*: No. Both `id` and `member_id` contain 38,576 unique values, confirming each record represents a distinct borrower and loan contract.

---

### Part 3: Data Cleaning & Transformation (Questions 13–18)

13. **How did you clean the raw dates?**
    - *Answer*: Raw dates were inconsistently formatted without zero-padding (e.g. `2/11/2021`). In Python, I parsed them via `%m/%d/%Y` and formatted them to ISO-8601 standard `YYYY-MM-DD` (`2021-02-11`), enabling native MySQL `DATE` column loading.

14. **How did you handle missing values in `emp_title`?**
    - *Answer*: 1,433 records (3.71%) lacked an employer/job title. Rather than dropping valid financial contracts, I imputed the string `'Unspecified'`, preserving all 38,576 loans without distorting financial aggregations.

15. **Were there any missing values in core financial columns?**
    - *Answer*: No. Columns such as `loan_amount`, `total_payment`, `int_rate`, `dti`, `annual_income`, and `installment` had zero NULLs or empty strings across all 38,576 rows.

16. **How did you handle the whitespace in the `term` column?**
    - *Answer*: The raw CSV had leading spaces (e.g., `' 36 months'`). I stripped leading/trailing whitespace to standardize values to `'36 months'` and `'60 months'`, allowing exact matches in SQL filters.

17. **How was loan purpose standardized?**
    - *Answer*: Raw values had mixed casing and underscores (`'Debt consolidation'`, `'renewable_energy'`). I mapped them to clean, uniform Title Case strings (`'Debt Consolidation'`, `'Renewable Energy'`).

18. **Why did you avoid replacing missing financial values with zero?**
    - *Answer*: Zero is a meaningful numeric value that drastically skews averages (`AVG()`) and distributions. Missing financial values must be investigated, handled as meaningful `NULL`s, or validated rather than fabricated.

---

### Part 4: MySQL Modeling & Database Design (Questions 19–24)

19. **Why did you choose `DECIMAL` instead of `FLOAT` or `DOUBLE` for monetary columns?**
    - *Answer*: `FLOAT` and `DOUBLE` are approximate binary floating-point types subject to rounding inaccuracies. Financial systems require fixed-point `DECIMAL` (e.g., `DECIMAL(12,2)`) to ensure exact arithmetic precision and penny-level reconciliation.

20. **What storage engine did you use in MySQL and why?**
    - *Answer*: InnoDB. It provides row-level locking, foreign key constraints, crash recovery, ACID compliance, and buffer pool optimization.

21. **Which columns did you index and what was your rationale?**
    - *Answer*: I indexed frequently filtered categorical columns (`loan_status`, `grade`, `purpose`, `home_ownership`, `address_state`, `verification_status`) and temporal fields (`issue_date`) to optimize `WHERE` clauses, join conditions, and `GROUP BY` aggregations.

22. **Why did you create a composite index on `(grade, sub_grade)`?**
    - *Answer*: Credit risk analyses frequently filter by `grade` and group by `sub_grade`. A composite index allows the query planner to satisfy both conditions in a single index scan without reading data pages.

23. **How did you load the cleaned CSV into MySQL?**
    - *Answer*: Using `LOAD DATA LOCAL INFILE` with comma delimiters, newline line terminators, and ignoring the header row. I also documented MySQL Workbench Table Data Import Wizard and Python SQLAlchemy bulk inserts as alternatives.

24. **Why create MySQL views instead of having Tableau query the raw table directly?**
    - *Answer*: Views encapsulate complex aggregations, standardize business naming, pre-calculate MTD/MoM metrics, decouple Tableau from physical table changes, and improve Tableau workbook rendering speed.

---

### Part 5: Data Quality & Integrity (Questions 25–30)

25. **What was your data quality validation strategy?**
    - *Answer*: I developed 14 deterministic SQL validation assertions in `sql/03_data_quality.sql` covering row counts, primary key uniqueness, NULL audits, non-negative constraints, rate/DTI bounds, date sequence chronology, and domain validity.

26. **What was check 10 in your data quality script?**
    - *Answer*: A date sequence chronology assertion verifying that `last_payment_date >= issue_date` for all active loans. It returned 0 violations, confirming logical servicing timestamps.

27. **How did you verify that no negative financial values existed?**
    - *Answer*: Executed checks asserting `COUNT(*) = 0` for `loan_amount <= 0`, `total_payment < 0`, and `annual_income < 0`. All returned `PASS`.

28. **How did you validate credit grade and loan term domains?**
    - *Answer*: Used `grade NOT IN ('A','B','C','D','E','F','G')` and `term NOT IN ('36 months', '60 months')` assertions. Both returned 0 invalid records.

29. **What was the biggest data quality risk identified during profiling?**
    - *Answer*: Missing job titles (`emp_title`) in 1,433 records and un-padded dates. These were resolved cleanly in Python before database loading.

30. **How would you automate these data quality checks in a production pipeline?**
    - *Answer*: By integrating them into an orchestration tool like Apache Airflow or dbt, running assertions as pre-load and post-load automated tests that fail the DAG if any assertion returns a non-zero violation count.

---

### Part 6: Financial KPIs & Accounting Definitions (Questions 31–38)

31. **What is the total funded amount vs total received amount?**
    - *Answer*: Total funded principal is $435,757,075 ($435.8M); total cash collected is $473,070,933 ($473.1M), representing a 108.56% overall cash return.

32. **How is default rate defined, and what is the denominator?**
    - *Answer*: Default Rate = `COUNT(Charged Off) / COUNT(Total Applications)`. The denominator is all originated loan applications (38,576). The observed rate is 13.82% (5,333 loans).

33. **What is the difference between Gross Charged-Off Amount and Net Credit Loss?**
    - *Answer*: Gross Charged-Off Amount is total principal disbursed to defaulted borrowers ($65,532,225). Net Credit Loss subtracts cash recovered prior to or post-charge-off ($37,284,763), resulting in a net economic credit loss of $28,247,462.

34. **How did you calculate the Recovery Rate?**
    - *Answer*: Total cash collected on Charged Off loans divided by total principal disbursed on Charged Off loans: `$37,284,763 / $65,532,225 = 56.89%`.

35. **What is the Fully Paid Rate?**
    - *Answer*: `COUNT(Fully Paid) / COUNT(Total Applications) = 32,145 / 38,576 = 83.33%`.

36. **What is the Good Loan vs Bad Loan breakdown?**
    - *Answer*: Good Loans (`Fully Paid` + `Current`) comprise 86.18% (33,243 loans, $370.2M funded). Bad Loans (`Charged Off`) comprise 13.82% (5,333 loans, $65.5M funded).

37. **What is MTD and how was it computed?**
    - *Answer*: Month-to-Date reflects performance during the latest available month in the calendar year (December 2021). December recorded 4,314 applications, $53.98M funded, and $58.07M received.

38. **How was Month-over-Month (MoM) growth calculated?**
    - *Answer*: Comparing December (Month 12) to November (Month 11): Applications grew +6.91% (4,314 vs 4,035); Funded capital grew +13.04% ($54.0M vs $47.8M); Received cash grew +15.84% ($58.1M vs $50.1M).

---

### Part 7: SQL Techniques & Query Engineering (Questions 39–45)

39. **How did you calculate Month-over-Month growth in SQL?**
    - *Answer*: Using a CTE to aggregate monthly totals, then applying the `LAG()` window function over `ORDER BY month_number` to access the prior month's metric and compute `(current - prior) / prior * 100`.

40. **How did you calculate cumulative capital disbursement across 2021?**
    - *Answer*: Using the cumulative window function `SUM(monthly_funded) OVER (ORDER BY month_number ASC)`.

41. **Why did you use `NULLIF` in recovery rate calculations?**
    - *Answer*: `NULLIF(SUM(charged_off_funded), 0)` converts a zero denominator to `NULL`, which prevents SQL runtime division-by-zero crashes if a filter isolates a segment with zero defaults.

42. **How did you identify the Top 5 loan purposes by funded amount?**
    - *Answer*: Using `DENSE_RANK() OVER (ORDER BY SUM(loan_amount) DESC)` inside a CTE, filtering for `WHERE ranking <= 5`.

43. **What is the performance advantage of conditional aggregation over multiple subqueries?**
    - *Answer*: Conditional aggregation (`SUM(CASE WHEN ... THEN ...)`) scans the underlying table once, whereas multiple scalar subqueries require repeated table scans, increasing disk I/O and query latency.

44. **What was the most complex SQL query in this project?**
    - *Answer*: The MTD and MoM comparison CTE in `04_kpi_analysis.sql` and the cumulative collection ratio window query in `08_time_series_analysis.sql`, which required self-referencing analytical functions across monthly partitions.

45. **How did you ensure chronological sorting of months?**
    - *Answer*: By grouping by and ordering by `MONTH(issue_date)` (integer 1–12) rather than `MONTHNAME(issue_date)`, which would sort alphabetically (April, August, December...).

---

### Part 8: Tableau Architecture & Visual Design (Questions 46–52)

46. **How are the 33 visualization areas distributed across the 3 dashboards?**
    - *Answer*: Dashboard 1 (Portfolio Overview) contains 11 core areas (6 KPI cards + 5 charts); Dashboard 2 (Customer & Loan Analysis) contains 11 demographic and sizing charts; Dashboard 3 (Risk Analysis) contains 11 risk ladder and loss recovery charts. Exactly 33 visualization areas in total.

47. **What visual design principles did you follow?**
    - *Answer*: Corporate financial palette (Midnight Navy `#0F2537`, clean off-white canvas `#F8FAFC`, Emerald `#10B981` for performing assets, Crimson `#DC2626` for defaults), consistent padding, KPI cards at top, filters on the left, and no visual clutter.

48. **How did you implement interactive cross-filtering in Tableau?**
    - *Answer*: Configured Dashboard Filter Actions where selecting a loan status on Dashboard 1 or a credit grade on Dashboard 3 dynamically updates all linked sheets on select.

49. **Why did you choose a dual-axis chart for monthly performance?**
    - *Answer*: An Area chart for Funded Capital combined with a solid Line chart for Cash Received enables instant visual comparison of capital disbursement versus cash inflow velocity over time.

50. **How did you ensure consistency between Tableau calculated fields and SQL views?**
    - *Answer*: Every Tableau calculated field formula was explicitly derived from the corresponding SQL `CASE` or aggregate expression (e.g. `[Default Flag]` exactly matches `CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END`).

51. **How did you validate Tableau numbers against SQL?**
    - *Answer*: Cross-checked summary cards and sheet totals in Tableau against the baseline output of `sql/04_kpi_analysis.sql` to guarantee 100% numerical reconciliation.

52. **Why use horizontal bar charts for loan purposes and states?**
    - *Answer*: Horizontal bars provide clean, readable text labels for long names (e.g., `Debt Consolidation`) without slanted or truncated labels, and facilitate intuitive top-to-bottom ranking.

---

### Part 9: Credit Risk & Sensitivity Analysis (Questions 53–58)

53. **How do default rates vary by credit grade?**
    - *Answer*: Default rates scale monotonically: Grade A = 5.98%, B = 12.21%, C = 17.15%, D = 21.08%, E = 26.85%, F = 32.68%, G = 33.78%.

54. **How did you define high-risk loans, and why?**
    - *Answer*: In this dataset, the maximum recorded DTI is 29.99%, making a `DTI > 40%` rule yield zero records. High risk was empirically defined as `DTI >= 20.0%` (top leverage quartile) OR subprime credit grade (`Grade IN ('D','E','F','G')`), isolating 12,842 loans with an observed 22.41% default rate.

55. **Does higher annual income guarantee lower default risk?**
    - *Answer*: Yes. Borrowers earning under $30,000 exhibit an observed default rate of 18.25%, whereas borrowers earning $120,000+ exhibit an observed default rate of 10.42%.

56. **What is the relationship between loan term and default risk?**
    - *Answer*: 60-month loans exhibit a default rate of ~22.6%, more than double the ~10.6% default rate observed on 36-month loans.

57. **Why do Small Business loans experience the highest default rate (27.08%)?**
    - *Answer*: Small business ventures carry inherent cash-flow volatility, higher economic sensitivity, and lack the collateral backing typical of secured commercial credit.

58. **Why did you use observational language rather than claiming causation?**
    - *Answer*: Cross-sectional observational data reveals correlations (e.g. higher DTI associates with higher default rate), but does not control for confounding variables. Claiming causation without econometric instruments is scientifically invalid.

---

### Part 10: Scalability, Optimization & Scenarios (Questions 59–65)

59. **What happens if the dataset scales from 38K to 10 million records?**
    - *Answer*: I would partition tables by `issue_date` (e.g. `PARTITION BY RANGE (YEAR(issue_date))`), migrate aggregations to pre-computed materialized summary tables, enforce clustered indexes on `(issue_date, id)`, leverage columnar storage engines (e.g. ClickHouse, BigQuery, or Amazon Redshift), and use Tableau Hyper Extracts with incremental refreshes.

60. **How would you optimize a slow-running SQL query on this table?**
    - *Answer*: Run `EXPLAIN` to inspect the execution plan, verify index usage, replace subqueries in `SELECT` with CTEs or `JOIN`s, eliminate wildcard scans, and ensure filter columns in `WHERE` are indexed and not wrapped in functions.

61. **How does this analysis support loan loss provisioning (CECL / IFRS 9)?**
    - *Answer*: It provides empirical estimates for Probability of Default (PD) across grades and Loss Given Default (LGD) through the 56.89% recovery rate, which are core parameters in Expected Credit Loss (ECL) provisioning.

62. **What would you do if a business stakeholder reported a KPI mismatch between Dashboard 1 and Dashboard 3?**
    - *Answer*: Audit global filter states (e.g., date range or status filters), verify whether calculated fields share identical formulas and data sources, and trace both back to the underlying SQL views.

63. **What additional features would you collect to improve credit risk modeling?**
    - *Answer*: FICO credit score at origination, revolving credit line utilization, revolving balance, delinquent accounts in last 2 years, loan-to-value (LTV) for secured loans, and macroeconomic variables (unemployment rate, Fed funds rate).

64. **What would you improve if given additional time?**
    - *Answer*: Implement automated dbt transformation models with CI/CD GitHub Actions testing, integrate automated anomaly detection on daily application volume, and deploy machine learning models (e.g. XGBoost / Logistic Regression) for predictive default probability scoring.

65. **Why should an employer hire you based on this project?**
    - *Answer*: This project demonstrates end-to-end analytics capability: writing production-grade, index-optimized SQL, implementing strict data engineering quality standards, deeply understanding credit risk metrics, and designing intuitive, executive-ready Tableau reporting suites grounded entirely in factual data.

