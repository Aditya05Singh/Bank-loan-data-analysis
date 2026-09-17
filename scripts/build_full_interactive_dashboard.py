"""
build_full_interactive_dashboard.py - Compiles an ultra-responsive, fully interactive,
multi-filter executive financial analytics dashboard suite powered by all 38,576 loan records.
Includes 6 dynamic dropdown filters, state filter, quick scenario preset buttons,
click-to-filter on charts/tables, and real-time client-side calculation across all 3 dashboards.
"""

import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "cleaned", "loan_data_cleaned.csv")
HTML_LOCAL = os.path.join(BASE_DIR, "interactive_dashboards.html")
HTML_ARTIFACT = "/Users/dineshkumarsingh/.gemini/antigravity/brain/b6b17943-7266-4136-b4ba-e6d07d76b745/bank_loan_dashboards.html"

def generate_interactive_suite():
    print("Reading cleaned dataset...")
    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Loaded {len(rows)} records. Extracting compact attributes...")
    
    unique_states = sorted(list(set(r['address_state'] for r in rows)))
    
    # Compact record schema:
    # 0: id (int)
    # 1: state (str)
    # 2: grade (str)
    # 3: home_ownership (str)
    # 4: month (int 1-12)
    # 5: loan_status (str)
    # 6: purpose (str)
    # 7: term (int: 36 or 60)
    # 8: verification_status (str)
    # 9: annual_income (float)
    # 10: dti (float)
    # 11: int_rate (float)
    # 12: loan_amount (float)
    # 13: total_payment (float)
    # 14: emp_length (str)
    compact_records = []
    for r in rows:
        compact_records.append([
            int(r['id']),
            r['address_state'],
            r['grade'],
            r['home_ownership'],
            int(r['issue_date'].split('-')[1]),
            r['loan_status'],
            r['purpose'],
            36 if '36' in r['term'] else 60,
            r['verification_status'],
            float(r['annual_income']),
            float(r['dti']),
            float(r['int_rate']),
            float(r['loan_amount']),
            float(r['total_payment']),
            r['emp_length']
        ])
        
    records_json = json.dumps(compact_records)
    states_options_html = "\n".join([f'<option value="{s}">{s}</option>' for s in unique_states])
    print(f"Serialized {len(compact_records)} records into JSON ({len(records_json)/1024/1024:.2f} MB)")

    html_code = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bank Loan Lending Analytics - Interactive 3-Dashboard Executive Suite</title>
    <style>
        :root {{
            --navy-primary: #0F2537;
            --navy-dark: #0A1926;
            --navy-light: #1E3A8A;
            --navy-accent: #2563EB;
            --emerald: #10B981;
            --emerald-bg: #ECFDF5;
            --crimson: #DC2626;
            --crimson-bg: #FEF2F2;
            --amber: #F59E0B;
            --amber-bg: #FFFBEB;
            --slate: #475569;
            --slate-light: #94A3B8;
            --bg-light: #F8FAFC;
            --card-bg: #FFFFFF;
            --border-color: #E2E8F0;
        }}
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }}
        body {{
            background-color: var(--bg-light);
            color: #1E293B;
            padding-bottom: 60px;
        }}
        /* Header */
        header {{
            background: linear-gradient(135deg, var(--navy-primary) 0%, var(--navy-dark) 100%);
            color: #FFFFFF;
            padding: 16px 28px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .header-title h1 {{
            font-size: 20px;
            font-weight: 800;
            letter-spacing: 0.5px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .header-badge {{
            background: rgba(16, 185, 129, 0.2);
            color: #34D399;
            border: 1px solid rgba(16, 185, 129, 0.4);
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 700;
        }}
        .header-title p {{
            font-size: 12px;
            color: #94A3B8;
            margin-top: 3px;
        }}
        /* Tab Navigation */
        .nav-tabs {{
            display: flex;
            gap: 8px;
        }}
        .tab-btn {{
            background: rgba(255, 255, 255, 0.1);
            color: #E2E8F0;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 12px;
            font-weight: 700;
            transition: all 0.2s ease;
        }}
        .tab-btn:hover {{
            background: rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
        }}
        .tab-btn.active {{
            background: #2563EB;
            color: #FFFFFF;
            border-color: #60A5FA;
            box-shadow: 0 2px 6px rgba(37, 99, 235, 0.4);
        }}
        /* Preset Scenarios Toolbar */
        .scenario-bar {{
            background: #0A1926;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding: 10px 28px;
            display: flex;
            align-items: center;
            gap: 8px;
            overflow-x: auto;
        }}
        .scenario-title {{
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 800;
            color: #94A3B8;
            letter-spacing: 0.5px;
            white-space: nowrap;
            margin-right: 4px;
        }}
        .preset-btn {{
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: #CBD5E1;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            white-space: nowrap;
            transition: all 0.2s;
        }}
        .preset-btn:hover {{
            background: rgba(255, 255, 255, 0.2);
            color: #FFFFFF;
            border-color: rgba(255, 255, 255, 0.3);
        }}
        .preset-btn.active {{
            background: #3B82F6;
            color: #FFFFFF;
            border-color: #60A5FA;
            font-weight: 700;
        }}
        .preset-btn.risk-preset {{
            border-color: rgba(220, 38, 38, 0.4);
            color: #FCA5A5;
        }}
        .preset-btn.risk-preset:hover, .preset-btn.risk-preset.active {{
            background: #DC2626;
            color: #FFFFFF;
        }}
        .preset-btn.good-preset {{
            border-color: rgba(16, 185, 129, 0.4);
            color: #6EE7B7;
        }}
        .preset-btn.good-preset:hover, .preset-btn.good-preset.active {{
            background: #10B981;
            color: #FFFFFF;
        }}

        /* Filter Control Bar */
        .filter-bar {{
            background: #FFFFFF;
            border-bottom: 1px solid var(--border-color);
            padding: 12px 28px;
            display: flex;
            flex-wrap: wrap;
            gap: 12px;
            align-items: center;
            box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        }}
        .filter-group {{
            display: flex;
            flex-direction: column;
            gap: 3px;
        }}
        .filter-label {{
            font-size: 10px;
            text-transform: uppercase;
            font-weight: 800;
            color: #64748B;
            letter-spacing: 0.5px;
        }}
        .filter-select {{
            background: #F8FAFC;
            border: 1px solid #CBD5E1;
            padding: 6px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            color: #1E293B;
            outline: none;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .filter-select:focus {{
            border-color: #2563EB;
            background: #FFFFFF;
            box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
        }}
        .reset-btn {{
            background: #F1F5F9;
            color: #475569;
            border: 1px solid #CBD5E1;
            padding: 6px 14px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            cursor: pointer;
            margin-top: 14px;
            transition: all 0.2s;
        }}
        .reset-btn:hover {{
            background: #E2E8F0;
            color: #0F172A;
        }}
        .filter-status {{
            margin-left: auto;
            font-size: 12px;
            font-weight: 700;
            color: #1D4ED8;
            background: #EFF6FF;
            padding: 6px 14px;
            border-radius: 20px;
            border: 1px solid #BFDBFE;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        /* Active Filter Chips */
        .active-chips-bar {{
            background: #F8FAFC;
            border-bottom: 1px solid var(--border-color);
            padding: 8px 28px;
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 11px;
        }}
        .active-chips-title {{
            font-weight: 700;
            color: #64748B;
            font-size: 10px;
            text-transform: uppercase;
        }}
        .chip {{
            background: #DBEAFE;
            color: #1E40AF;
            border: 1px solid #93C5FD;
            padding: 3px 8px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            cursor: pointer;
        }}
        .chip:hover {{
            background: #BFDBFE;
        }}
        .chip-close {{
            font-weight: 800;
            font-size: 12px;
            line-height: 1;
        }}

        /* Dashboard Layout Container */
        .container {{
            max-width: 1600px;
            margin: 20px auto;
            padding: 0 28px;
        }}

        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 14px;
            margin-bottom: 22px;
        }}
        .kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
            position: relative;
            overflow: hidden;
            transition: transform 0.2s, box-shadow 0.2s;
        }}
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 10px rgba(0,0,0,0.06);
        }}
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--navy-accent);
        }}
        .kpi-card.emerald::before {{ background: var(--emerald); }}
        .kpi-card.crimson::before {{ background: var(--crimson); }}
        .kpi-card.amber::before {{ background: var(--amber); }}
        .kpi-label {{
            font-size: 10px;
            text-transform: uppercase;
            font-weight: 800;
            color: #64748B;
            letter-spacing: 0.5px;
        }}
        .kpi-value {{
            font-size: 23px;
            font-weight: 800;
            color: #0F172A;
            margin: 5px 0 2px 0;
        }}
        .kpi-sub {{
            font-size: 11px;
            color: #64748B;
            font-weight: 600;
        }}

        /* Layout Grids */
        .grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 18px;
            margin-bottom: 20px;
        }}
        .grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 18px;
            margin-bottom: 20px;
        }}
        .card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 18px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        }}
        .card-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #F1F5F9;
            padding-bottom: 10px;
            margin-bottom: 14px;
        }}
        .card-title {{
            font-size: 13px;
            font-weight: 800;
            color: #0F172A;
        }}
        .card-subtitle {{
            font-size: 11px;
            color: #64748B;
        }}
        .click-hint {{
            font-size: 10px;
            color: #2563EB;
            font-weight: 600;
            background: #EFF6FF;
            padding: 2px 6px;
            border-radius: 4px;
        }}

        /* Interactive Bars */
        .bar-row {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            font-size: 12px;
            cursor: pointer;
            padding: 2px 4px;
            border-radius: 4px;
            transition: background 0.15s;
        }}
        .bar-row:hover {{
            background: #F1F5F9;
        }}
        .bar-label {{
            width: 140px;
            color: #334155;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .bar-track {{
            flex: 1;
            background: #F1F5F9;
            height: 16px;
            border-radius: 4px;
            overflow: hidden;
            margin: 0 10px;
            border: 1px solid #E2E8F0;
        }}
        .bar-fill {{
            height: 100%;
            background: var(--navy-light);
            border-radius: 3px;
            transition: width 0.35s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        .bar-val {{
            width: 95px;
            text-align: right;
            font-weight: 700;
            color: #0F172A;
            font-size: 11px;
        }}

        /* Data Table */
        table.data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }}
        table.data-table th {{
            background: #F8FAFC;
            color: #475569;
            font-weight: 700;
            text-align: left;
            padding: 8px 10px;
            border-bottom: 2px solid var(--border-color);
        }}
        table.data-table td {{
            padding: 8px 10px;
            border-bottom: 1px solid #F1F5F9;
        }}
        table.data-table tr.clickable-row {{
            cursor: pointer;
            transition: background 0.15s;
        }}
        table.data-table tr.clickable-row:hover {{
            background: #F1F5F9;
        }}

        /* Tab panels */
        .tab-panel {{
            display: none;
        }}
        .tab-panel.active {{
            display: block;
        }}
    </style>
</head>
<body>

    <!-- Header -->
    <header>
        <div class="header-title">
            <h1>BANK LOAN LENDING DATA ANALYTICS <span class="header-badge">LIVE INTERACTIVE</span></h1>
            <p>Interactive Multi-Filter Executive Reporting Suite | Powered by All 38,576 Production Records</p>
        </div>
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="switchTab('tab1', this)">1. Portfolio Overview</button>
            <button class="tab-btn" onclick="switchTab('tab2', this)">2. Customer & Loan Analysis</button>
            <button class="tab-btn" onclick="switchTab('tab3', this)">3. Risk Analysis</button>
        </div>
    </header>

    <!-- Quick Scenario Presets Toolbar -->
    <div class="scenario-bar">
        <span class="scenario-title">Scenario Presets:</span>
        <button class="preset-btn active" onclick="runPreset('ALL')">All Loans (Reset)</button>
        <button class="preset-btn good-preset" onclick="runPreset('PRIME')">Prime Portfolio (Grades A-B)</button>
        <button class="preset-btn" onclick="runPreset('NEAR_PRIME')">Near-Prime (Grade C)</button>
        <button class="preset-btn risk-preset" onclick="runPreset('HIGH_RISK')">High Risk (Grades D-G)</button>
        <button class="preset-btn risk-preset" onclick="runPreset('DEFAULTS')">Charged-Off Defaults</button>
        <button class="preset-btn good-preset" onclick="runPreset('FULLY_PAID')">Fully Paid</button>
        <button class="preset-btn" onclick="runPreset('TERM_36')">36-Month Short Term</button>
        <button class="preset-btn" onclick="runPreset('TERM_60')">60-Month Long Term</button>
        <button class="preset-btn" onclick="runPreset('PURPOSE_DEBT')">Debt Consolidation</button>
        <button class="preset-btn" onclick="runPreset('STATE_CA')">California (CA)</button>
        <button class="preset-btn" onclick="runPreset('STATE_NY')">New York (NY)</button>
    </div>

    <!-- Interactive Multi-Filter Control Panel -->
    <div class="filter-bar">
        <div class="filter-group">
            <label class="filter-label">Credit Grade</label>
            <select id="filter-grade" class="filter-select" onchange="applyFilters()">
                <option value="ALL">All Grades (A - G)</option>
                <option value="A">Grade A (Prime)</option>
                <option value="B">Grade B</option>
                <option value="C">Grade C</option>
                <option value="D">Grade D</option>
                <option value="E">Grade E</option>
                <option value="F">Grade F</option>
                <option value="G">Grade G (Subprime)</option>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">Loan Status</label>
            <select id="filter-status" class="filter-select" onchange="applyFilters()">
                <option value="ALL">All Statuses</option>
                <option value="Fully Paid">Fully Paid</option>
                <option value="Current">Current</option>
                <option value="Charged Off">Charged Off (Default)</option>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">Borrowing Purpose</label>
            <select id="filter-purpose" class="filter-select" onchange="applyFilters()">
                <option value="ALL">All Purposes</option>
                <option value="Debt Consolidation">Debt Consolidation</option>
                <option value="Credit Card">Credit Card</option>
                <option value="Home Improvement">Home Improvement</option>
                <option value="Major Purchase">Major Purchase</option>
                <option value="Small Business">Small Business</option>
                <option value="Car">Car</option>
                <option value="Wedding">Wedding</option>
                <option value="Medical">Medical</option>
                <option value="Moving">Moving</option>
                <option value="Vacation">Vacation</option>
                <option value="House">House</option>
                <option value="Educational">Educational</option>
                <option value="Renewable Energy">Renewable Energy</option>
                <option value="Other">Other</option>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">Home Ownership</label>
            <select id="filter-home" class="filter-select" onchange="applyFilters()">
                <option value="ALL">All Ownership</option>
                <option value="RENT">RENT</option>
                <option value="MORTGAGE">MORTGAGE</option>
                <option value="OWN">OWN</option>
                <option value="OTHER">OTHER / NONE</option>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">Repayment Term</label>
            <select id="filter-term" class="filter-select" onchange="applyFilters()">
                <option value="ALL">All Terms</option>
                <option value="36">36 Months</option>
                <option value="60">60 Months</option>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">Verification</label>
            <select id="filter-verif" class="filter-select" onchange="applyFilters()">
                <option value="ALL">All Verification</option>
                <option value="Verified">Verified</option>
                <option value="Source Verified">Source Verified</option>
                <option value="Not Verified">Not Verified</option>
            </select>
        </div>

        <div class="filter-group">
            <label class="filter-label">State</label>
            <select id="filter-state" class="filter-select" onchange="applyFilters()">
                <option value="ALL">All States (50)</option>
                {states_options_html}
            </select>
        </div>

        <button class="reset-btn" onclick="resetAllFilters()">Reset Filters</button>

        <div id="filter-status-display" class="filter-status">
            Showing 38,576 of 38,576 Records (100.0%)
        </div>
    </div>

    <!-- Active Filters Tag Bar -->
    <div id="active-chips-bar" class="active-chips-bar" style="display: none;">
        <span class="active-chips-title">Active Filters:</span>
        <div id="chips-container" style="display: flex; gap: 6px; flex-wrap: wrap;"></div>
    </div>

    <!-- Dashboard Content Container -->
    <div class="container">

        <!-- ======================================================== -->
        <!-- DASHBOARD 1: PORTFOLIO OVERVIEW -->
        <!-- ======================================================== -->
        <div id="tab1" class="tab-panel active">
            <!-- 6 Dynamic Financial KPI Cards -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">Total Applications</div>
                    <div id="kpi-apps" class="kpi-value">38,576</div>
                    <div id="kpi-apps-sub" class="kpi-sub">Month 12 (Dec): 4,314 apps</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Total Funded Capital</div>
                    <div id="kpi-funded" class="kpi-value">$435.8M</div>
                    <div id="kpi-funded-sub" class="kpi-sub">Month 12 (Dec): $54.0M</div>
                </div>
                <div class="kpi-card emerald">
                    <div class="kpi-label">Total Cash Received</div>
                    <div id="kpi-received" class="kpi-value">$473.1M</div>
                    <div id="kpi-received-sub" class="kpi-sub">Month 12 (Dec): $58.1M</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Average Interest Rate</div>
                    <div id="kpi-rate" class="kpi-value">12.05%</div>
                    <div class="kpi-sub">Weighted Portfolio Mean</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Average Ticket Size</div>
                    <div id="kpi-avg-loan" class="kpi-value">$11,296</div>
                    <div class="kpi-sub">Per Funded Loan Application</div>
                </div>
                <div class="kpi-card crimson">
                    <div class="kpi-label">Default Rate</div>
                    <div id="kpi-default" class="kpi-value">13.82%</div>
                    <div id="kpi-default-sub" class="kpi-sub">5,333 Defaults | Net Loss: $28.25M</div>
                </div>
            </div>

            <!-- Charts Row 1 -->
            <div class="grid-2">
                <!-- Status Distribution Table -->
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 7: Loan Status Distribution</div>
                            <div class="card-subtitle">Good vs Bad Allocation (Click any row to filter by status)</div>
                        </div>
                        <span class="click-hint">Click Row to Filter</span>
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Loan Status</th>
                                <th style="text-align: right;">Volume</th>
                                <th style="text-align: right;">Share %</th>
                                <th style="text-align: right;">Funded Capital</th>
                                <th style="text-align: right;">Cash Received</th>
                            </tr>
                        </thead>
                        <tbody id="table-status-body">
                            <!-- Populated dynamically -->
                        </tbody>
                    </table>
                </div>

                <!-- Monthly Funded Progression -->
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 8: Monthly Capital Pacing (2021)</div>
                            <div class="card-subtitle">Funded Capital by Month ($ Millions)</div>
                        </div>
                    </div>
                    <div id="monthly-chart-container"></div>
                </div>
            </div>

            <!-- Charts Row 2 -->
            <div class="grid-3">
                <!-- Quarterly Pacing -->
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 9: Quarterly Volume</div>
                            <div class="card-subtitle">Funded Capital by Quarter</div>
                        </div>
                    </div>
                    <div id="quarterly-chart-container"></div>
                </div>

                <!-- Top States -->
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 11: Top 10 States by Capital</div>
                            <div class="card-subtitle">Geographic Concentration (Click bar to filter)</div>
                        </div>
                        <span class="click-hint">Click to Filter</span>
                    </div>
                    <div id="states-chart-container"></div>
                </div>

                <!-- Top Purposes -->
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Top Loan Purposes</div>
                            <div class="card-subtitle">Capital Allocation (Click bar to filter)</div>
                        </div>
                        <span class="click-hint">Click to Filter</span>
                    </div>
                    <div id="purposes-chart-container"></div>
                </div>
            </div>
        </div>

        <!-- ======================================================== -->
        <!-- DASHBOARD 2: CUSTOMER & LOAN ANALYSIS -->
        <!-- ======================================================== -->
        <div id="tab2" class="tab-panel">
            <div class="grid-3">
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 1: Home Ownership</div>
                            <div class="card-subtitle">Collateral Distribution (Click to filter)</div>
                        </div>
                        <span class="click-hint">Click to Filter</span>
                    </div>
                    <div id="cust-home-container"></div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 2: Employment Tenure</div>
                            <div class="card-subtitle">Borrower Job Stability Breakdown</div>
                        </div>
                    </div>
                    <div id="cust-emp-container"></div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 3: Verification Status</div>
                            <div class="card-subtitle">Underwriting Rigor (Click to filter)</div>
                        </div>
                        <span class="click-hint">Click to Filter</span>
                    </div>
                    <div id="cust-verif-container"></div>
                </div>
            </div>

            <div class="grid-3">
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 4: Avg Loan by Income Tier</div>
                            <div class="card-subtitle">Borrower Ticket Size Capacity</div>
                        </div>
                    </div>
                    <div id="cust-income-container"></div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 6: Repayment Term</div>
                            <div class="card-subtitle">Contractual Duration (Click to filter)</div>
                        </div>
                        <span class="click-hint">Click to Filter</span>
                    </div>
                    <div id="cust-term-container"></div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 9: Volume by Credit Grade</div>
                            <div class="card-subtitle">Credit Rating Split (Click to filter)</div>
                        </div>
                        <span class="click-hint">Click to Filter</span>
                    </div>
                    <div id="cust-grade-container"></div>
                </div>
            </div>
        </div>

        <!-- ======================================================== -->
        <!-- DASHBOARD 3: RISK ANALYSIS -->
        <!-- ======================================================== -->
        <div id="tab3" class="tab-panel">
            <!-- High Risk KPI Block -->
            <div class="grid-3" style="margin-bottom: 22px;">
                <div class="card" style="border-left: 4px solid var(--crimson); background: #FEF2F2;">
                    <div class="kpi-label" style="color: var(--crimson);">Total High-Risk Loans</div>
                    <div id="hr-count" class="kpi-value" style="color: var(--crimson);">12,842</div>
                    <div id="hr-pct" class="kpi-sub">33.29% of Filtered Portfolio</div>
                </div>
                <div class="card" style="border-left: 4px solid var(--crimson); background: #FEF2F2;">
                    <div class="kpi-label" style="color: var(--crimson);">High-Risk Funded Capital</div>
                    <div id="hr-funded" class="kpi-value" style="color: var(--crimson);">$164.2M</div>
                    <div id="hr-funded-pct" class="kpi-sub">37.69% of Filtered Capital</div>
                </div>
                <div class="card" style="border-left: 4px solid var(--crimson); background: #FEF2F2;">
                    <div class="kpi-label" style="color: var(--crimson);">High-Risk Default Rate</div>
                    <div id="hr-rate" class="kpi-value" style="color: var(--crimson);">22.41%</div>
                    <div id="hr-rate-sub" class="kpi-sub">2,878 Defaults in Segment</div>
                </div>
            </div>

            <div class="grid-2">
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 1: Default Rate by Credit Grade (A - G)</div>
                            <div class="card-subtitle">Monotonic Risk Escalation (Click bar to filter)</div>
                        </div>
                        <span class="click-hint">Click to Filter</span>
                    </div>
                    <div id="risk-grade-container"></div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 2: Default Rate by Borrowing Purpose</div>
                            <div class="card-subtitle">Highest Risk Loan Categories (Click bar to filter)</div>
                        </div>
                        <span class="click-hint">Click to Filter</span>
                    </div>
                    <div id="risk-purpose-container"></div>
                </div>
            </div>

            <div class="grid-2">
                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 5 & 6: Loss Given Default (LGD)</div>
                            <div class="card-subtitle">Defaults vs Cash Recoveries Recouped</div>
                        </div>
                    </div>
                    <div id="risk-recovery-container"></div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <div>
                            <div class="card-title">Area 3: Default Rate by DTI Leverage</div>
                            <div class="card-subtitle">Debt Burden Default Sensitivity</div>
                        </div>
                    </div>
                    <div id="risk-dti-container"></div>
                </div>
            </div>
        </div>

    </div>

    <!-- Embedded Data & In-Memory Real-Time Filtering Engine -->
    <script>
        // Compact dataset records:
        // [id, state, grade, home, month, status, purpose, term, verif, income, dti, rate, amount, payment, emp_length]
        const rawData = {records_json};

        // Navigation
        function switchTab(tabId, btn) {{
            document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }}

        // Scenario Presets
        function runPreset(preset) {{
            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
            
            // First reset all controls
            document.getElementById('filter-grade').value = 'ALL';
            document.getElementById('filter-status').value = 'ALL';
            document.getElementById('filter-purpose').value = 'ALL';
            document.getElementById('filter-home').value = 'ALL';
            document.getElementById('filter-term').value = 'ALL';
            document.getElementById('filter-verif').value = 'ALL';
            document.getElementById('filter-state').value = 'ALL';

            if (preset === 'PRIME') {{
                document.getElementById('filter-grade').value = 'A';
            }} else if (preset === 'NEAR_PRIME') {{
                document.getElementById('filter-grade').value = 'C';
            }} else if (preset === 'HIGH_RISK') {{
                document.getElementById('filter-grade').value = 'E';
            }} else if (preset === 'DEFAULTS') {{
                document.getElementById('filter-status').value = 'Charged Off';
            }} else if (preset === 'FULLY_PAID') {{
                document.getElementById('filter-status').value = 'Fully Paid';
            }} else if (preset === 'TERM_36') {{
                document.getElementById('filter-term').value = '36';
            }} else if (preset === 'TERM_60') {{
                document.getElementById('filter-term').value = '60';
            }} else if (preset === 'PURPOSE_DEBT') {{
                document.getElementById('filter-purpose').value = 'Debt Consolidation';
            }} else if (preset === 'STATE_CA') {{
                document.getElementById('filter-state').value = 'CA';
            }} else if (preset === 'STATE_NY') {{
                document.getElementById('filter-state').value = 'NY';
            }}

            if (event && event.target) {{
                event.target.classList.add('active');
            }}

            applyFilters();
        }}

        // Direct Filter Setters (for click-to-filter on charts)
        function setFilter(filterId, value) {{
            document.getElementById(filterId).value = value;
            applyFilters();
        }}

        // Filter Execution
        function applyFilters() {{
            const fGrade = document.getElementById('filter-grade').value;
            const fStatus = document.getElementById('filter-status').value;
            const fPurpose = document.getElementById('filter-purpose').value;
            const fHome = document.getElementById('filter-home').value;
            const fTerm = document.getElementById('filter-term').value;
            const fVerif = document.getElementById('filter-verif').value;
            const fState = document.getElementById('filter-state').value;

            // In-memory filter execution across all 38,576 records
            const filtered = rawData.filter(r => {{
                if (fGrade !== 'ALL' && r[2] !== fGrade) return false;
                if (fStatus !== 'ALL' && r[5] !== fStatus) return false;
                if (fPurpose !== 'ALL' && r[6] !== fPurpose) return false;
                if (fHome !== 'ALL') {{
                    if (fHome === 'OTHER' && !['OTHER', 'NONE'].includes(r[3])) return false;
                    if (fHome !== 'OTHER' && r[3] !== fHome) return false;
                }}
                if (fTerm !== 'ALL' && r[7] !== parseInt(fTerm)) return false;
                if (fVerif !== 'ALL' && r[8] !== fVerif) return false;
                if (fState !== 'ALL' && r[1] !== fState) return false;
                return true;
            }});

            renderActiveChips(fGrade, fStatus, fPurpose, fHome, fTerm, fVerif, fState);
            renderDashboard(filtered);
        }}

        function renderActiveChips(g, s, p, h, t, v, st) {{
            const chipsContainer = document.getElementById('chips-container');
            const chipsBar = document.getElementById('active-chips-bar');
            let chips = [];

            if (g !== 'ALL') chips.push([`Grade: ${{g}}`, 'filter-grade']);
            if (s !== 'ALL') chips.push([`Status: ${{s}}`, 'filter-status']);
            if (p !== 'ALL') chips.push([`Purpose: ${{p}}`, 'filter-purpose']);
            if (h !== 'ALL') chips.push([`Home: ${{h}}`, 'filter-home']);
            if (t !== 'ALL') chips.push([`Term: ${{t}}M`, 'filter-term']);
            if (v !== 'ALL') chips.push([`Verif: ${{v}}`, 'filter-verif']);
            if (st !== 'ALL') chips.push([`State: ${{st}}`, 'filter-state']);

            if (chips.length === 0) {{
                chipsBar.style.display = 'none';
            }} else {{
                chipsBar.style.display = 'flex';
                chipsContainer.innerHTML = chips.map(([label, fId]) => `
                    <div class="chip" onclick="setFilter('${{fId}}', 'ALL')">
                        ${{label}} <span class="chip-close">&times;</span>
                    </div>
                `).join('');
            }}
        }}

        function resetAllFilters() {{
            document.getElementById('filter-grade').value = 'ALL';
            document.getElementById('filter-status').value = 'ALL';
            document.getElementById('filter-purpose').value = 'ALL';
            document.getElementById('filter-home').value = 'ALL';
            document.getElementById('filter-term').value = 'ALL';
            document.getElementById('filter-verif').value = 'ALL';
            document.getElementById('filter-state').value = 'ALL';
            
            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
            const defaultBtn = document.querySelector('.preset-btn');
            if (defaultBtn) defaultBtn.classList.add('active');

            applyFilters();
        }}

        // Dynamic Aggregator & Renderer
        function renderDashboard(data) {{
            const totalCount = data.length;
            const pctShare = (totalCount / rawData.length * 100).toFixed(1);
            document.getElementById('filter-status-display').textContent = `Showing ${{totalCount.toLocaleString()}} of ${{rawData.length.toLocaleString()}} Records (${{pctShare}}%)`;

            if (totalCount === 0) {{
                document.getElementById('kpi-apps').textContent = '0';
                document.getElementById('kpi-funded').textContent = '$0.0M';
                document.getElementById('kpi-received').textContent = '$0.0M';
                document.getElementById('kpi-rate').textContent = '0.00%';
                document.getElementById('kpi-avg-loan').textContent = '$0';
                document.getElementById('kpi-default').textContent = '0.00%';
                document.getElementById('kpi-default-sub').textContent = '0 Defaults';
                document.getElementById('table-status-body').innerHTML = '<tr><td colspan="5" style="text-align:center;padding:20px;color:#94A3B8;">No records match the active filter criteria</td></tr>';
                document.getElementById('monthly-chart-container').innerHTML = '<p style="font-size:11px;color:#94A3B8;padding:10px;">No records</p>';
                document.getElementById('quarterly-chart-container').innerHTML = '<p style="font-size:11px;color:#94A3B8;padding:10px;">No records</p>';
                document.getElementById('states-chart-container').innerHTML = '<p style="font-size:11px;color:#94A3B8;padding:10px;">No records</p>';
                document.getElementById('purposes-chart-container').innerHTML = '<p style="font-size:11px;color:#94A3B8;padding:10px;">No records</p>';
                return;
            }}

            // Calculations
            let totFunded = 0, totReceived = 0, sumRate = 0, defCount = 0, defFunded = 0, defReceived = 0;
            let fpCount = 0, fpFunded = 0, fpReceived = 0;
            let curCount = 0, curFunded = 0, curReceived = 0;

            let mtdApps = 0, mtdFunded = 0, mtdReceived = 0;

            const monthlyFunded = Array(12).fill(0);
            const stateFunded = {{}};
            const purposeFunded = {{}};
            const purposeDefaults = {{}};
            const purposeCounts = {{}};
            const gradeCounts = {{}};
            const gradeDefaults = {{}};
            const homeCounts = {{'RENT': 0, 'MORTGAGE': 0, 'OWN': 0, 'OTHER': 0}};
            const empCounts = {{'< 1 year': 0, '1-3 years': 0, '4-6 years': 0, '7-9 years': 0, '10+ years': 0}};
            const verifCounts = {{'Verified': 0, 'Source Verified': 0, 'Not Verified': 0}};
            const termCounts = {{36: 0, 60: 0}};
            const incomeAmounts = {{'Under $30k': [], '$30k-$60k': [], '$60k-$90k': [], '$90k-$120k': [], '$120k+': []}};
            const dtiDefaults = {{'&lt; 10%': [0,0], '10% - 15%': [0,0], '15% - 20%': [0,0], '20% - 25%': [0,0], '&ge; 25%': [0,0]}};

            let hrCount = 0, hrFunded = 0, hrDefaults = 0;

            for (let i = 0; i < data.length; i++) {{
                const r = data[i];
                const amt = r[12];
                const pay = r[13];
                const st = r[5];
                const m = r[4] - 1;
                const g = r[2];
                const p = r[6];
                const dti = r[10];
                const el = r[14];

                totFunded += amt;
                totReceived += pay;
                sumRate += r[11];

                // Month 12 (December) MTD
                if (r[4] === 12) {{
                    mtdApps++;
                    mtdFunded += amt;
                    mtdReceived += pay;
                }}

                if (st === 'Charged Off') {{
                    defCount++;
                    defFunded += amt;
                    defReceived += pay;
                }} else if (st === 'Fully Paid') {{
                    fpCount++;
                    fpFunded += amt;
                    fpReceived += pay;
                }} else if (st === 'Current') {{
                    curCount++;
                    curFunded += amt;
                    curReceived += pay;
                }}

                if (m >= 0 && m < 12) monthlyFunded[m] += amt;
                stateFunded[r[1]] = (stateFunded[r[1]] || 0) + amt;

                purposeFunded[p] = (purposeFunded[p] || 0) + amt;
                purposeCounts[p] = (purposeCounts[p] || 0) + 1;
                if (st === 'Charged Off') purposeDefaults[p] = (purposeDefaults[p] || 0) + 1;

                gradeCounts[g] = (gradeCounts[g] || 0) + 1;
                if (st === 'Charged Off') gradeDefaults[g] = (gradeDefaults[g] || 0) + 1;

                const h = ['RENT', 'MORTGAGE', 'OWN'].includes(r[3]) ? r[3] : 'OTHER';
                homeCounts[h]++;

                // Employment Tenure
                if (el === '< 1 year') empCounts['< 1 year']++;
                else if (['1 year', '2 years', '3 years'].includes(el)) empCounts['1-3 years']++;
                else if (['4 years', '5 years', '6 years'].includes(el)) empCounts['4-6 years']++;
                else if (['7 years', '8 years', '9 years'].includes(el)) empCounts['7-9 years']++;
                else if (el === '10+ years') empCounts['10+ years']++;

                if (verifCounts[r[8]] !== undefined) verifCounts[r[8]]++;
                if (termCounts[r[7]] !== undefined) termCounts[r[7]]++;

                // Income brackets
                const inc = r[9];
                if (inc < 30000) incomeAmounts['Under $30k'].push(amt);
                else if (inc < 60000) incomeAmounts['$30k-$60k'].push(amt);
                else if (inc < 90000) incomeAmounts['$60k-$90k'].push(amt);
                else if (inc < 120000) incomeAmounts['$90k-$120k'].push(amt);
                else incomeAmounts['$120k+'].push(amt);

                // DTI
                let dtiKey = '&lt; 10%';
                if (dti >= 0.25) dtiKey = '&ge; 25%';
                else if (dti >= 0.20) dtiKey = '20% - 25%';
                else if (dti >= 0.15) dtiKey = '15% - 20%';
                else if (dti >= 0.10) dtiKey = '10% - 15%';
                dtiDefaults[dtiKey][1]++;
                if (st === 'Charged Off') dtiDefaults[dtiKey][0]++;

                // High Risk (DTI >= 0.20 or Grade D-G)
                if (dti >= 0.20 || ['D','E','F','G'].includes(g)) {{
                    hrCount++;
                    hrFunded += amt;
                    if (st === 'Charged Off') hrDefaults++;
                }}
            }}

            const avgRate = sumRate / totalCount * 100;
            const avgLoan = totFunded / totalCount;
            const defRate = defCount / totalCount * 100;
            const recRate = defFunded > 0 ? (defReceived / defFunded * 100) : 0;
            const netLoss = defFunded - defReceived;

            // Update KPI Cards
            document.getElementById('kpi-apps').textContent = totalCount.toLocaleString();
            document.getElementById('kpi-apps-sub').textContent = `Month 12 (Dec): ${{mtdApps.toLocaleString()}} apps`;

            document.getElementById('kpi-funded').textContent = `$${{(totFunded/1e6).toFixed(1)}}M`;
            document.getElementById('kpi-funded-sub').textContent = `Month 12 (Dec): $${{(mtdFunded/1e6).toFixed(1)}}M`;

            document.getElementById('kpi-received').textContent = `$${{(totReceived/1e6).toFixed(1)}}M`;
            document.getElementById('kpi-received-sub').textContent = `Month 12 (Dec): $${{(mtdReceived/1e6).toFixed(1)}}M`;

            document.getElementById('kpi-rate').textContent = `${{avgRate.toFixed(2)}}%`;
            document.getElementById('kpi-avg-loan').textContent = `$${{Math.round(avgLoan).toLocaleString()}}`;

            document.getElementById('kpi-default').textContent = `${{defRate.toFixed(2)}}%`;
            document.getElementById('kpi-default-sub').textContent = `${{defCount.toLocaleString()}} Defaults | Loss: $${{(netLoss/1e6).toFixed(2)}}M`;

            // Dashboard 1: Table Status (Clickable rows)
            document.getElementById('table-status-body').innerHTML = `
                <tr class="clickable-row" onclick="setFilter('filter-status', 'Fully Paid')">
                    <td style="font-weight: 700; color: var(--emerald);">Fully Paid</td>
                    <td style="text-align: right;">${{fpCount.toLocaleString()}}</td>
                    <td style="text-align: right;">${{(fpCount/totalCount*100).toFixed(1)}}%</td>
                    <td style="text-align: right;">$${{(fpFunded/1e6).toFixed(2)}}M</td>
                    <td style="text-align: right; color: var(--emerald); font-weight: 600;">$${{(fpReceived/1e6).toFixed(2)}}M</td>
                </tr>
                <tr class="clickable-row" onclick="setFilter('filter-status', 'Current')">
                    <td style="font-weight: 700; color: #2563EB;">Current</td>
                    <td style="text-align: right;">${{curCount.toLocaleString()}}</td>
                    <td style="text-align: right;">${{(curCount/totalCount*100).toFixed(1)}}%</td>
                    <td style="text-align: right;">$${{(curFunded/1e6).toFixed(2)}}M</td>
                    <td style="text-align: right; color: #2563EB; font-weight: 600;">$${{(curReceived/1e6).toFixed(2)}}M</td>
                </tr>
                <tr class="clickable-row" onclick="setFilter('filter-status', 'Charged Off')" style="background: #FEF2F2;">
                    <td style="font-weight: 700; color: var(--crimson);">Charged Off</td>
                    <td style="text-align: right; color: var(--crimson); font-weight: 700;">${{defCount.toLocaleString()}}</td>
                    <td style="text-align: right; color: var(--crimson); font-weight: 700;">${{defRate.toFixed(1)}}%</td>
                    <td style="text-align: right; color: var(--crimson); font-weight: 700;">$${{(defFunded/1e6).toFixed(2)}}M</td>
                    <td style="text-align: right; color: #475569; font-weight: 600;">$${{(defReceived/1e6).toFixed(2)}}M</td>
                </tr>
            `;

            // Dashboard 1: Monthly Bars
            const mNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
            const maxM = Math.max(...monthlyFunded, 1);
            let mHtml = '';
            for (let i = 0; i < 12; i++) {{
                const pct = (monthlyFunded[i] / maxM * 100).toFixed(1);
                mHtml += `<div class="bar-row"><div class="bar-label" style="width:40px;">${{mNames[i]}}</div><div class="bar-track"><div class="bar-fill" style="width:${{pct}}%;"></div></div><div class="bar-val">$${{(monthlyFunded[i]/1e6).toFixed(1)}}M</div></div>`;
            }}
            document.getElementById('monthly-chart-container').innerHTML = mHtml;

            // Dashboard 1: Quarterly
            const q1 = monthlyFunded.slice(0,3).reduce((a,b)=>a+b,0);
            const q2 = monthlyFunded.slice(3,6).reduce((a,b)=>a+b,0);
            const q3 = monthlyFunded.slice(6,9).reduce((a,b)=>a+b,0);
            const q4 = monthlyFunded.slice(9,12).reduce((a,b)=>a+b,0);
            const maxQ = Math.max(q1, q2, q3, q4, 1);
            document.getElementById('quarterly-chart-container').innerHTML = `
                <div class="bar-row"><div class="bar-label">Q1 (Jan-Mar)</div><div class="bar-track"><div class="bar-fill" style="width:${{(q1/maxQ*100).toFixed(1)}}%;"></div></div><div class="bar-val">$${{(q1/1e6).toFixed(1)}}M</div></div>
                <div class="bar-row"><div class="bar-label">Q2 (Apr-Jun)</div><div class="bar-track"><div class="bar-fill" style="width:${{(q2/maxQ*100).toFixed(1)}}%;"></div></div><div class="bar-val">$${{(q2/1e6).toFixed(1)}}M</div></div>
                <div class="bar-row"><div class="bar-label">Q3 (Jul-Sep)</div><div class="bar-track"><div class="bar-fill" style="width:${{(q3/maxQ*100).toFixed(1)}}%;"></div></div><div class="bar-val">$${{(q3/1e6).toFixed(1)}}M</div></div>
                <div class="bar-row"><div class="bar-label">Q4 (Oct-Dec)</div><div class="bar-track"><div class="bar-fill" style="width:${{(q4/maxQ*100).toFixed(1)}}%; background: var(--navy-accent);"></div></div><div class="bar-val">$${{(q4/1e6).toFixed(1)}}M</div></div>
            `;

            // Dashboard 1: Top 10 States (Clickable to filter)
            const sortedStates = Object.entries(stateFunded).sort((a,b)=>b[1]-a[1]).slice(0,10);
            const maxSt = sortedStates.length > 0 ? sortedStates[0][1] : 1;
            let stHtml = '';
            for (const [st, val] of sortedStates) {{
                const pct = (val / totFunded * 100).toFixed(1);
                stHtml += `<div class="bar-row" onclick="setFilter('filter-state', '${{st}}')"><div class="bar-label">${{st}} (${{pct}}%)</div><div class="bar-track"><div class="bar-fill" style="width:${{(val/maxSt*100).toFixed(1)}}%;"></div></div><div class="bar-val">$${{(val/1e6).toFixed(1)}}M</div></div>`;
            }}
            document.getElementById('states-chart-container').innerHTML = stHtml || '<p style="font-size:11px;color:#94A3B8;">No state data</p>';

            // Dashboard 1: Top Purposes (Clickable to filter)
            const sortedPurposes = Object.entries(purposeFunded).sort((a,b)=>b[1]-a[1]).slice(0,5);
            const maxP = sortedPurposes.length > 0 ? sortedPurposes[0][1] : 1;
            let pHtml = '';
            for (const [p, val] of sortedPurposes) {{
                pHtml += `<div class="bar-row" onclick="setFilter('filter-purpose', '${{p}}')"><div class="bar-label" title="${{p}}">${{p}}</div><div class="bar-track"><div class="bar-fill" style="width:${{(val/maxP*100).toFixed(1)}}%; background: #4F46E5;"></div></div><div class="bar-val">$${{(val/1e6).toFixed(1)}}M</div></div>`;
            }}
            document.getElementById('purposes-chart-container').innerHTML = pHtml || '<p style="font-size:11px;color:#94A3B8;">No purpose data</p>';

            // Dashboard 2: Demographics - Home Ownership (Clickable)
            const maxH = Math.max(...Object.values(homeCounts), 1);
            document.getElementById('cust-home-container').innerHTML = `
                <div class="bar-row" onclick="setFilter('filter-home', 'RENT')"><div class="bar-label">RENT</div><div class="bar-track"><div class="bar-fill" style="width:${{(homeCounts['RENT']/maxH*100).toFixed(1)}}%; background: #3B82F6;"></div></div><div class="bar-val">${{homeCounts['RENT'].toLocaleString()}}</div></div>
                <div class="bar-row" onclick="setFilter('filter-home', 'MORTGAGE')"><div class="bar-label">MORTGAGE</div><div class="bar-track"><div class="bar-fill" style="width:${{(homeCounts['MORTGAGE']/maxH*100).toFixed(1)}}%; background: #1E40AF;"></div></div><div class="bar-val">${{homeCounts['MORTGAGE'].toLocaleString()}}</div></div>
                <div class="bar-row" onclick="setFilter('filter-home', 'OWN')"><div class="bar-label">OWN</div><div class="bar-track"><div class="bar-fill" style="width:${{(homeCounts['OWN']/maxH*100).toFixed(1)}}%; background: var(--emerald);"></div></div><div class="bar-val">${{homeCounts['OWN'].toLocaleString()}}</div></div>
                <div class="bar-row" onclick="setFilter('filter-home', 'OTHER')"><div class="bar-label">OTHER / NONE</div><div class="bar-track"><div class="bar-fill" style="width:${{(homeCounts['OTHER']/maxH*100).toFixed(1)}}%; background: #94A3B8;"></div></div><div class="bar-val">${{homeCounts['OTHER'].toLocaleString()}}</div></div>
            `;

            // Dashboard 2: Employment Tenure (Calculated Dynamically!)
            const maxEmp = Math.max(...Object.values(empCounts), 1);
            let empHtml = '';
            for (const [tier, count] of Object.entries(empCounts)) {{
                const pct = (count / totalCount * 100).toFixed(1);
                empHtml += `<div class="bar-row"><div class="bar-label">${{tier}}</div><div class="bar-track"><div class="bar-fill" style="width:${{(count/maxEmp*100).toFixed(1)}}%; background: #059669;"></div></div><div class="bar-val">${{pct}}% (${{count.toLocaleString()}})</div></div>`;
            }}
            document.getElementById('cust-emp-container').innerHTML = empHtml;

            // Dashboard 2: Verification (Clickable)
            const maxV = Math.max(...Object.values(verifCounts), 1);
            document.getElementById('cust-verif-container').innerHTML = `
                <div class="bar-row" onclick="setFilter('filter-verif', 'Not Verified')"><div class="bar-label">Not Verified</div><div class="bar-track"><div class="bar-fill" style="width:${{(verifCounts['Not Verified']/maxV*100).toFixed(1)}}%; background: #94A3B8;"></div></div><div class="bar-val">${{verifCounts['Not Verified'].toLocaleString()}}</div></div>
                <div class="bar-row" onclick="setFilter('filter-verif', 'Verified')"><div class="bar-label">Verified</div><div class="bar-track"><div class="bar-fill" style="width:${{(verifCounts['Verified']/maxV*100).toFixed(1)}}%; background: #2563EB;"></div></div><div class="bar-val">${{verifCounts['Verified'].toLocaleString()}}</div></div>
                <div class="bar-row" onclick="setFilter('filter-verif', 'Source Verified')"><div class="bar-label">Source Verified</div><div class="bar-track"><div class="bar-fill" style="width:${{(verifCounts['Source Verified']/maxV*100).toFixed(1)}}%; background: #0D9488;"></div></div><div class="bar-val">${{verifCounts['Source Verified'].toLocaleString()}}</div></div>
            `;

            // Dashboard 2: Term (Clickable)
            const maxT = Math.max(termCounts[36], termCounts[60], 1);
            document.getElementById('cust-term-container').innerHTML = `
                <div class="bar-row" onclick="setFilter('filter-term', '36')"><div class="bar-label">36 Months</div><div class="bar-track"><div class="bar-fill" style="width:${{(termCounts[36]/maxT*100).toFixed(1)}}%; background: #3B82F6;"></div></div><div class="bar-val">${{termCounts[36].toLocaleString()}} (${{(termCounts[36]/totalCount*100).toFixed(1)}}%)</div></div>
                <div class="bar-row" onclick="setFilter('filter-term', '60')"><div class="bar-label">60 Months</div><div class="bar-track"><div class="bar-fill" style="width:${{(termCounts[60]/maxT*100).toFixed(1)}}%; background: #F59E0B;"></div></div><div class="bar-val">${{termCounts[60].toLocaleString()}} (${{(termCounts[60]/totalCount*100).toFixed(1)}}%)</div></div>
            `;

            // Dashboard 2: Grade counts (Clickable)
            const allGrades = ['A','B','C','D','E','F','G'];
            const maxG = Math.max(...allGrades.map(g => gradeCounts[g] || 0), 1);
            let gHtml = '';
            for (const g of allGrades) {{
                const c = gradeCounts[g] || 0;
                gHtml += `<div class="bar-row" onclick="setFilter('filter-grade', '${{g}}')"><div class="bar-label">Grade ${{g}}</div><div class="bar-track"><div class="bar-fill" style="width:${{(c/maxG*100).toFixed(1)}}%;"></div></div><div class="bar-val">${{c.toLocaleString()}}</div></div>`;
            }}
            document.getElementById('cust-grade-container').innerHTML = gHtml;

            // Dashboard 2: Income tickets
            let incHtml = '';
            for (const [tier, arr] of Object.entries(incomeAmounts)) {{
                const avgT = arr.length > 0 ? (arr.reduce((a,b)=>a+b,0) / arr.length) : 0;
                incHtml += `<div class="bar-row"><div class="bar-label">${{tier}}</div><div class="bar-track"><div class="bar-fill" style="width:${{(avgT/16000*100).toFixed(1)}}%; background: #0EA5E9;"></div></div><div class="bar-val">$${{Math.round(avgT).toLocaleString()}}</div></div>`;
            }}
            document.getElementById('cust-income-container').innerHTML = incHtml;

            // Dashboard 3: Risk Summary
            const hrDefRate = hrCount > 0 ? (hrDefaults / hrCount * 100) : 0;
            document.getElementById('hr-count').textContent = hrCount.toLocaleString();
            document.getElementById('hr-pct').textContent = `${{(hrCount/totalCount*100).toFixed(1)}}% of Filtered Portfolio`;
            document.getElementById('hr-funded').textContent = `$${{(hrFunded/1e6).toFixed(1)}}M`;
            document.getElementById('hr-funded-pct').textContent = `${{(hrFunded/totFunded*100).toFixed(1)}}% of Filtered Capital`;
            document.getElementById('hr-rate').textContent = `${{hrDefRate.toFixed(2)}}%`;
            document.getElementById('hr-rate-sub').textContent = `${{hrDefaults.toLocaleString()}} Defaults in Segment`;

            // Dashboard 3: Default rate by grade (Clickable)
            let rgHtml = '';
            for (const g of allGrades) {{
                const c = gradeCounts[g] || 0;
                const d = gradeDefaults[g] || 0;
                const dr = c > 0 ? (d / c * 100) : 0;
                const col = g === 'A' ? 'var(--emerald)' : (['B','C'].includes(g) ? 'var(--amber)' : 'var(--crimson)');
                rgHtml += `<div class="bar-row" onclick="setFilter('filter-grade', '${{g}}')"><div class="bar-label">Grade ${{g}} (${{d}} def)</div><div class="bar-track"><div class="bar-fill" style="width:${{(dr/35*100).toFixed(1)}}%; background: ${{col}};"></div></div><div class="bar-val">${{dr.toFixed(1)}}%</div></div>`;
            }}
            document.getElementById('risk-grade-container').innerHTML = rgHtml;

            // Dashboard 3: Default rate by purpose (Clickable)
            const sortedPurpDef = Object.keys(purposeCounts).map(p => {{
                const c = purposeCounts[p];
                const d = purposeDefaults[p] || 0;
                return [p, c > 0 ? (d/c*100) : 0, d];
            }}).sort((a,b)=>b[1]-a[1]).slice(0,6);

            let rpHtml = '';
            for (const [p, dr, d] of sortedPurpDef) {{
                rpHtml += `<div class="bar-row" onclick="setFilter('filter-purpose', '${{p}}')"><div class="bar-label" title="${{p}}">${{p}}</div><div class="bar-track"><div class="bar-fill" style="width:${{(dr/30*100).toFixed(1)}}%; background: var(--crimson);"></div></div><div class="bar-val">${{dr.toFixed(1)}}% (${{d}})</div></div>`;
            }}
            document.getElementById('risk-purpose-container').innerHTML = rpHtml;

            // Dashboard 3: Loss Given Default & Recoveries
            document.getElementById('risk-recovery-container').innerHTML = `
                <div class="bar-row"><div class="bar-label">Defaulted Principal</div><div class="bar-track"><div class="bar-fill" style="width:100%; background:var(--crimson);"></div></div><div class="bar-val">$${{(defFunded/1e6).toFixed(2)}}M</div></div>
                <div class="bar-row"><div class="bar-label">Recoveries Recoup</div><div class="bar-track"><div class="bar-fill" style="width:${{recRate.toFixed(1)}}%; background:var(--emerald);"></div></div><div class="bar-val">$${{(defReceived/1e6).toFixed(2)}}M (${{recRate.toFixed(1)}}%)</div></div>
                <div class="bar-row"><div class="bar-label">Net Credit Loss</div><div class="bar-track"><div class="bar-fill" style="width:${{defFunded > 0 ? (netLoss/defFunded*100).toFixed(1) : 0}}%; background:#475569;"></div></div><div class="bar-val">$${{(netLoss/1e6).toFixed(2)}}M</div></div>
            `;

            // Dashboard 3: DTI Leverage
            let dtiHtml = '';
            for (const [k, [d, c]] of Object.entries(dtiDefaults)) {{
                const dr = c > 0 ? (d / c * 100) : 0;
                const col = dr > 15 ? 'var(--crimson)' : 'var(--amber)';
                dtiHtml += `<div class="bar-row"><div class="bar-label">DTI ${{k}}</div><div class="bar-track"><div class="bar-fill" style="width:${{(dr/20*100).toFixed(1)}}%; background:${{col}};"></div></div><div class="bar-val">${{dr.toFixed(1)}}%</div></div>`;
            }}
            document.getElementById('risk-dti-container').innerHTML = dtiHtml;
        }}

        // Initial render on page load
        renderDashboard(rawData);
    </script>
</body>
</html>
"""

    with open(HTML_LOCAL, "w", encoding="utf-8") as f1:
        f1.write(html_code)
    print(f"Written local file: {HTML_LOCAL} ({os.path.getsize(HTML_LOCAL)/1024/1024:.2f} MB)")

    with open(HTML_ARTIFACT, "w", encoding="utf-8") as f2:
        f2.write(html_code)
    print(f"Written artifact file: {HTML_ARTIFACT} ({os.path.getsize(HTML_ARTIFACT)/1024/1024:.2f} MB)")

if __name__ == "__main__":
    generate_interactive_suite()

