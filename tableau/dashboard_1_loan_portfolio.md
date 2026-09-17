# DASHBOARD 1 - LOAN PORTFOLIO OVERVIEW

## 1. Executive Summary & Dashboard Architecture
**Dashboard Title**: `DASHBOARD 1 - LOAN PORTFOLIO OVERVIEW`  
**Primary Analytical Role**: High-level portfolio health monitoring, capital deployment velocity, cash collection performance, and high-level credit performance segmentation.  
**Target Audience**: Chief Credit Officer (CCO), Portfolio Managers, Treasury & Capital Allocation Committees.  
**Data Sources**: MySQL Database `bank_loan_analytics` -> Views `vw_loan_kpis`, `vw_monthly_loan_summary`, `vw_loan_status_distribution`, `vw_state_analysis`, and base table `loan_data`.

---

## 2. Canvas & Layout Container Specifications
- **Dashboard Dimensions**: Fixed Desktop Browser (`1600px` width × `1000px` height) or Automatic Responsive.
- **Color Palette & Theme**:
  - **Header / Corporate Accent**: Midnight Navy Blue (`#0F2537`)
  - **Canvas Background**: Crisp Off-White / Light Gray (`#F4F7F9`)
  - **KPI Card Background**: Clean White (`#FFFFFF`) with 1px border (`#E2E8F0`) and subtle drop shadow.
  - **Primary Metric Accent (Good Loans / Cash Received)**: Emerald Green (`#10B981`)
  - **Neutral / Capital Funded**: Navy Slate (`#1E3A8A`)
  - **Alert / Bad Loans / Defaults**: Crimson Coral (`#EF4444`)
- **Container Structure**:
  - **Top Horizontal Container (`Height: 80px`)**: Corporate Header Banner with Title, Subtitle ("Data as of December 31, 2021"), and Navigation Buttons.
  - **Upper Horizontal Container (`Height: 110px`)**: 6 Financial KPI Cards.
  - **Middle Horizontal Container (`Height: 380px`)**:
    - Left Column (`Width: 50%`): Sheet 7 (Loan Status Distribution Grid / Donut) & Supplementary Purpose/Grade Bars.
    - Right Column (`Width: 50%`): Sheet 8 (Total Funded vs Received Amount by Month Area/Line Chart).
  - **Lower Horizontal Container (`Height: 380px`)**:
    - Left Column (`Width: 35%`): Sheet 9 (Total Loan Amount by Quarter) & Sheet 10 (Applications by Year).
    - Center Column (`Width: 40%`): Sheet 11 (Top 10 States by Total Loan Amount Horizontal Bar).
    - Right Column (`Width: 25%`): Loan Amount and Interest Rate Distributions.
  - **Left Vertical Sidebar (`Width: 220px`)**: Interactive Global Filter Panel.

---

## 3. Global Filters Configuration
Global filters apply across all sheets in Dashboard 1 using Tableau's **"Apply to Worksheets -> Selected Worksheets / All Using Related Data Sources"**:
1. **Issue Date Range**: Continuous Date Filter (`Range of Dates: 2021-01-01 to 2021-12-31`).
2. **Loan Status**: Multiple Values (Dropdown) — `[All]`, `Fully Paid`, `Current`, `Charged Off`.
3. **Credit Grade**: Multiple Values (Dropdown) — `[All]`, `A`, `B`, `C`, `D`, `E`, `F`, `G`.
4. **Loan Purpose**: Multiple Values (Dropdown) — `[All]`, `Debt Consolidation`, `Credit Card`, `Home Improvement`, etc.
5. **Home Ownership**: Multiple Values (Dropdown) — `[All]`, `MORTGAGE`, `RENT`, `OWN`, `OTHER`, `NONE`.

---

## 4. Worksheets & Shelf Configurations (11 Core Visualization Areas)

### Area 1: Total Loan Applications (KPI Card 1)
- **Sheet Name**: `kpi_total_applications`
- **Data Source**: `vw_loan_kpis`
- **Columns**: *(empty)*
- **Rows**: *(empty)*
- **Marks**: Text
- **Measures / Text Pill**: `AGG(SUM([total_loan_applications]))`
- **Formatting**: Number format `#,##0` or `38.6K` (`38,576`), Font: Segoe UI / Tableau Bold 24pt, Midnight Navy `#0F2537`.
- **Subtitle / Label**: "TOTAL LOAN APPLICATIONS | MTD: 4,314 | MoM: +6.91%"
- **Tooltip**: "Total volume of originated borrower loan applications across the portfolio."

### Area 2: Total Funded Amount (KPI Card 2)
- **Sheet Name**: `kpi_total_funded`
- **Data Source**: `vw_loan_kpis`
- **Marks**: Text
- **Measures / Text Pill**: `AGG(SUM([total_funded_amount]))`
- **Formatting**: Currency custom `$#,##0,,.0"M"` (`$435.8M`), Font: Tableau Bold 24pt, Navy `#1E3A8A`.
- **Subtitle / Label**: "TOTAL FUNDED AMOUNT | MTD: $54.0M | MoM: +13.04%"
- **Tooltip**: "Total principal capital disbursed to borrowers at loan origination."

### Area 3: Total Received Amount (KPI Card 3)
- **Sheet Name**: `kpi_total_received`
- **Data Source**: `vw_loan_kpis`
- **Marks**: Text
- **Measures / Text Pill**: `AGG(SUM([total_received_amount]))`
- **Formatting**: Currency custom `$#,##0,,.0"M"` (`$473.1M`), Font: Tableau Bold 24pt, Emerald Green `#10B981`.
- **Subtitle / Label**: "TOTAL CASH RECEIVED | MTD: $58.1M | MoM: +15.84%"
- **Tooltip**: "Total cumulative cash collected from borrower payments (principal + interest + fees)."

### Area 4: Average Interest Rate (KPI Card 4)
- **Sheet Name**: `kpi_avg_int_rate`
- **Data Source**: `vw_loan_kpis`
- **Marks**: Text
- **Measures / Text Pill**: `AGG(AVG([avg_interest_rate_pct]))`
- **Formatting**: Percentage `0.00%` (`12.05%`), Font: Tableau Bold 24pt, Slate `#334155`.
- **Subtitle / Label**: "AVERAGE INTEREST RATE | MTD: 12.36% | MoM: +3.52%"
- **Tooltip**: "Weighted portfolio average borrower interest rate."

### Area 5: Average Loan Amount (KPI Card 5)
- **Sheet Name**: `kpi_avg_loan_amount`
- **Data Source**: `vw_loan_kpis`
- **Marks**: Text
- **Measures / Text Pill**: `AGG(AVG([avg_loan_amount]))`
- **Formatting**: Currency custom `$#,##0` (`$11,296`), Font: Tableau Bold 24pt, Slate `#334155`.
- **Subtitle / Label**: "AVERAGE TICKET SIZE | Min: $500 | Max: $35,000"
- **Tooltip**: "Mean loan principal disbursed per approved applicant."

### Area 6: Default / Charged-Off Rate (KPI Card 6)
- **Sheet Name**: `kpi_default_rate`
- **Data Source**: `vw_loan_kpis`
- **Marks**: Text
- **Measures / Text Pill**: `[bad_loan_pct]`
- **Formatting**: Percentage `0.00%` (`13.82%`), Font: Tableau Bold 24pt, Crimson Coral `#EF4444`.
- **Subtitle / Label**: "DEFAULT RATE (5,333 Loans) | Loss: $28.25M"
- **Tooltip**: "Percentage of total loan applications classified as Charged Off (uncollectible)."

---

### Area 7: Loan Status Distribution (Good vs Bad Portfolio Health)
- **Sheet Name**: `viz_loan_status_distribution`
- **Data Source**: `vw_loan_status_distribution`
- **Columns**: `Measure Names` (`total_applications`, `total_funded_amount`, `total_received_amount`, `avg_interest_rate_pct`, `avg_dti_pct`)
- **Rows**: `[loan_status]`
- **Marks**: Table / Multi-Measure Grid or Side-by-Side Horizontal Bar
- **Color Mark**: `[loan_status]` (Fully Paid = `#10B981`, Current = `#3B82F6`, Charged Off = `#EF4444`)
- **Sorting**: Total funded amount descending.
- **Labels**: Show values for each cell formatted as Currency (`$M`), Integer (`#,##0`), and Percentage (`0.0%`).
- **Tooltip**:  
  `Loan Status: <loan_status>`  
  `Total Applications: <total_applications>` (`<pct_of_total_loans>%`)  
  `Total Funded: $<total_funded_amount>`  
  `Total Received: $<total_received_amount>`  
  `Avg Interest Rate: <avg_interest_rate_pct>%`

### Area 8: Total Funded Amount by Month (Monthly Lending Trend)
- **Sheet Name**: `viz_monthly_funded_trend`
- **Data Source**: `vw_monthly_loan_summary`
- **Columns**: `[month_number]` (Continuous or Discrete chronologically sorted 1 to 12 with aliases Jan-Dec)
- **Rows**: `SUM([total_funded_amount])`, `SUM([total_received_amount])` (Dual Axis)
- **Marks**:
  - Primary Axis (`total_funded_amount`): Area Chart, Color `#1E3A8A` (40% opacity), Line `#1E3A8A` (2px).
  - Secondary Axis (`total_received_amount`): Line Chart, Color `#10B981` (2.5px solid), with circular data points.
- **Sorting**: Chronological `month_number ASC` (January through December).
- **Labels**: Show label on latest point (Dec: `$54.0M Funded / $58.1M Received`).
- **Tooltip**:  
  `Month: <month_name> 2021`  
  `Funded Amount: $<total_funded_amount>`  
  `Cash Received: $<total_received_amount>`  
  `Applications: <total_applications>`  
  `Avg Interest Rate: <avg_interest_rate_pct>%`

### Area 9: Total Loan Amount by Quarter
- **Sheet Name**: `viz_quarterly_funded`
- **Data Source**: `vw_monthly_loan_summary`
- **Columns**: `[issue_quarter]` (`Q1`, `Q2`, `Q3`, `Q4`)
- **Rows**: `SUM([total_funded_amount])`
- **Marks**: Bar Chart, Color `#2563EB`
- **Sorting**: Chronological (`Q1` to `Q4`).
- **Labels**: Show total amount formatted as `$#,##0,,.0"M"`.
- **Tooltip**:  
  `Quarter: <issue_quarter>`  
  `Funded Amount: $<total_funded_amount>`  
  `Total Applications: <total_applications>`

### Area 10: Loan Applications by Year
- **Sheet Name**: `viz_applications_by_year`
- **Data Source**: `vw_monthly_loan_summary`
- **Columns**: `[issue_year]` (`2021`)
- **Rows**: `SUM([total_applications])`
- **Marks**: Bar Chart / Text Card, Color `#0F2537`
- **Labels**: `38,576 Applications` (`$435.8M Funded`).
- **Tooltip**: `Origination Year: 2021 | 38,576 Total Applications`.

### Area 11: Total Loan Amount by State - Top 10
- **Sheet Name**: `viz_top10_states_funded`
- **Data Source**: `vw_state_analysis`
- **Columns**: `SUM([total_funded_amount])`
- **Rows**: `[state_code]`
- **Marks**: Horizontal Bar Chart, Color `#1E3A8A`
- **Sorting**: Sort `state_code` descending by `SUM([total_funded_amount])`.
- **Top N Filter**: Top 10 by `SUM([total_funded_amount])` (CA: $64.4M, NY: $41.4M, TX: $37.8M, FL: $34.5M, etc.).
- **Labels**: Show funded amount formatted as `$#,##0,,.1"M"`.
- **Tooltip**:  
  `State: <state_code>`  
  `Total Funded: $<total_funded_amount>`  
  `Applications: <total_applications>`  
  `Default Rate: <default_rate_pct>%`

---

## 5. Supplementary Integrated Visualizations (Incorporated)

### 12. Top 5 Loan Purposes by Funded Amount
- **Sheet Name**: `viz_top5_purposes`
- **Shelf**: Rows = `purpose`, Columns = `SUM(loan_amount)`, Marks = Bar Chart.
- **Top N Filter**: Top 5 (Debt Consolidation, Credit Card, Home Improvement, Major Purchase, Small Business).
- **Ranking Insight**: Debt Consolidation accounts for over 50% of total funded capital ($233.9M).

### 13. Top 5 Loan Grades by Funded Amount
- **Sheet Name**: `viz_top5_grades`
- **Shelf**: Rows = `grade`, Columns = `SUM(loan_amount)`, Marks = Bar Chart (Grades B, A, C, D, E).

### 14. Loan Amount Range Distribution
- **Sheet Name**: `viz_loan_amount_buckets`
- **Shelf**: Columns = `loan_amount_bracket`, Rows = `COUNT(id)`, Marks = Histogram/Bar.
- **Bins**: `<$5k`, `$5k-$10k`, `$10k-$15k`, `$15k-$20k`, `$20k-$25k`, `>=$25k`.

### 15. Interest Rate Distribution
- **Sheet Name**: `viz_int_rate_distribution`
- **Shelf**: Columns = `int_rate_bracket`, Rows = `COUNT(id)`, Marks = Column Bar.

### 16. Average Interest Rate by Grade
- **Sheet Name**: `viz_avg_int_rate_by_grade`
- **Shelf**: Columns = `grade`, Rows = `AVG(int_rate)`, Marks = Line / Dot plot with risk ladder (A: 7.34% to G: 20.91%).

---

## 6. Dashboard Interactivity & Action Triggers
1. **Filter Action `act_filter_by_loan_status`**:
   - **Source Sheet**: `viz_loan_status_distribution`
   - **Target Sheets**: All sheets on Dashboard 1 & 2.
   - **Trigger**: Select (Click).
   - **Behavior**: Clicking "Charged Off" filters the monthly trend, state map, and purpose breakdowns to defaulted loans only.
2. **Filter Action `act_filter_by_state`**:
   - **Source Sheet**: `viz_top10_states_funded`
   - **Target Sheets**: Monthly trend, loan status distribution.
   - **Trigger**: Select (Click).
3. **Highlight Action `act_highlight_grade`**:
   - **Source Sheet**: `viz_top5_grades`
   - **Trigger**: Hover. Highlights corresponding points on the monthly trend and state bar charts.

