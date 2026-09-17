# Tableau Final Setup Guide & Manual Workbook Construction

> [!IMPORTANT]
> **Environment Status**: Tableau Desktop is **not installed** in this local CLI environment.
> Therefore, **Tableau Desktop work remains to be completed manually**.
> In strict compliance with technical accuracy and audit governance, no fake `.twb` binary or synthetic dashboard mockup has been generated.
> Follow this exact 18-step implementation manual to build, configure, format, and validate the 3 dashboards in Tableau Desktop or Tableau Public.

---

## Complete 18-Step Manual Build Process

### Step 1: Open Tableau Desktop
1. Launch **Tableau Desktop** (v2021.1+ or newer) or **Tableau Public Edition** on your workstation.
2. Ensure you have the MySQL Connector/ODBC driver installed if connecting directly to a local MySQL server (available free from the official MySQL website).

---

### Step 2: Connect to MySQL (or Cleaned CSV)
1. On the Tableau start screen under the **"Connect"** left navigation pane:
   - Under **"To a Server"**, select **"MySQL"** (click "More..." if not visible in the top list).
   - *Alternative (No MySQL server required)*: Under **"To a File"**, click **"Text file"**, and browse directly to `BANK_LOAN_LENDING_DATA_ANALYTICS/data/cleaned/loan_data_cleaned.csv`.

---

### Step 3: Server Configuration
In the MySQL Connection dialog box, configure your host credentials:
- **Server**: `localhost` (or `127.0.0.1`)
- **Port**: `3306` (standard MySQL default port)

---

### Step 4: Username Configuration
- **Username**: Enter `root` (or the dedicated analytics user created via `sql/01_database_setup.sql`, e.g., `loan_analyst`).

---

### Step 5: Password Field Location & Entry
- In the **Password** field immediately below the Username field, enter your MySQL root user password (e.g. `root` or your local development password).
- Check **"Remember password"** if you want Tableau to preserve credentials across sessions.
- Click the orange **"Sign In"** button.

---

### Step 6: Database Selection
1. Once connected, locate the **Database** dropdown menu on the left data source pane.
2. Click the dropdown and select (or search for): `bank_loan_analytics`.

---

### Step 7: Select `bank_loan_analytics`
- Confirm `bank_loan_analytics` is selected. The left pane will now populate with:
  - **Tables**: `loan_data`
  - **Views**: The 10 production analytical views created by `sql/09_tableau_views.sql`.

---

### Step 8: Select the Analytical Views
Drag the primary table or views onto the Data Source canvas:
- **Primary Data Source**: Drag `loan_data` onto the canvas.
- For dedicated pre-aggregated reporting, you can also add the analytical views:
  - `vw_loan_kpis` (Single-row portfolio and MTD totals)
  - `vw_monthly_loan_summary` (Chronological time series)
  - `vw_loan_status_distribution` (Portfolio status splits)
  - `vw_grade_analysis` (Credit grade ladder)
  - `vw_purpose_analysis` (Loan purpose breakdown)
  - `vw_customer_analysis` (Borrower demographic profile)
  - `vw_risk_analysis` (Risk segment and loss metrics)
  - `vw_state_analysis` (State geographical metrics)
  - `vw_income_analysis` (Income bracket distribution)
  - `vw_recovery_analysis` (Charged-off recovery metrics)

---

### Step 9: Create Each Worksheet (33 Visualizations Across 3 Dashboards)

Click on **Sheet 1** at the bottom of Tableau to begin building worksheets.
Refer to the exact shelf configurations in:
- [`tableau/dashboard_1_loan_portfolio.md`](../tableau/dashboard_1_loan_portfolio.md)
- [`tableau/dashboard_2_customer_loan_analysis.md`](../tableau/dashboard_2_customer_loan_analysis.md)
- [`tableau/dashboard_3_risk_analysis.md`](../tableau/dashboard_3_risk_analysis.md)

#### Dashboard 1 Worksheets (Portfolio Overview):
1. `kpi_total_applications`: Text card showing `COUNT([id])` (38,576).
2. `kpi_total_funded`: Text card showing `SUM([loan_amount])` ($435.8M).
3. `kpi_total_received`: Text card showing `SUM([total_payment])` ($473.1M).
4. `kpi_avg_int_rate`: Text card showing `AVG([int_rate])` (12.05%).
5. `kpi_avg_loan_amount`: Text card showing `AVG([loan_amount])` ($11,296).
6. `kpi_default_rate`: Text card showing `[Default Rate]` (13.82%).
7. `viz_loan_status_distribution`: Grid/table with `[loan_status]` on Rows and applications, funded, received, and rates on Columns.
8. `viz_monthly_funded_trend`: Columns = `MONTH([issue_date])`, Rows = Dual Axis `SUM([loan_amount])` (Area `#1E3A8A`) and `SUM([total_payment])` (Line `#10B981`).
9. `viz_quarterly_funded`: Columns = `QUARTER([issue_date])`, Rows = `SUM([loan_amount])` (Bar chart).
10. `viz_applications_by_year`: Bar chart displaying 2021 annual volume (38,576).
11. `viz_top10_states_funded`: Rows = `[address_state]`, Columns = `SUM([loan_amount])` (Horizontal bar filtered to Top 10).
*(Supplementary sheets: `viz_top5_purposes`, `viz_top5_grades`, `viz_loan_amount_buckets`, `viz_int_rate_distribution`, `viz_avg_int_rate_by_grade`).*

#### Dashboard 2 Worksheets (Customer & Loan Analysis):
1. `viz_cust_home_ownership`: Donut or bar chart by `[home_ownership]`.
2. `viz_cust_emp_length`: Bar chart by `[emp_length]`, sorted `< 1 year` to `10+ years`.
3. `viz_cust_verification_status`: Horizontal bars by `[verification_status]`.
4. `viz_avg_loan_by_income`: Column chart showing average ticket size by `[income_bracket]`.
5. `viz_total_loan_by_income`: Column chart showing total funded capital by `[income_bracket]`.
6. `viz_cust_term_split`: Donut chart showing `[term]` (73.2% 36 mos vs 26.8% 60 mos).
7. `viz_top5_purposes_by_rate`: Horizontal bar of Top 5 purposes by average interest rate.
8. `viz_avg_dti_by_income`: Line chart showing average DTI across income brackets.
9. `viz_loan_count_by_grade`: Bar chart of applications by credit grade (A-G).
10. `viz_avg_loan_by_grade`: Line/symbol chart of average ticket size across grades.
11. `viz_top10_states_count`: Horizontal bar of Top 10 states by application count.

#### Dashboard 3 Worksheets (Risk Analysis):
1. `viz_risk_default_rate_by_grade`: Step/bar chart of default rate from Grade A (~6.0%) to Grade G (~33.8%).
2. `viz_risk_default_by_purpose`: Horizontal bar of default rates for Top 10 purposes (Small Business highest at ~27.1%).
3. `viz_risk_default_by_dti`: Default rate across DTI ranges (<10% to >25%).
4. `viz_risk_default_by_int_rate`: Default rate across interest rate brackets.
5. `viz_risk_charged_off_by_year`: Bar chart showing $65.53M gross default principal.
6. `viz_risk_recovery_rate_by_year`: Bullet/gauge showing 56.89% recovery rate ($37.28M recovered).
7. `viz_risk_default_by_home`: Default rate comparison across home ownership categories.
8. `viz_risk_default_by_emp_length`: Default rate curve across employment tenure.
9. `viz_risk_default_by_income`: Default rate across annual income brackets (<$30k at ~18.3% down to $120k+ at ~10.4%).
10. `kpi_high_risk_summary`: Summary card of High-Risk Segment (12,842 loans, $164.2M funded, 22.41% default rate).
11. `viz_risk_segment_distribution`: Multi-filter drill-down ledger grid showing granular loan defaults.

---

### Step 10: Create Calculated Fields
In the Data pane, click the small triangle next to the search bar and choose **"Create Calculated Field"**.
Create each formula exactly as provided in [`tableau/calculated_fields.md`](../tableau/calculated_fields.md):
- `[Default Flag]`: `IF [loan_status] = 'Charged Off' THEN 1 ELSE 0 END`
- `[Default Rate]`: `SUM([Default Flag]) / COUNT([id])` (Format: `Percentage`, 2 decimals)
- `[Good Loan Flag]`: `IF [loan_status] = 'Fully Paid' OR [loan_status] = 'Current' THEN 1 ELSE 0 END`
- `[Good Loan Rate]`: `SUM([Good Loan Flag]) / COUNT([id])`
- `[Loan Amount Range]`: (Case/If statement for <$5k to >$25k)
- `[Income Range]`: (Under $30k to $120k+)
- `[DTI Range]`: (Under 10% to 25%+)
- `[Interest Rate Range]`: (Under 8% to 20%+)
- `[High Risk Flag]`: `IF [dti] >= 0.20 OR [grade] = 'D' OR [grade] = 'E' OR [grade] = 'F' OR [grade] = 'G' THEN 'High Risk' ELSE 'Standard Risk' END`
- `[Recovery Rate]`: `SUM(IF [loan_status] = 'Charged Off' THEN [total_payment] ELSE 0 END) / NULLIF(SUM(IF [loan_status] = 'Charged Off' THEN [loan_amount] ELSE 0 END), 0)`

---

### Step 11: Create Filters
On each worksheet, drag the appropriate dimensions to the **Filters** shelf:
- `[issue_date]`: Range of Dates (`2021-01-01` to `2021-12-31`).
- `[loan_status]`: Multiple values list.
- `[grade]`: Multiple values list.
- `[purpose]`: Multiple values list.
- `[home_ownership]`: Multiple values list.
- `[verification_status]`: Multiple values list.
Right-click each filter on the shelf and select: **"Apply to Worksheets -> Selected Worksheets..."** so that global filters synchronize across all sheets.

---

### Step 12: Build Dashboard 1 (Loan Portfolio Overview)
1. Click **New Dashboard** at the bottom. Rename to: `DASHBOARD 1 - LOAN PORTFOLIO OVERVIEW`.
2. Under Dashboard Size, set **Fixed Size** to `1600 x 1000` pixels.
3. Drag a **Vertical Container** onto the canvas.
4. Header: Add a **Horizontal Container** (`Height: 80px`). Add text box title: `BANK LOAN LENDING DATA ANALYTICS | PORTFOLIO OVERVIEW` with Navy `#0F2537` background and white text.
5. KPI Band: Add a **Horizontal Container** (`Height: 110px`). Drag `kpi_total_applications`, `kpi_total_funded`, `kpi_total_received`, `kpi_avg_int_rate`, `kpi_avg_loan_amount`, and `kpi_default_rate` side-by-side.
6. Main Body: Add a **Horizontal Container**.
   - Left Sidebar (`Width: 220px`): Place the global filter controls.
   - Right Main Grid: Place `viz_loan_status_distribution`, `viz_monthly_funded_trend`, `viz_quarterly_funded`, and `viz_top10_states_funded`.

---

### Step 13: Build Dashboard 2 (Customer & Loan Analysis)
1. Click **New Dashboard**. Rename to: `DASHBOARD 2 - CUSTOMER & LOAN ANALYSIS`.
2. Set Fixed Size to `1600 x 1000`.
3. Add Header Container (`Height: 80px`).
4. Place filter sidebar on the left.
5. Place customer demographic charts in a clean 3-row grid:
   - Row 1: Home Ownership, Employment Length, Verification Status.
   - Row 2: Income Range, Loan Term, Top 5 Purposes by Interest Rate.
   - Row 3: DTI by Income, Grade Sizing, Top 10 States.

---

### Step 14: Build Dashboard 3 (Risk Analysis)
1. Click **New Dashboard**. Rename to: `DASHBOARD 3 - RISK ANALYSIS`.
2. Set Fixed Size to `1600 x 1050`.
3. Add Header Container (`Height: 80px`).
4. Place `kpi_high_risk_summary` card block at the top.
5. Place Default Rate by Grade, Default Rate by Purpose, and DTI tiers in the upper chart row.
6. Place Gross Charged-Off Amount, Recovery Rate, and the Granular Loan Drill-Down Ledger in the lower row.

---

### Step 15: Add Navigation
Add Tableau Navigation Buttons to allow one-click traversal between dashboards:
1. In the Objects panel on the left of each dashboard, drag a **Navigation** object into the header container.
2. In the Edit Button dialog:
   - **Navigate To**: Select `DASHBOARD 1 - LOAN PORTFOLIO OVERVIEW`, `DASHBOARD 2 - CUSTOMER & LOAN ANALYSIS`, or `DASHBOARD 3 - RISK ANALYSIS`.
   - **Button Style**: Text Button.
   - **Title**: `1. Portfolio Overview` | `2. Customer Analysis` | `3. Risk Analysis`.
   - **Background**: `#1E3A8A` (Navy), Font: White, Semi-bold.

---

### Step 16: Add Interactions (Dashboard Actions)
Go to **Dashboard -> Actions... -> Add Action**:
1. **Filter Action `Filter by Status`**:
   - Source: `viz_loan_status_distribution`
   - Target: All sheets in Dashboard 1 & 2
   - Run on: Select (Click)
   - Clearing the selection: Show all values.
2. **Filter Action `Filter by State`**:
   - Source: `viz_top10_states_funded`
   - Target: Monthly trend, loan purpose, and customer demographics.
   - Run on: Select (Click).
3. **Filter Action `Drill Down on High Risk`**:
   - Source: `kpi_high_risk_summary`
   - Target: Granular Loan Ledger on Dashboard 3.
   - Run on: Select (Click).
4. **Highlight Action `Highlight Grade`**:
   - Source: `viz_top5_grades` / `viz_loan_count_by_grade`
   - Run on: Hover.

---

### Step 17: Validate KPIs Against SQL Baseline
Before finalizing, verify that the numbers displayed on your Tableau canvas match the SQL baseline results from `sql/04_kpi_analysis.sql`:
- Total Applications: **38,576**
- Total Funded Amount: **$435,757,075.00** ($435.8M)
- Total Received Amount: **$473,070,933.00** ($473.1M)
- Average Interest Rate: **12.05%**
- Average Loan Amount: **$11,296.07**
- Default Rate: **13.82%** (5,333 charged-off loans)
- Fully Paid Rate: **83.33%** (32,145 fully paid loans)
- Recovery Rate: **56.89%** ($37,284,763 / $65,532,225)
- Net Credit Loss: **$28,247,462.00**

---

### Step 18: Save & Export Workbook
1. In Tableau Desktop, select **File -> Save As...**
2. Choose **Tableau Packaged Workbook (`.twbx`)** to bundle the data extract and sheets.
3. Save as: `tableau/Bank_Loan_Lending_Analytics.twbx`.
4. (Optional for Portfolio): Select **Server -> Tableau Public -> Save to Tableau Public As...** to generate a live shareable web URL for your resume and LinkedIn portfolio.

