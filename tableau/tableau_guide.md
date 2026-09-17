# Complete Tableau Build & Reproduction Guide

This guide walks you through the step-by-step process of constructing the complete 3-dashboard, 33-visualization Tableau workbook from scratch using the MySQL `bank_loan_analytics` database or the cleaned CSV data.

---

## Step 1: Open Tableau & Connect to Data

### Option A: Direct MySQL Connection (Recommended)
1. Launch **Tableau Desktop** (or **Tableau Public**).
2. Under "Connect -> To a Server", click **MySQL**.
3. In the Connection Dialog:
   - **Server**: `localhost` (or `127.0.0.1`)
   - **Port**: `3306`
   - **Database**: `bank_loan_analytics`
   - **Username**: `root` (or your configured user)
   - **Password**: `YourPassword`
4. Click **Sign In**.

### Option B: Cleaned CSV File Connection (No Database Server Required)
1. Under "Connect -> To a File", click **Text file**.
2. Navigate to `BANK_LOAN_LENDING_DATA_ANALYTICS/data/cleaned/loan_data_cleaned.csv` and select **Open**.
3. Verify that all 24 fields load with appropriate types:
   - `issue_date`, `last_payment_date`: Date
   - `loan_amount`, `total_payment`, `annual_income`, `installment`: Number (decimal)
   - `int_rate`, `dti`: Number (decimal)
   - `id`, `member_id`, `total_acc`: Number (whole)
   - `grade`, `sub_grade`, `purpose`, `home_ownership`, `address_state`, `term`, `loan_status`: String

---

## Step 2: Drag and Organize Data Sources
In the Tableau Data Source canvas:
- For MySQL: Drag the analytical views (`vw_loan_kpis`, `vw_monthly_loan_summary`, `vw_customer_analysis`, `vw_risk_analysis`, `vw_state_analysis`) or the primary `loan_data` table onto the canvas.
- For CSV: Select the `loan_data_cleaned.csv` extract.

---

## Step 3: Create Calculated Fields
Click the dropdown arrow in the Data pane and select **Create Calculated Field**. Create each formula exactly as documented in [`calculated_fields.md`](file:///Users/dineshkumarsingh/Documents/antigravity/goofy-mendeleev/BANK_LOAN_LENDING_DATA_ANALYTICS/tableau/calculated_fields.md):
1. `[Default Flag]`: `IF [Loan Status] = 'Charged Off' THEN 1 ELSE 0 END`
2. `[Default Rate]`: `SUM([Default Flag]) / COUNT([Id])` (Format: Percentage, 2 decimals)
3. `[Good Loan Flag]`: `IF [Loan Status] = 'Fully Paid' OR [Loan Status] = 'Current' THEN 1 ELSE 0 END`
4. `[Good Loan Rate]`: `SUM([Good Loan Flag]) / COUNT([Id])`
5. `[Loan Amount Range]`: (CASE / IF statement for tickets <$5k to >$25k)
6. `[Income Range]`: (Under $30k to $120k+)
7. `[DTI Range]`: (Under 10% to 25%+)
8. `[Interest Rate Range]`: (Under 8% to 20%+)
9. `[High Risk Flag]`: `IF [DTI] >= 0.20 OR [Grade] IN ('D','E','F','G') THEN 'High Risk' ELSE 'Standard Risk' END`
10. `[Recovery Rate]`: `SUM(IF [Loan Status] = 'Charged Off' THEN [Total Payment] ELSE 0 END) / NULLIF(SUM(IF [Loan Status] = 'Charged Off' THEN [Loan Amount] ELSE 0 END), 0)`

---

## Step 4: Build Worksheets for Dashboard 1 (Loan Portfolio Overview)
Build each worksheet following the shelf instructions in [`dashboard_1_loan_portfolio.md`](file:///Users/dineshkumarsingh/Documents/antigravity/goofy-mendeleev/BANK_LOAN_LENDING_DATA_ANALYTICS/tableau/dashboard_1_loan_portfolio.md):
- **Sheets 1-6 (KPI Cards)**: Create individual text cards for Total Applications (`COUNT([Id])`), Total Funded (`SUM([Loan Amount])`), Total Received (`SUM([Total Payment])`), Average Rate (`AVG([Int Rate])`), Average Loan Amount (`AVG([Loan Amount])`), and Default Rate (`[Default Rate]`).
- **Sheet 7 (`viz_loan_status_distribution`)**: Rows = `[Loan Status]`, Columns = `Measure Values`. Format as text table / status card.
- **Sheet 8 (`viz_monthly_funded_trend`)**: Columns = `MONTH([Issue Date])`, Rows = Dual Axis `SUM([Loan Amount])` (Area `#1E3A8A`) and `SUM([Total Payment])` (Line `#10B981`).
- **Sheet 9 (`viz_quarterly_funded`)**: Columns = `QUARTER([Issue Date])`, Rows = `SUM([Loan Amount])`.
- **Sheet 10 (`viz_applications_by_year`)**: Bar chart showing 2021 total applications.
- **Sheet 11 (`viz_top10_states_funded`)**: Rows = `[Address State]`, Columns = `SUM([Loan Amount])`. Add Top 10 filter.

---

## Step 5: Build Worksheets for Dashboard 2 (Customer & Loan Analysis)
Build each worksheet following [`dashboard_2_customer_loan_analysis.md`](file:///Users/dineshkumarsingh/Documents/antigravity/goofy-mendeleev/BANK_LOAN_LENDING_DATA_ANALYTICS/tableau/dashboard_2_customer_loan_analysis.md):
- **Sheet 1**: Home Ownership Bar/Donut (`RENT`, `MORTGAGE`, `OWN`).
- **Sheet 2**: Employment Length Bar (Tenure sorted `< 1 year` to `10+ years`).
- **Sheet 3**: Verification Status horizontal bars.
- **Sheets 4 & 5**: Income Range dual-axis bar/line (Funded amount & Avg ticket).
- **Sheet 6**: Loan Term donut (36 vs 60 months).
- **Sheet 7**: Top 5 Purposes by Avg Interest Rate.
- **Sheet 8**: Avg DTI by Income Range line chart.
- **Sheets 9 & 10**: Grade loan count and average size.
- **Sheet 11**: Top 10 States by Application Count.

---

## Step 6: Build Worksheets for Dashboard 3 (Risk Analysis)
Build each worksheet following [`dashboard_3_risk_analysis.md`](file:///Users/dineshkumarsingh/Documents/antigravity/goofy-mendeleev/BANK_LOAN_LENDING_DATA_ANALYTICS/tableau/dashboard_3_risk_analysis.md):
- **Sheet 1**: Default Rate by Grade step-bar (A: ~6% to G: ~34%).
- **Sheet 2**: Default Rate by Purpose Top 10 horizontal bar.
- **Sheet 3**: Default Rate by DTI Range column chart.
- **Sheet 4**: Default Rate by Interest Rate Range.
- **Sheet 5**: Gross Charged-off Amount Bar ($65.53M).
- **Sheet 6**: Recovery Rate Bar/Bullet (56.89%).
- **Sheet 7**: Default Rate by Home Ownership.
- **Sheet 8**: Default Rate by Employment Length line chart.
- **Sheet 9**: Default Rate by Income Range.
- **Sheet 10**: High-Risk KPI Summary Card (12,842 loans, $164.2M funded, 22.41% default rate).
- **Sheet 11**: Risk Distribution & Granular Drill-Down Ledger table.

---

## Step 7: Assemble Dashboards & Layout Containers
1. Create New Dashboard -> Set Fixed Size `1600 x 1000` (or `1600 x 1050` for Risk).
2. Drag a **Vertical Container** onto the canvas as the root layout container.
3. Top Header: Add a **Horizontal Container** (`Height: 80px`). Add corporate title and navy blue background fill (`#0F2537`).
4. KPI Row: Add a **Horizontal Container** (`Height: 110px`). Drag the 6 KPI cards side-by-side with even distribution.
5. Filter Sidebar: Add a **Horizontal Container** below KPIs. Place a **Vertical Container** (`Width: 220px`) on the left for filters, and place chart containers on the right.
6. Grid Alignment: Format padding (Outer padding: 4px, Inner padding: 8px) to achieve clean white card separation over the light gray canvas (`#F8FAFC`).

---

## Step 8: Add Interactive Dashboard Actions
Under **Dashboard -> Actions**:
1. **Filter Action `Filter by Status`**: Source = `viz_loan_status_distribution`, Target = All other sheets. Trigger = Select.
2. **Filter Action `Filter by State`**: Source = Top 10 States bar, Target = Monthly trend & purpose. Trigger = Select.
3. **Filter Action `Filter by Risk Segment`**: Source = Risk Segment card, Target = Granular loan ledger. Trigger = Select.
4. **Highlight Action `Highlight Grade`**: Source = Grade bar, Target = All sheets using Grade. Trigger = Hover.

---

## Step 9: Validate Numbers Against MySQL
Audit your visual output against SQL results in `sql/04_kpi_analysis.sql`:
- Total Applications: **38,576**
- Total Funded Amount: **$435,757,075** ($435.8M)
- Total Received Amount: **$473,070,933** ($473.1M)
- Overall Default Rate: **13.82%** (5,333 charged-off loans)
- Overall Avg Interest Rate: **12.05%**
- Overall Avg DTI: **13.33%**
- MTD Dec 2021 Applications: **4,314**
- MTD Dec 2021 Funded: **$53,981,425** ($54.0M)
- MoM Application Growth: **+6.91%**

---

## Step 10: Save & Publish Workbook
- In Tableau Desktop: File -> **Save As** -> `BANK_LOAN_LENDING_DATA_ANALYTICS.twbx` (packaged workbook).
- For Portfolio / GitHub: Server -> Tableau Public -> **Save to Tableau Public As...** to generate a live interactive portfolio link.

