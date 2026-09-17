# DASHBOARD 2 - CUSTOMER & LOAN ANALYSIS

## 1. Executive Summary & Dashboard Architecture
**Dashboard Title**: `DASHBOARD 2 - CUSTOMER & LOAN ANALYSIS`  
**Primary Analytical Role**: Evaluates borrower demographic profiles, underwriting verification rigor, income and debt burden distribution, and loan structural attributes across the customer base.  
**Target Audience**: Credit Underwriting Officers, Retail Lending Product Managers, Customer Segmentation Strategy Teams.  
**Data Sources**: MySQL Database `bank_loan_analytics` -> Views `vw_customer_analysis`, `vw_income_analysis`, `vw_state_analysis`, and base table `loan_data`.

---

## 2. Canvas & Layout Container Specifications
- **Dashboard Dimensions**: Fixed Desktop Browser (`1600px` width × `1000px` height) or Automatic Responsive.
- **Color Palette & Theme**:
  - **Header / Corporate Accent**: Midnight Navy Blue (`#0F2537`)
  - **Canvas Background**: Clean Professional Gray (`#F8FAFC`)
  - **Primary Chart Fill**: Deep Sapphire (`#1E40AF`)
  - **Secondary Metric Accent (Income/DTI)**: Teal Cyan (`#0EA5E9`)
  - **Categorical Accent (Term/Verification)**: Indigo Violet (`#6366F1`)
- **Container Structure**:
  - **Top Horizontal Banner (`Height: 80px`)**: Title, Breadcrumbs, Tab Navigation ("1. Portfolio", "2. Customer & Loan", "3. Risk Analysis").
  - **Left Vertical Sidebar (`Width: 220px`)**: Interactive Filter Control Panel.
  - **Main Dashboard Grid (`Width: 1380px`)**:
    - **Top Row (`Height: 280px`)**:
      - Sheet 1: Loans by Home Ownership (Donut/Bar, `Width: 33%`)
      - Sheet 2: Loans by Employment Length (Ordered Bar, `Width: 34%`)
      - Sheet 3: Loans by Verification Status (Horizontal Bar, `Width: 33%`)
    - **Middle Row (`Height: 300px`)**:
      - Sheet 4 & 5: Loan Amount and Avg Ticket by Income Range (Dual Axis Column Chart, `Width: 35%`)
      - Sheet 6: Loans by Repayment Term (Donut Chart: 36 vs 60 months, `Width: 25%`)
      - Sheet 7: Top 5 Purposes by Average Interest Rate (Ranked Bar, `Width: 40%`)
    - **Bottom Row (`Height: 320px`)**:
      - Sheet 8: Average DTI by Income Range (Line & Dot Chart, `Width: 30%`)
      - Sheet 9 & 10: Loan Count & Average Amount by Grade (Dual Axis Bar/Line, `Width: 35%`)
      - Sheet 11: Top 10 States by Loan Count (Ranked Bar / Geographic Map, `Width: 35%`)

---

## 3. Global Filters Configuration
1. **Date Range**: Continuous Slider on `issue_date` (`2021-01-01` to `2021-12-31`).
2. **Credit Grade**: Multiple Values Dropdown (`[All]`, `A`, `B`, `C`, `D`, `E`, `F`, `G`).
3. **Loan Purpose**: Multiple Values Dropdown (`[All]`, 14 standard loan purposes).
4. **Home Ownership**: Multiple Values Dropdown (`[All]`, `RENT`, `MORTGAGE`, `OWN`, `OTHER`, `NONE`).
5. **Verification Status**: Multiple Values Dropdown (`[All]`, `Verified`, `Source Verified`, `Not Verified`).

---

## 4. Worksheets & Shelf Configurations (11 Core Visualization Areas)

### Area 1: Loans by Home Ownership
- **Sheet Name**: `viz_cust_home_ownership`
- **Data Source**: `vw_customer_analysis`
- **Columns**: `[home_ownership]` (`RENT`, `MORTGAGE`, `OWN`, `OTHER`, `NONE`)
- **Rows**: `COUNT([loan_id])`
- **Marks**: Vertical Bar Chart (or Donut Chart)
- **Color Mark**: `[home_ownership]` (`RENT` = `#3B82F6`, `MORTGAGE` = `#1E40AF`, `OWN` = `#10B981`, `OTHER/NONE` = `#94A3B8`)
- **Sorting**: Descending by loan count (`RENT`: 18,447, `MORTGAGE`: 17,198, `OWN`: 2,838).
- **Labels**: Show loan count (`#,##0`) and percentage of total (`0.0%`).
- **Tooltip**:  
  `Home Ownership: <home_ownership>`  
  `Loan Count: <COUNT(loan_id)>` (`<pct_of_total>%`)  
  `Total Funded: $<SUM(loan_amount)>`  
  `Avg Annual Income: $<AVG(annual_income)>`

### Area 2: Loans by Employment Length
- **Sheet Name**: `viz_cust_emp_length`
- **Data Source**: `vw_customer_analysis`
- **Columns**: `[emp_length]` (Sorted by tenure)
- **Rows**: `COUNT([loan_id])`
- **Marks**: Bar Chart, Color `#1E40AF`
- **Sorting**: Custom logical order: `< 1 year`, `1 year`, `2 years`, `3 years`, `4 years`, `5 years`, `6 years`, `7 years`, `8 years`, `9 years`, `10+ years`.
- **Labels**: Count of applications.
- **Key Insight**: Borrowers with 10+ years of employment represent the largest single borrower cohort (8,879 loans, ~23% of total).
- **Tooltip**:  
  `Tenure: <emp_length>`  
  `Applications: <COUNT(loan_id)>`  
  `Avg Loan Size: $<AVG(loan_amount)>`  
  `Default Rate: <default_rate_pct>%`

### Area 3: Loans by Verification Status
- **Sheet Name**: `viz_cust_verification_status`
- **Data Source**: `vw_customer_analysis`
- **Columns**: `COUNT([loan_id])`
- **Rows**: `[verification_status]` (`Not Verified`, `Verified`, `Source Verified`)
- **Marks**: Horizontal Bar Chart, Color by `[verification_status]`
- **Labels**: Show count and percentage of total applications.
- **Tooltip**:  
  `Status: <verification_status>`  
  `Total Loans: <COUNT(loan_id)>`  
  `Funded Amount: $<SUM(loan_amount)>`  
  `Avg Income: $<AVG(annual_income)>`

### Area 4: Average Loan Amount by Income Range
- **Sheet Name**: `viz_avg_loan_by_income`
- **Data Source**: `vw_income_analysis`
- **Columns**: `[income_bracket]`
- **Rows**: `[avg_loan_amount]`
- **Marks**: Bar / Line Chart, Color `#0EA5E9`
- **Sorting**: Ascending by income tier (`Under $30k`, `$30k-$60k`, `$60k-$90k`, `$90k-$120k`, `$120k+`).
- **Labels**: Currency `$#,##0` (e.g. Under $30k: $6,500 vs $120k+: $15,800).
- **Tooltip**:  
  `Income Tier: <income_bracket>`  
  `Avg Ticket Size: $<avg_loan_amount>`  
  `Borrower Income Avg: $<avg_annual_income>`

### Area 5: Total Loan Amount by Income Range
- **Sheet Name**: `viz_total_loan_by_income`
- **Data Source**: `vw_income_analysis`
- **Columns**: `[income_bracket]`
- **Rows**: `SUM([total_funded_amount])`
- **Marks**: Bar Chart, Color `#1E3A8A`
- **Labels**: Currency `$#,##0,,.1"M"`.
- **Tooltip**:  
  `Income Tier: <income_bracket>`  
  `Total Funded Capital: $<total_funded_amount>`  
  `Share of Portfolio: <pct_of_funded>%`

### Area 6: Loans by Repayment Term
- **Sheet Name**: `viz_cust_term_split`
- **Data Source**: `vw_customer_analysis`
- **Columns**: *(none)*
- **Rows**: *(none)*
- **Marks**: Pie / Donut Chart
- **Color Mark**: `[term]` (`36 months` = `#3B82F6`, `60 months` = `#F59E0B`)
- **Angle Mark**: `COUNT([loan_id])`
- **Labels**: Show Term, Count (`#,##0`), and Percentage (`73.2% 36 Months` vs `26.8% 60 Months`).
- **Tooltip**:  
  `Term: <term>`  
  `Total Loans: <COUNT(loan_id)>`  
  `Total Funded: $<SUM(loan_amount)>`  
  `Avg Interest Rate: <AVG(int_rate)*100>%`

### Area 7: Top 5 Purposes by Average Interest Rate
- **Sheet Name**: `viz_top5_purposes_by_rate`
- **Data Source**: `vw_purpose_analysis`
- **Columns**: `[avg_interest_rate_pct]`
- **Rows**: `[purpose]`
- **Marks**: Horizontal Bar Chart, Color Gradient (Orange to Red)
- **Top N Filter**: Top 5 by `avg_interest_rate_pct` (Renewable Energy, Small Business, House, Moving, Educational).
- **Labels**: Percentage `0.00%`.
- **Tooltip**:  
  `Purpose: <purpose>`  
  `Avg Interest Rate: <avg_interest_rate_pct>%`  
  `Total Loans: <total_loans>`  
  `Default Rate: <default_rate_pct>%`

### Area 8: Average DTI by Income Range
- **Sheet Name**: `viz_avg_dti_by_income`
- **Data Source**: `vw_income_analysis`
- **Columns**: `[income_bracket]`
- **Rows**: `[avg_dti_pct]`
- **Marks**: Line Chart with circle data points, Color `#D97706`
- **Labels**: Percentage `0.00%` (e.g. Under $30k: ~13.8% down to $120k+: ~11.9%).
- **Key Insight**: Lower-income borrowers carry higher debt-to-income leverage burdens.
- **Tooltip**:  
  `Income Tier: <income_bracket>`  
  `Average DTI: <avg_dti_pct>%`

### Area 9: Loan Count by Credit Grade
- **Sheet Name**: `viz_loan_count_by_grade`
- **Data Source**: `vw_grade_analysis`
- **Columns**: `[grade]` (`A`, `B`, `C`, `D`, `E`, `F`, `G`)
- **Rows**: `SUM([total_loans])`
- **Marks**: Bar Chart, Color `#1E40AF`
- **Sorting**: Grade alphabetical order (A through G).
- **Labels**: Integer `#,##0` (Grade B highest at 11.6K loans, Grade A at 9.9K loans).
- **Tooltip**:  
  `Grade: <grade>`  
  `Applications: <total_loans>`  
  `Pct of Portfolio: <pct_loans>%`

### Area 10: Average Loan Amount by Grade
- **Sheet Name**: `viz_avg_loan_by_grade`
- **Data Source**: `vw_grade_analysis`
- **Columns**: `[grade]`
- **Rows**: `AVG([avg_loan_amount])`
- **Marks**: Line & Symbol Chart, Color `#0D9488`
- **Labels**: Currency `$#,##0` (Grade A: $8,600 up to Grade G: $17,500).
- **Tooltip**:  
  `Grade: <grade>`  
  `Avg Loan Size: $<avg_loan_amount>`  
  `Avg Interest Rate: <avg_interest_rate_pct>%`

### Area 11: Top 10 States by Loan Count
- **Sheet Name**: `viz_top10_states_count`
- **Data Source**: `vw_state_analysis`
- **Columns**: `[total_applications]`
- **Rows**: `[state_code]`
- **Marks**: Horizontal Bar Chart, Color `#1E3A8A`
- **Sorting**: Descending by `total_applications`.
- **Top N Filter**: Top 10 States (CA: 6,894, NY: 3,701, FL: 2,773, TX: 2,662, NJ: 1,822, etc.).
- **Labels**: Count formatted as `#,##0`.
- **Tooltip**:  
  `State: <state_code>`  
  `Total Applications: <total_applications>`  
  `Total Funded: $<total_funded_amount>`  
  `Default Rate: <default_rate_pct>%`

---

## 5. Dashboard Interactivity & Action Triggers
1. **Click-to-Filter on State Bar (`act_filter_state_cust`)**: Selecting California filters all employment, home ownership, and term charts to California borrowers.
2. **Click-to-Filter on Grade Bar (`act_filter_grade_cust`)**: Selecting Grade A reveals the prime borrower demographic profile.
3. **Hover Highlight on Term (`act_highlight_term`)**: Highlights the 36-month vs 60-month loan cohorts across all income brackets.

