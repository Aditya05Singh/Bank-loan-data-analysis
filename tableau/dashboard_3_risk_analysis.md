# DASHBOARD 3 - RISK ANALYSIS

## 1. Executive Summary & Dashboard Architecture
**Dashboard Title**: `DASHBOARD 3 - RISK ANALYSIS`  
**Primary Analytical Role**: Credit risk surveillance, loss given default (LGD) tracking, default driver sensitivity analysis across risk cohorts, and subprime loan exposure monitoring.  
**Target Audience**: Chief Risk Officer (CRO), Credit Risk Committees, Loan Workout & Special Assets Teams, Underwriting Policy Analysts.  
**Data Sources**: MySQL Database `bank_loan_analytics` -> Views `vw_risk_analysis`, `vw_recovery_analysis`, `vw_grade_analysis`, `vw_income_analysis`, and base table `loan_data`.

---

## 2. Canvas & Layout Container Specifications
- **Dashboard Dimensions**: Fixed Desktop Browser (`1600px` width × `1050px` height) or Automatic Responsive.
- **Color Palette & Theme**:
  - **Header / Corporate Accent**: Midnight Navy Blue (`#0F2537`)
  - **Canvas Background**: Light Risk Surveillance Gray (`#F8FAFC`)
  - **Low Risk / Safe Tier Accent**: Emerald Green (`#10B981`)
  - **Moderate Risk Tier Accent**: Amber Orange (`#F59E0B`)
  - **High Risk / Default Accent**: Crimson Coral (`#DC2626`)
  - **Loss Recovery Accent**: Slate Purple (`#7C3AED`)
- **Container Structure**:
  - **Top Horizontal Banner (`Height: 80px`)**: Dashboard Title, Last Refresh Timestamp, Navigation Controls.
  - **Upper Row (`Height: 110px`)**: High-Risk KPI Summary Cards (Area 10: Total High-Risk Loans, High-Risk Funded Amount, High-Risk Default Rate).
  - **Middle Row (`Height: 380px`)**:
    - Left Column (`Width: 35%`): Area 1 (Default Rate by Grade & Sub-Grade Risk Ladder).
    - Center Column (`Width: 35%`): Area 2 (Default Rate by Purpose - Top 10).
    - Right Column (`Width: 30%`): Area 3 & 4 (Default Rate by DTI Range & Interest Rate Range).
  - **Bottom Row (`Height: 400px`)**:
    - Left Column (`Width: 25%`): Area 5 & 6 (Charged-Off Amount & Recovery Rate by Year).
    - Center Column (`Width: 40%`): Area 7, 8 & 9 (Default Rate by Home Ownership, Employment Length, and Income Range).
    - Right Column (`Width: 35%`): Area 11 (Empirical Risk Segment Distribution & Ledger Grid).

---

## 3. Global Filters Configuration
1. **Origination Date Range**: Continuous Slider on `issue_date` (`2021-01-01` to `2021-12-31`).
2. **Credit Grade**: Multi-select Dropdown (`[All]`, `A`, `B`, `C`, `D`, `E`, `F`, `G`).
3. **Loan Purpose**: Multi-select Dropdown (`[All]`, 14 standard loan purposes).
4. **Home Ownership**: Multi-select Dropdown (`[All]`, `MORTGAGE`, `RENT`, `OWN`, `OTHER`, `NONE`).

---

## 4. Worksheets & Shelf Configurations (11 Core Visualization Areas)

### Area 1: Default Rate by Loan Grade
- **Sheet Name**: `viz_risk_default_rate_by_grade`
- **Data Source**: `vw_grade_analysis`
- **Columns**: `[grade]` (`A`, `B`, `C`, `D`, `E`, `F`, `G`)
- **Rows**: `[default_rate_pct]`
- **Marks**: Bar Chart with Step/Trend Line
- **Color Mark**: Color gradient based on `[default_rate_pct]` (Green `#10B981` for Grade A ~5.98% through Deep Red `#DC2626` for Grade G ~33.78%).
- **Labels**: Percentage format `0.0%`.
- **Key Observation**: The observed default rate exhibits a strong monotonic increase across risk grades, moving from ~6.0% in Grade A to ~33.8% in Grade G.
- **Tooltip**:  
  `Grade: <grade>`  
  `Default Rate: <default_rate_pct>%`  
  `Charged Off Count: <default_count> / <total_loans>`  
  `Funded Capital at Risk: $<total_funded_amount>`

### Area 2: Default Rate by Purpose - Top 10
- **Sheet Name**: `viz_risk_default_by_purpose`
- **Data Source**: `vw_purpose_analysis`
- **Columns**: `[default_rate_pct]`
- **Rows**: `[purpose]`
- **Marks**: Horizontal Bar Chart, Color `#DC2626`
- **Sorting**: Descending by `default_rate_pct`.
- **Top N Filter**: Top 10 Loan Purposes by Volume.
- **Key Observation**: Small business loans display the highest observed default rate (~27.1%), while major purchase and car loans demonstrate the lowest observed default rates (~10.3% and ~10.7%).
- **Labels**: Percentage `0.0%`.
- **Tooltip**:  
  `Purpose: <purpose>`  
  `Observed Default Rate: <default_rate_pct>%`  
  `Total Loans: <total_loans>`  
  `Charged-Off Count: <default_count>`

### Area 3: Default Rate by Debt-to-Income (DTI) Range
- **Sheet Name**: `viz_risk_default_by_dti`
- **Data Source**: `vw_risk_analysis`
- **Columns**: `[dti_range]` (`< 10%`, `10% - 14.99%`, `15% - 19.99%`, `20% - 24.99%`, `25% - 29.99%`)
- **Rows**: `AVG([is_default]) * 100`
- **Marks**: Column Bar Chart, Color `#F59E0B`
- **Sorting**: Ascending by DTI bracket.
- **Key Observation**: Observed default rate increases from ~12.2% for DTI under 10% to ~16.8% for DTI exceeding 25%.
- **Labels**: Percentage `0.0%`.
- **Tooltip**:  
  `DTI Bracket: <dti_range>`  
  `Default Rate: <AVG(is_default)*100>%`  
  `Total Loans in Bracket: <COUNT(loan_id)>`

### Area 4: Default Rate by Interest Rate Range
- **Sheet Name**: `viz_risk_default_by_int_rate`
- **Data Source**: `vw_risk_analysis`
- **Columns**: `[interest_rate_bracket]` (`< 8%`, `8% - 11.99%`, `12% - 15.99%`, `16% - 19.99%`, `>= 20%`)
- **Rows**: `AVG([is_default]) * 100`
- **Marks**: Column Bar Chart, Color `#E11D48`
- **Labels**: Percentage `0.0%` (e.g. Rate < 8%: ~5.4% default rate vs Rate >= 20%: ~24.7% default rate).
- **Tooltip**:  
  `Pricing Bracket: <interest_rate_bracket>`  
  `Default Rate: <default_rate_pct>%`  
  `Charged-Off Capital: $<SUM(charged_off_amount)>`

### Area 5: Charged-Off Amount by Year
- **Sheet Name**: `viz_risk_charged_off_by_year`
- **Data Source**: `vw_recovery_analysis`
- **Columns**: `[issue_year]` (`2021`)
- **Rows**: `SUM([gross_charged_off_amount])`
- **Marks**: Bar Chart / Text Pill, Color `#991B1B`
- **Labels**: Currency `$#,##0,,.2"M"` (`$65.53M`).
- **Tooltip**: `Year: 2021 | Gross Charged Off Funded Principal: $65,532,225`.

### Area 6: Recovery Rate by Year
- **Sheet Name**: `viz_risk_recovery_rate_by_year`
- **Data Source**: `vw_recovery_analysis`
- **Columns**: `[issue_year]` (`2021`)
- **Rows**: `[recovery_rate_pct]`
- **Marks**: Bar Chart / Bullet Gauge, Color `#7C3AED`
- **Labels**: Percentage `0.0%` (`56.9%`).
- **Calculated Formula**: `SUM([total_recoveries_received]) / SUM([gross_charged_off_amount]) * 100` (`$37.28M / $65.53M = 56.89%`).
- **Tooltip**:  
  `Year: 2021`  
  `Recoveries Received: $37,284,763`  
  `Gross Default Amount: $65,532,225`  
  `Net Credit Loss: $28,247,462`  
  `Recovery Rate: 56.89%`

### Area 7: Default Rate by Home Ownership
- **Sheet Name**: `viz_risk_default_by_home`
- **Data Source**: `vw_customer_analysis`
- **Columns**: `[home_ownership]` (`RENT`, `MORTGAGE`, `OWN`, `OTHER`)
- **Rows**: `AVG([is_default]) * 100`
- **Marks**: Bar Chart, Color `#475569`
- **Labels**: Percentage `0.0%` (`RENT`: ~14.6%, `MORTGAGE`: ~13.0%, `OWN`: ~13.7%).
- **Tooltip**:  
  `Home Ownership: <home_ownership>`  
  `Default Rate: <default_rate>%`  
  `Loan Count: <COUNT(loan_id)>`

### Area 8: Default Rate by Employment Length
- **Sheet Name**: `viz_risk_default_by_emp_length`
- **Data Source**: `vw_customer_analysis`
- **Columns**: `[emp_length]` (Ordered `< 1 year` to `10+ years`)
- **Rows**: `AVG([is_default]) * 100`
- **Marks**: Line Chart with Data Markers, Color `#64748B`
- **Labels**: Percentage `0.0%`.
- **Tooltip**:  
  `Employment Tenure: <emp_length>`  
  `Default Rate: <default_rate>%`  
  `Total Loans: <COUNT(loan_id)>`

### Area 9: Default Rate by Income Range
- **Sheet Name**: `viz_risk_default_by_income`
- **Data Source**: `vw_income_analysis`
- **Columns**: `[income_bracket]`
- **Rows**: `[default_rate_pct]`
- **Marks**: Column Bar Chart, Color `#EA580C`
- **Sorting**: Ascending by income tier.
- **Key Observation**: Borrowers earning under $30,000 experienced an observed default rate of ~18.3%, compared to ~10.4% for borrowers earning $120,000 or above.
- **Labels**: Percentage `0.0%`.
- **Tooltip**:  
  `Income Bracket: <income_bracket>`  
  `Default Rate: <default_rate_pct>%`  
  `Total Defaulted Loans: <default_count>`

---

### Area 10: High-Risk Loan KPIs (Summary Card Block)
- **Sheet Name**: `kpi_high_risk_summary`
- **Data Source**: `vw_risk_analysis`
- **Empirical Definition**:
  > **High-Risk Segment Definition**: Loans where borrower Debt-to-Income `DTI >= 0.20` (top quartile leverage) OR assigned credit grade is subprime (`Grade IN ('D', 'E', 'F', 'G')`).  
  > *Technical Note*: The maximum DTI in this actual dataset is 0.2999 (29.99%). Setting a filter of `DTI > 40%` yields zero records. This empirical definition provides genuine business utility.
- **KPI Metrics Rendered**:
  1. **Total High-Risk Loans**: `12,842 Loans` (~33.3% of total portfolio).
  2. **High-Risk Funded Amount**: `$164.2M` (~37.7% of total funded portfolio).
  3. **High-Risk Default Rate**: `22.41%` (2,878 charged-off loans vs 13.82% portfolio average).
- **Marks**: 3 KPI Cards, Border `#DC2626` (Red Accent).

---

### Area 11: Risk Distribution & Multi-Filter Ledger Grid
- **Sheet Name**: `viz_risk_segment_distribution`
- **Data Source**: `vw_risk_analysis`
- **Columns**: `[risk_segment]` (`Standard Risk` vs `High Risk`)
- **Rows**: `COUNT([loan_id])`, `SUM([loan_amount])`, `[default_rate_pct]`
- **Marks**: Stacked Bar Chart & Detailed Interactive Drill-Down Table
- **Ledger Columns**: `Loan ID`, `Grade`, `Purpose`, `Loan Amount`, `Interest Rate`, `DTI`, `Loan Status`, `Net Loss`.
- **Tooltip**: Provides granular borrower-level risk audit on click.

---

## 5. Dashboard Interactivity & Action Triggers
1. **Click on High Risk Segment (`act_filter_high_risk`)**: Filters the loan ledger and purpose breakdowns to high-risk borrowers.
2. **Click on Grade G Bar (`act_filter_subprime`)**: Drills down into the 33.8% default cohort, updating the geographic and purpose risk distribution.
3. **Hover on DTI Bracket (`act_highlight_dti`)**: Highlights corresponding income brackets and interest rate tiers.

