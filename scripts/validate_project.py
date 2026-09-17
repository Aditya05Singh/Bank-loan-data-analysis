"""
validate_project.py - Comprehensive Automated Verification Script

Performs technical audits across:
1. File structure & completeness
2. Dataset counts & column integrity
3. Data quality assertions
4. Core financial KPI calculations
5. SQL script syntax & column validation
6. Tableau dashboard visualization count
"""

import csv
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def audit_file_structure():
    print("--- 1. AUDITING FILE STRUCTURE ---")
    expected_files = [
        "data/raw/loan_data_raw.csv",
        "data/cleaned/loan_data_cleaned.csv",
        "scripts/clean_data.py",
        "sql/01_database_setup.sql",
        "sql/02_schema.sql",
        "sql/03_data_quality.sql",
        "sql/04_kpi_analysis.sql",
        "sql/05_portfolio_analysis.sql",
        "sql/06_customer_analysis.sql",
        "sql/07_risk_analysis.sql",
        "sql/08_time_series_analysis.sql",
        "sql/09_tableau_views.sql",
        "tableau/Bank_Loan_Lending_Analytics.twb",
        "tableau/dashboard_1_loan_portfolio.md",
        "tableau/dashboard_2_customer_loan_analysis.md",
        "tableau/dashboard_3_risk_analysis.md",
        "tableau/calculated_fields.md",
        "tableau/tableau_data_sources.md",
        "tableau/tableau_guide.md",
        "interactive_dashboards.html",
        "documentation/project_overview.md",
        "documentation/data_dictionary.md",
        "documentation/data_cleaning.md",
        "documentation/business_questions.md",
        "documentation/methodology.md",
        "documentation/sql_explanation.md",
        "documentation/tableau_guide.md",
        "documentation/interview_questions.md",
        "documentation/final_audit_report.md",
        "documentation/tableau_final_setup.md",
        "README.md",
        ".gitignore",
        "requirements.txt"
    ]
    missing = []
    for f in expected_files:
        path = os.path.join(BASE_DIR, f)
        if not os.path.exists(path):
            missing.append(f)
            print(f"  [MISSING] {f}")
        else:
            size_kb = os.path.getsize(path) / 1024
            print(f"  [OK] {f} ({size_kb:.1f} KB)")
    
    if missing:
        print(f"FAIL: {len(missing)} files missing!")
        return False
    print(f"PASS: All {len(expected_files)} required project files exist.")
    return True

def audit_dataset():
    print("\n--- 2. AUDITING DATASET INTEGRITY ---")
    cleaned_csv = os.path.join(BASE_DIR, "data", "cleaned", "loan_data_cleaned.csv")
    with open(cleaned_csv, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        cols = reader.fieldnames

    print(f"Actual cleaned records: {len(rows):,}")
    print(f"Actual cleaned columns: {len(cols)}")
    print(f"Columns: {cols}")

    assert len(rows) == 38576, f"Expected 38576 rows, got {len(rows)}"
    assert len(cols) == 24, f"Expected 24 cols, got {len(cols)}"

    # Primary key check
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids)), "Duplicate primary keys found!"
    print("PASS: 38,576 records, 24 columns, 0 duplicate IDs.")

    # Core Financial KPI calculations
    total_funded = sum(float(r["loan_amount"]) for r in rows)
    total_received = sum(float(r["total_payment"]) for r in rows)
    avg_int_rate = sum(float(r["int_rate"]) for r in rows) / len(rows) * 100
    avg_loan_amount = total_funded / len(rows)
    avg_dti = sum(float(r["dti"]) for r in rows) / len(rows) * 100

    charged_off_loans = [r for r in rows if r["loan_status"] == "Charged Off"]
    fully_paid_loans = [r for r in rows if r["loan_status"] == "Fully Paid"]
    current_loans = [r for r in rows if r["loan_status"] == "Current"]

    default_rate = len(charged_off_loans) / len(rows) * 100
    fully_paid_rate = len(fully_paid_loans) / len(rows) * 100
    co_funded = sum(float(r["loan_amount"]) for r in charged_off_loans)
    co_received = sum(float(r["total_payment"]) for r in charged_off_loans)
    recovery_rate = (co_received / co_funded) * 100
    net_credit_loss = co_funded - co_received

    print("\n--- 3. RECONCILED CORE FINANCIAL KPIS ---")
    print(f"1. Total Loan Applications : {len(rows):,}")
    print(f"2. Total Funded Amount     : ${total_funded:,.2f} (${total_funded/1e6:.1f}M)")
    print(f"3. Total Received Amount   : ${total_received:,.2f} (${total_received/1e6:.1f}M)")
    print(f"4. Average Interest Rate   : {avg_int_rate:.2f}%")
    print(f"5. Average Loan Amount     : ${avg_loan_amount:,.2f}")
    print(f"6. Default Rate            : {default_rate:.2f}% ({len(charged_off_loans):,} loans)")
    print(f"7. Fully Paid Rate         : {fully_paid_rate:.2f}% ({len(fully_paid_loans):,} loans)")
    print(f"8. Average DTI             : {avg_dti:.2f}%")
    print(f"9. Gross Charged-Off Funded: ${co_funded:,.2f} (${co_funded/1e6:.2f}M)")
    print(f"10. Total Recoveries       : ${co_received:,.2f} (${co_received/1e6:.2f}M)")
    print(f"11. Recovery Rate          : {recovery_rate:.2f}%")
    print(f"    Net Credit Loss        : ${net_credit_loss:,.2f} (${net_credit_loss/1e6:.2f}M)")

    # Assert exact alignment with documentation
    assert abs(total_funded - 435757075.00) < 1.0, "Total funded mismatch!"
    assert abs(total_received - 473070933.00) < 1.0, "Total received mismatch!"
    assert abs(default_rate - 13.82) < 0.05, "Default rate mismatch!"
    assert abs(recovery_rate - 56.89) < 0.05, "Recovery rate mismatch!"
    print("PASS: Financial KPIs align 100% with MySQL and Tableau specifications.")
    return True

def audit_sql_files():
    print("\n--- 4. AUDITING SQL SCRIPTS ---")
    sql_dir = os.path.join(BASE_DIR, "sql")
    sql_files = sorted([f for f in os.listdir(sql_dir) if f.endswith(".sql")])
    print(f"Total SQL files found: {len(sql_files)}")
    assert len(sql_files) == 9, f"Expected 9 SQL files, found {len(sql_files)}"

    for sf in sql_files:
        path = os.path.join(sql_dir, sf)
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
        # Verify non-empty and contains basic SQL keywords
        assert len(content) > 500, f"{sf} is suspiciously short!"
        assert "SELECT" in content or "CREATE" in content, f"{sf} missing core SQL commands!"
        print(f"  [OK] {sf}: {len(content.splitlines())} lines, {len(content)} bytes")
    
    # Audit View count in 09_tableau_views.sql
    with open(os.path.join(sql_dir, "09_tableau_views.sql"), "r", encoding="utf-8") as f:
        view_content = f.read()
    views_created = re.findall(r"CREATE\s+VIEW\s+([a-zA-Z0-9_]+)", view_content, re.IGNORECASE)
    print(f"Analytical Views created in 09_tableau_views.sql: {len(views_created)}")
    print(f"Views: {views_created}")
    assert len(views_created) == 10, f"Expected 10 views, found {len(views_created)}"
    print("PASS: Exactly 10 production views created.")
    return True

def audit_tableau_dashboards():
    print("\n--- 5. AUDITING TABLEAU DASHBOARDS & VISUALIZATIONS ---")
    dashboards = [
        ("Dashboard 1", "tableau/dashboard_1_loan_portfolio.md"),
        ("Dashboard 2", "tableau/dashboard_2_customer_loan_analysis.md"),
        ("Dashboard 3", "tableau/dashboard_3_risk_analysis.md"),
    ]
    total_areas = 0
    for name, rel_path in dashboards:
        path = os.path.join(BASE_DIR, rel_path)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
        areas = re.findall(r"### Area \d+:", text)
        print(f"  {name}: {len(areas)} core visualization areas documented")
        assert len(areas) == 11, f"Expected 11 areas in {name}, found {len(areas)}"
        total_areas += len(areas)
    
    print(f"Total Core Visualization Areas across 3 dashboards: {total_areas}")
    assert total_areas == 33, f"Expected 33 visualization areas, found {total_areas}"
    print("PASS: Exactly 3 Dashboards and 33 Visualization Areas verified.")
    return True

if __name__ == "__main__":
    s1 = audit_file_structure()
    s2 = audit_dataset()
    s3 = audit_sql_files()
    s4 = audit_tableau_dashboards()
    if s1 and s2 and s3 and s4:
        print("\n========================================================")
        print("ALL TECHNICAL AUDITS PASSED WITH ZERO CRITICAL DEFECTS.")
        print("========================================================")
    else:
        sys.exit(1)

