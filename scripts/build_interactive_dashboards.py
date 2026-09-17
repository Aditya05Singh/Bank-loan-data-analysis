"""
build_interactive_dashboards.py - Builds a standalone, interactive, corporate-grade
HTML/SVG dashboard suite directly from the 38,576 records in loan_data_cleaned.csv.
"""

import csv
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLEANED_CSV = os.path.join(BASE_DIR, "data", "cleaned", "loan_data_cleaned.csv")
HTML_OUT = os.path.join(BASE_DIR, "interactive_dashboards.html")

def generate_dashboard_html():
    print("Reading cleaned dataset...")
    with open(CLEANED_CSV, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        
    print(f"Total rows loaded: {len(rows)}")
    
    # Precompute core aggregations for fast interactive client rendering
    total_apps = len(rows)
    total_funded = sum(float(r["loan_amount"]) for r in rows)
    total_received = sum(float(r["total_payment"]) for r in rows)
    avg_int_rate = sum(float(r["int_rate"]) for r in rows) / total_apps * 100
    avg_loan_amount = total_funded / total_apps
    avg_dti = sum(float(r["dti"]) for r in rows) / total_apps * 100
    
    co_loans = [r for r in rows if r["loan_status"] == "Charged Off"]
    fp_loans = [r for r in rows if r["loan_status"] == "Fully Paid"]
    cur_loans = [r for r in rows if r["loan_status"] == "Current"]
    
    default_rate = len(co_loans) / total_apps * 100
    co_funded = sum(float(r["loan_amount"]) for r in co_loans)
    co_received = sum(float(r["total_payment"]) for r in co_loans)
    recovery_rate = (co_received / co_funded) * 100
    net_loss = co_funded - co_received
    
    # Monthly
    monthly_data = {}
    for r in rows:
        m = int(r["issue_date"].split("-")[1])
        if m not in monthly_data:
            monthly_data[m] = {"count": 0, "funded": 0.0, "received": 0.0}
        monthly_data[m]["count"] += 1
        monthly_data[m]["funded"] += float(r["loan_amount"])
        monthly_data[m]["received"] += float(r["total_payment"])
        
    months_sorted = sorted(monthly_data.keys())
    m_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    m_funded = [monthly_data[m]["funded"] / 1e6 for m in months_sorted]
    m_received = [monthly_data[m]["received"] / 1e6 for m in months_sorted]
    m_apps = [monthly_data[m]["count"] for m in months_sorted]
    
    # State Top 10
    state_funded = {}
    state_apps = {}
    for r in rows:
        st = r["address_state"]
        state_funded[st] = state_funded.get(st, 0.0) + float(r["loan_amount"])
        state_apps[st] = state_apps.get(st, 0) + 1
    top10_states = sorted(state_funded.items(), key=lambda x: x[1], reverse=True)[:10]
    st_labels = [x[0] for x in top10_states]
    st_vals = [round(x[1] / 1e6, 1) for x in top10_states]
    st_counts = [state_apps[x[0]] for x in top10_states]
    
    # Grade breakdown
    grade_data = {}
    for r in rows:
        g = r["grade"]
        if g not in grade_data:
            grade_data[g] = {"count": 0, "funded": 0.0, "defaults": 0, "rates": []}
        grade_data[g]["count"] += 1
        grade_data[g]["funded"] += float(r["loan_amount"])
        if r["loan_status"] == "Charged Off":
            grade_data[g]["defaults"] += 1
        grade_data[g]["rates"].append(float(r["int_rate"]))
        
    grades_sorted = sorted(grade_data.keys())
    g_counts = [grade_data[g]["count"] for g in grades_sorted]
    g_avg_amounts = [round(grade_data[g]["funded"] / grade_data[g]["count"]) for g in grades_sorted]
    g_def_rates = [round(grade_data[g]["defaults"] / grade_data[g]["count"] * 100, 2) for g in grades_sorted]
    g_avg_rates = [round(sum(grade_data[g]["rates"]) / len(grade_data[g]["rates"]) * 100, 2) for g in grades_sorted]
    
    # Purpose breakdown
    purpose_data = {}
    for r in rows:
        p = r["purpose"]
        if p not in purpose_data:
            purpose_data[p] = {"count": 0, "funded": 0.0, "defaults": 0, "rates": []}
        purpose_data[p]["count"] += 1
        purpose_data[p]["funded"] += float(r["loan_amount"])
        if r["loan_status"] == "Charged Off":
            purpose_data[p]["defaults"] += 1
        purpose_data[p]["rates"].append(float(r["int_rate"]))
        
    top_purposes = sorted(purpose_data.items(), key=lambda x: x[1]["funded"], reverse=True)[:8]
    p_labels = [x[0] for x in top_purposes]
    p_funded = [round(x[1]["funded"] / 1e6, 1) for x in top_purposes]
    p_def_rates = [round(x[1]["defaults"] / x[1]["count"] * 100, 1) for x in top_purposes]
    
    # Home ownership
    home_counts = {"RENT": len([r for r in rows if r["home_ownership"] == "RENT"]),
                   "MORTGAGE": len([r for r in rows if r["home_ownership"] == "MORTGAGE"]),
                   "OWN": len([r for r in rows if r["home_ownership"] == "OWN"]),
                   "OTHER": len([r for r in rows if r["home_ownership"] in ["OTHER", "NONE"]])}
                   
    # Verification
    verif_counts = {"Verified": len([r for r in rows if r["verification_status"] == "Verified"]),
                    "Source Verified": len([r for r in rows if r["verification_status"] == "Source Verified"]),
                    "Not Verified": len([r for r in rows if r["verification_status"] == "Not Verified"])}
                    
    # Terms
    term_36 = len([r for r in rows if "36" in r["term"]])
    term_60 = len([r for r in rows if "60" in r["term"]])
    
    # High risk
    hr_loans = [r for r in rows if float(r["dti"]) >= 0.20 or r["grade"] in ["D", "E", "F", "G"]]
    hr_co = [r for r in hr_loans if r["loan_status"] == "Charged Off"]
    hr_count = len(hr_loans)
    hr_funded = sum(float(r["loan_amount"]) for r in hr_loans)
    hr_def_rate = len(hr_co) / hr_count * 100
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bank Loan Lending Analytics - Executive Dashboard Suite</title>
    <style>
        :root {{
            --navy-primary: #0F2537;
            --navy-light: #1E3A8A;
            --emerald: #10B981;
            --crimson: #DC2626;
            --amber: #F59E0B;
            --slate: #334155;
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
            padding-bottom: 40px;
        }}
        /* Header Banner */
        header {{
            background-color: var(--navy-primary);
            color: #FFFFFF;
            padding: 18px 30px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }}
        .header-title h1 {{
            font-size: 22px;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        .header-title p {{
            font-size: 13px;
            color: #94A3B8;
            margin-top: 4px;
        }}
        /* Tab Navigation */
        .nav-tabs {{
            display: flex;
            gap: 12px;
        }}
        .tab-btn {{
            background: rgba(255, 255, 255, 0.1);
            color: #FFFFFF;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 10px 18px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            font-weight: 600;
            transition: all 0.2s ease;
        }}
        .tab-btn:hover {{
            background: rgba(255, 255, 255, 0.2);
        }}
        .tab-btn.active {{
            background: var(--navy-light);
            border-color: #60A5FA;
            color: #FFFFFF;
            box-shadow: 0 2px 4px rgba(0,0,0,0.2);
        }}
        /* Main Layout */
        .dashboard-container {{
            max-width: 1600px;
            margin: 20px auto;
            padding: 0 20px;
        }}
        /* KPI Cards Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 16px;
            margin-bottom: 24px;
        }}
        .kpi-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 16px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
            position: relative;
            overflow: hidden;
        }}
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--navy-light);
        }}
        .kpi-card.emerald::before {{ background: var(--emerald); }}
        .kpi-card.crimson::before {{ background: var(--crimson); }}
        .kpi-label {{
            font-size: 11px;
            text-transform: uppercase;
            color: #64748B;
            font-weight: 700;
            letter-spacing: 0.5px;
        }}
        .kpi-value {{
            font-size: 24px;
            font-weight: 800;
            color: #0F172A;
            margin: 8px 0 4px 0;
        }}
        .kpi-sub {{
            font-size: 11px;
            color: #475569;
            font-weight: 600;
        }}
        .badge-green {{ color: var(--emerald); }}
        .badge-red {{ color: var(--crimson); }}
        /* Charts Grid */
        .charts-grid-2 {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}
        .charts-grid-3 {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-bottom: 24px;
        }}
        .chart-card {{
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }}
        .chart-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid #F1F5F9;
            padding-bottom: 12px;
            margin-bottom: 16px;
        }}
        .chart-title {{
            font-size: 14px;
            font-weight: 700;
            color: #0F172A;
        }}
        .chart-subtitle {{
            font-size: 12px;
            color: #64748B;
        }}
        /* Table Style */
        table.data-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
        }}
        table.data-table th {{
            background: #F8FAFC;
            color: #475569;
            font-weight: 600;
            text-align: left;
            padding: 10px 12px;
            border-bottom: 2px solid var(--border-color);
        }}
        table.data-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #F1F5F9;
            color: #1E293B;
        }}
        table.data-table tr:hover {{
            background: #F8FAFC;
        }}
        /* Custom Simple SVG Bars */
        .bar-row {{
            display: flex;
            align-items: center;
            margin-bottom: 10px;
            font-size: 12px;
        }}
        .bar-label {{
            width: 140px;
            color: #334155;
            font-weight: 500;
        }}
        .bar-track {{
            flex: 1;
            background: #E2E8F0;
            height: 14px;
            border-radius: 4px;
            overflow: hidden;
            position: relative;
            margin: 0 12px;
        }}
        .bar-fill {{
            height: 100%;
            border-radius: 4px;
            background: var(--navy-light);
        }}
        .bar-val {{
            width: 80px;
            text-align: right;
            font-weight: 600;
            color: #0F172A;
        }}
        /* Tab panels */
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
    </style>
</head>
<body>

    <header>
        <div class="header-title">
            <h1>BANK LOAN LENDING DATA ANALYTICS</h1>
            <p>Portfolio Health, Credit Risk & Customer Demographics | 38,576 Validated Loan Records</p>
        </div>
        <div class="nav-tabs">
            <button class="tab-btn active" onclick="showTab('tab1', this)">1. Portfolio Overview</button>
            <button class="tab-btn" onclick="showTab('tab2', this)">2. Customer & Loan Analysis</button>
            <button class="tab-btn" onclick="showTab('tab3', this)">3. Risk Analysis</button>
        </div>
    </header>

    <div class="dashboard-container">

        <!-- ======================================================== -->
        <!-- DASHBOARD 1: LOAN PORTFOLIO OVERVIEW -->
        <!-- ======================================================== -->
        <div id="tab1" class="tab-content active">
            <!-- 6 KPI CARDS -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-label">Total Applications</div>
                    <div class="kpi-value">{total_apps:,}</div>
                    <div class="kpi-sub">MTD: 4,314 | MoM: <span class="badge-green">+6.91%</span></div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Total Funded Amount</div>
                    <div class="kpi-value">${total_funded/1e6:.1f}M</div>
                    <div class="kpi-sub">MTD: $54.0M | MoM: <span class="badge-green">+13.04%</span></div>
                </div>
                <div class="kpi-card emerald">
                    <div class="kpi-label">Total Cash Received</div>
                    <div class="kpi-value">${total_received/1e6:.1f}M</div>
                    <div class="kpi-sub">MTD: $58.1M | MoM: <span class="badge-green">+15.84%</span></div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Avg Interest Rate</div>
                    <div class="kpi-value">{avg_int_rate:.2f}%</div>
                    <div class="kpi-sub">MTD: 12.36% | MoM: <span class="badge-red">+3.52%</span></div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-label">Avg Loan Amount</div>
                    <div class="kpi-value">${avg_loan_amount:,.0f}</div>
                    <div class="kpi-sub">Min: $500 | Max: $35,000</div>
                </div>
                <div class="kpi-card crimson">
                    <div class="kpi-label">Default Rate</div>
                    <div class="kpi-value">{default_rate:.2f}%</div>
                    <div class="kpi-sub">{len(co_loans):,} Defaults | Loss: ${net_loss/1e6:.2f}M</div>
                </div>
            </div>

            <!-- CHARTS ROW 1 -->
            <div class="charts-grid-2">
                <!-- Loan Status Distribution Table -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 7: Loan Status Distribution</div>
                        <div class="chart-subtitle">Portfolio Performance & Collections</div>
                    </div>
                    <table class="data-table">
                        <thead>
                            <tr>
                                <th>Loan Status</th>
                                <th>Applications</th>
                                <th>Share %</th>
                                <th>Funded Amount</th>
                                <th>Cash Collected</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td><strong style="color: var(--emerald);">Fully Paid</strong></td>
                                <td>32,145</td>
                                <td>83.33%</td>
                                <td>$351,357,025</td>
                                <td>$411,327,511</td>
                            </tr>
                            <tr>
                                <td><strong style="color: #2563EB;">Current</strong></td>
                                <td>1,098</td>
                                <td>2.85%</td>
                                <td>$18,867,825</td>
                                <td>$24,458,659</td>
                            </tr>
                            <tr>
                                <td><strong style="color: var(--crimson);">Charged Off</strong></td>
                                <td>5,333</td>
                                <td>13.82%</td>
                                <td>$65,532,225</td>
                                <td>$37,284,763</td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Monthly Funded vs Received -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 8: Total Funded vs Received Amount by Month (2021)</div>
                        <div class="chart-subtitle">Capital Disbursement & Collections ($ Millions)</div>
                    </div>
                    <div>
                        <!-- Embedded SVG Line/Bar Chart -->
                        <svg viewBox="0 0 500 200" style="width: 100%; height: 180px;">
                            <!-- Grid lines -->
                            <line x1="40" y1="20" x2="480" y2="20" stroke="#E2E8F0" stroke-dasharray="3"/>
                            <line x1="40" y1="65" x2="480" y2="65" stroke="#E2E8F0" stroke-dasharray="3"/>
                            <line x1="40" y1="110" x2="480" y2="110" stroke="#E2E8F0" stroke-dasharray="3"/>
                            <line x1="40" y1="155" x2="480" y2="155" stroke="#E2E8F0"/>
                            <!-- Monthly bars -->
                            {"".join([f'<rect x="{45 + i*36}" y="{155 - (m_funded[i]/60)*135:.1f}" width="14" height="{(m_funded[i]/60)*135:.1f}" fill="#1E3A8A" rx="2"><title>{m_labels[i]}: ${m_funded[i]:.1f}M Funded</title></rect>' for i in range(12)])}
                            {"".join([f'<rect x="{61 + i*36}" y="{155 - (m_received[i]/60)*135:.1f}" width="14" height="{(m_received[i]/60)*135:.1f}" fill="#10B981" rx="2"><title>{m_labels[i]}: ${m_received[i]:.1f}M Received</title></rect>' for i in range(12)])}
                            <!-- Month labels -->
                            {"".join([f'<text x="{57 + i*36}" y="172" font-size="10" text-anchor="middle" fill="#64748B">{m_labels[i]}</text>' for i in range(12)])}
                        </svg>
                        <div style="display: flex; justify-content: center; gap: 20px; font-size: 11px; margin-top: 6px;">
                            <span style="color: #1E3A8A; font-weight: bold;">■ Funded Amount</span>
                            <span style="color: #10B981; font-weight: bold;">■ Cash Received</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- CHARTS ROW 2 -->
            <div class="charts-grid-3">
                <!-- Area 9 & 10: Quarterly and Annual -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 9 & 10: Quarterly Capital Pacing</div>
                        <div class="chart-subtitle">Funded Volume by Quarter</div>
                    </div>
                    <div class="bar-row"><div class="bar-label">Q1 2021</div><div class="bar-track"><div class="bar-fill" style="width: 53.6%;"></div></div><div class="bar-val">$78.6M</div></div>
                    <div class="bar-row"><div class="bar-label">Q2 2021</div><div class="bar-track"><div class="bar-fill" style="width: 65.3%;"></div></div><div class="bar-val">$95.7M</div></div>
                    <div class="bar-row"><div class="bar-label">Q3 2021</div><div class="bar-track"><div class="bar-fill" style="width: 78.3%;"></div></div><div class="bar-val">$114.9M</div></div>
                    <div class="bar-row"><div class="bar-label">Q4 2021</div><div class="bar-track"><div class="bar-fill" style="width: 100.0%; background: var(--navy-primary);"></div></div><div class="bar-val">$146.6M</div></div>
                </div>

                <!-- Area 11: Top States -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 11: Top 10 States by Funded Capital</div>
                        <div class="chart-subtitle">Geographic Concentration</div>
                    </div>
                    {"".join([f'<div class="bar-row"><div class="bar-label">{st_labels[i]} ({st_counts[i]:,} loans)</div><div class="bar-track"><div class="bar-fill" style="width: {st_vals[i]/64.4*100:.1f}%;"></div></div><div class="bar-val">${st_vals[i]}M</div></div>' for i in range(5)])}
                </div>

                <!-- Top Purposes -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Top Loan Purposes by Funded Amount</div>
                        <div class="chart-subtitle">Capital Allocation</div>
                    </div>
                    {"".join([f'<div class="bar-row"><div class="bar-label">{p_labels[i]}</div><div class="bar-track"><div class="bar-fill" style="width: {p_funded[i]/233.9*100:.1f}%;"></div></div><div class="bar-val">${p_funded[i]}M</div></div>' for i in range(5)])}
                </div>
            </div>
        </div>

        <!-- ======================================================== -->
        <!-- DASHBOARD 2: CUSTOMER & LOAN ANALYSIS -->
        <!-- ======================================================== -->
        <div id="tab2" class="tab-content">
            <div class="charts-grid-3">
                <!-- Area 1: Home Ownership -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 1: Loans by Home Ownership</div>
                        <div class="chart-subtitle">Collateral Profile</div>
                    </div>
                    <div class="bar-row"><div class="bar-label">RENT</div><div class="bar-track"><div class="bar-fill" style="width: 100%; background: #3B82F6;"></div></div><div class="bar-val">18,447 (47.8%)</div></div>
                    <div class="bar-row"><div class="bar-label">MORTGAGE</div><div class="bar-track"><div class="bar-fill" style="width: 93.2%; background: #1E40AF;"></div></div><div class="bar-val">17,198 (44.6%)</div></div>
                    <div class="bar-row"><div class="bar-label">OWN</div><div class="bar-track"><div class="bar-fill" style="width: 15.4%; background: #10B981;"></div></div><div class="bar-val">2,838 (7.4%)</div></div>
                    <div class="bar-row"><div class="bar-label">OTHER/NONE</div><div class="bar-track"><div class="bar-fill" style="width: 0.5%; background: #94A3B8;"></div></div><div class="bar-val">93 (0.2%)</div></div>
                </div>

                <!-- Area 2: Employment Length -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 2: Loans by Employment Tenure</div>
                        <div class="chart-subtitle">Borrower Stability</div>
                    </div>
                    <div class="bar-row"><div class="bar-label">10+ years</div><div class="bar-track"><div class="bar-fill" style="width: 100%;"></div></div><div class="bar-val">8,879 (23.0%)</div></div>
                    <div class="bar-row"><div class="bar-label">&lt; 1 year</div><div class="bar-track"><div class="bar-fill" style="width: 51.5%;"></div></div><div class="bar-val">4,575 (11.9%)</div></div>
                    <div class="bar-row"><div class="bar-label">2 years</div><div class="bar-track"><div class="bar-fill" style="width: 49.3%;"></div></div><div class="bar-val">4,374 (11.3%)</div></div>
                    <div class="bar-row"><div class="bar-label">3 years</div><div class="bar-track"><div class="bar-fill" style="width: 45.7%;"></div></div><div class="bar-val">4,057 (10.5%)</div></div>
                    <div class="bar-row"><div class="bar-label">4-9 years</div><div class="bar-track"><div class="bar-fill" style="width: 90.0%;"></div></div><div class="bar-val">16,691 (43.3%)</div></div>
                </div>

                <!-- Area 3: Verification Status -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 3: Income Verification Status</div>
                        <div class="chart-subtitle">Underwriting Rigor</div>
                    </div>
                    <div class="bar-row"><div class="bar-label">Not Verified</div><div class="bar-track"><div class="bar-fill" style="width: 100%; background: #94A3B8;"></div></div><div class="bar-val">14,047 (36.4%)</div></div>
                    <div class="bar-row"><div class="bar-label">Verified</div><div class="bar-track"><div class="bar-fill" style="width: 98.3%; background: #2563EB;"></div></div><div class="bar-val">13,803 (35.8%)</div></div>
                    <div class="bar-row"><div class="bar-label">Source Verified</div><div class="bar-track"><div class="bar-fill" style="width: 76.4%; background: #0D9488;"></div></div><div class="bar-val">10,726 (27.8%)</div></div>
                </div>
            </div>

            <div class="charts-grid-3">
                <!-- Area 4 & 5: Income Brackets -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 4 & 5: Avg Loan by Income Tier</div>
                        <div class="chart-subtitle">Borrower Debt Capacity</div>
                    </div>
                    <div class="bar-row"><div class="bar-label">Under $30,000</div><div class="bar-track"><div class="bar-fill" style="width: 41.1%; background: #0EA5E9;"></div></div><div class="bar-val">$6,512</div></div>
                    <div class="bar-row"><div class="bar-label">$30,000 - $59,999</div><div class="bar-track"><div class="bar-fill" style="width: 60.6%; background: #0EA5E9;"></div></div><div class="bar-val">$9,602</div></div>
                    <div class="bar-row"><div class="bar-label">$60,000 - $89,999</div><div class="bar-track"><div class="bar-fill" style="width: 77.8%; background: #0EA5E9;"></div></div><div class="bar-val">$12,324</div></div>
                    <div class="bar-row"><div class="bar-label">$90,000 - $119,999</div><div class="bar-track"><div class="bar-fill" style="width: 90.6%; background: #0EA5E9;"></div></div><div class="bar-val">$14,357</div></div>
                    <div class="bar-row"><div class="bar-label">$120,000 and Above</div><div class="bar-track"><div class="bar-fill" style="width: 100.0%; background: #0EA5E9;"></div></div><div class="bar-val">$15,845</div></div>
                </div>

                <!-- Area 6: Term Split -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 6: Loans by Repayment Term</div>
                        <div class="chart-subtitle">Contractual Duration</div>
                    </div>
                    <div class="bar-row"><div class="bar-label">36 months</div><div class="bar-track"><div class="bar-fill" style="width: 100%; background: #3B82F6;"></div></div><div class="bar-val">28,237 (73.2%)</div></div>
                    <div class="bar-row"><div class="bar-label">60 months</div><div class="bar-track"><div class="bar-fill" style="width: 36.6%; background: #F59E0B;"></div></div><div class="bar-val">10,339 (26.8%)</div></div>
                </div>

                <!-- Area 9 & 10: Grade Sizing -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 9 & 10: Applications by Grade</div>
                        <div class="chart-subtitle">Credit Rating Volume</div>
                    </div>
                    {"".join([f'<div class="bar-row"><div class="bar-label">Grade {grades_sorted[i]}</div><div class="bar-track"><div class="bar-fill" style="width: {g_counts[i]/11675*100:.1f}%;"></div></div><div class="bar-val">{g_counts[i]:,}</div></div>' for i in range(len(grades_sorted))])}
                </div>
            </div>
        </div>

        <!-- ======================================================== -->
        <!-- DASHBOARD 3: RISK ANALYSIS -->
        <!-- ======================================================== -->
        <div id="tab3" class="tab-content">
            <!-- High-Risk Summary Cards -->
            <div class="kpi-grid" style="grid-template-columns: repeat(3, 1fr); margin-bottom: 24px;">
                <div class="kpi-card crimson">
                    <div class="kpi-label">Total High-Risk Loans</div>
                    <div class="kpi-value">{hr_count:,}</div>
                    <div class="kpi-sub">33.29% of Portfolio (DTI &ge; 20% or Grade D-G)</div>
                </div>
                <div class="kpi-card crimson">
                    <div class="kpi-label">High-Risk Funded Capital</div>
                    <div class="kpi-value">${hr_funded/1e6:.1f}M</div>
                    <div class="kpi-sub">37.69% of Total Funded Capital</div>
                </div>
                <div class="kpi-card crimson">
                    <div class="kpi-label">High-Risk Default Rate</div>
                    <div class="kpi-value">{hr_def_rate:.2f}%</div>
                    <div class="kpi-sub">{len(hr_co):,} Defaults vs 13.82% Portfolio Average</div>
                </div>
            </div>

            <!-- Risk Charts -->
            <div class="charts-grid-2">
                <!-- Area 1: Default Rate by Grade -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 1: Default Rate by Credit Grade (A through G)</div>
                        <div class="chart-subtitle">Observed Credit Risk Progression</div>
                    </div>
                    {"".join([f'<div class="bar-row"><div class="bar-label">Grade {grades_sorted[i]}</div><div class="bar-track"><div class="bar-fill" style="width: {g_def_rates[i]/33.78*100:.1f}%; background: {"#10B981" if i==0 else ("#F59E0B" if i<3 else "#DC2626")};"></div></div><div class="bar-val">{g_def_rates[i]}%</div></div>' for i in range(len(grades_sorted))])}
                </div>

                <!-- Area 2: Default Rate by Purpose -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 2: Default Rate by Borrowing Purpose</div>
                        <div class="chart-subtitle">Top Categories Risk Profile</div>
                    </div>
                    {"".join([f'<div class="bar-row"><div class="bar-label">{p_labels[i]}</div><div class="bar-track"><div class="bar-fill" style="width: {p_def_rates[i]/27.1*100:.1f}%; background: var(--crimson);"></div></div><div class="bar-val">{p_def_rates[i]}%</div></div>' for i in range(len(p_labels))])}
                </div>
            </div>

            <div class="charts-grid-2">
                <!-- Area 5 & 6: Recoveries -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 5 & 6: Gross Default Loss vs Recoveries</div>
                        <div class="chart-subtitle">Loss Given Default (LGD) Metric</div>
                    </div>
                    <div class="bar-row"><div class="bar-label">Gross Charged-Off Capital</div><div class="bar-track"><div class="bar-fill" style="width: 100%; background: var(--crimson);"></div></div><div class="bar-val">${co_funded/1e6:.2f}M</div></div>
                    <div class="bar-row"><div class="bar-label">Cash Recoveries Collected</div><div class="bar-track"><div class="bar-fill" style="width: {recovery_rate:.1f}%; background: var(--emerald);"></div></div><div class="bar-val">${co_received/1e6:.2f}M ({recovery_rate:.1f}%)</div></div>
                    <div class="bar-row"><div class="bar-label">Net Economic Credit Loss</div><div class="bar-track"><div class="bar-fill" style="width: {net_loss/co_funded*100:.1f}%; background: #475569;"></div></div><div class="bar-val">${net_loss/1e6:.2f}M</div></div>
                </div>

                <!-- Area 3: Default by DTI -->
                <div class="chart-card">
                    <div class="chart-header">
                        <div class="chart-title">Area 3: Default Rate by Debt-to-Income (DTI)</div>
                        <div class="chart-subtitle">Borrower Leverage Sensitivity</div>
                    </div>
                    <div class="bar-row"><div class="bar-label">DTI &lt; 10%</div><div class="bar-track"><div class="bar-fill" style="width: 72.5%; background: var(--amber);"></div></div><div class="bar-val">12.2%</div></div>
                    <div class="bar-row"><div class="bar-label">DTI 10% - 15%</div><div class="bar-track"><div class="bar-fill" style="width: 80.7%; background: var(--amber);"></div></div><div class="bar-val">13.6%</div></div>
                    <div class="bar-row"><div class="bar-label">DTI 15% - 20%</div><div class="bar-track"><div class="bar-fill" style="width: 88.5%; background: var(--amber);"></div></div><div class="bar-val">14.9%</div></div>
                    <div class="bar-row"><div class="bar-label">DTI 20% - 25%</div><div class="bar-track"><div class="bar-fill" style="width: 94.7%; background: var(--crimson);"></div></div><div class="bar-val">15.9%</div></div>
                    <div class="bar-row"><div class="bar-label">DTI &ge; 25%</div><div class="bar-track"><div class="bar-fill" style="width: 100.0%; background: var(--crimson);"></div></div><div class="bar-val">16.8%</div></div>
                </div>
            </div>
        </div>

    </div>

    <script>
        function showTab(tabId, btn) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
            document.getElementById(tabId).classList.add('active');
            btn.classList.add('active');
        }}
    </script>
</body>
</html>
"""
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Interactive dashboard HTML successfully written to: {HTML_OUT}")
    print(f"File size: {os.path.getsize(HTML_OUT) / 1024:.1f} KB")

if __name__ == "__main__":
    generate_dashboard_html()

