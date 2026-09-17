"""
generate_tableau_twb.py - Generates an actual, valid Tableau Workbook (.twb) XML file
for the Bank Loan Lending Data Analytics project.
"""

import os
import xml.etree.ElementTree as ET
from xml.dom import minidom

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TWB_PATH = os.path.join(BASE_DIR, "tableau", "Bank_Loan_Lending_Analytics.twb")

def create_twb():
    print(f"Generating Tableau Workbook at: {TWB_PATH}...")
    
    root = ET.Element("workbook", {
        "version": "18.1",
        "xmlns:user": "http://www.tableausoftware.com/xml/user"
    })
    
    # Document info
    doc_info = ET.SubElement(root, "document-info")
    ET.SubElement(doc_info, "properties")
    
    # Preferences
    ET.SubElement(root, "preferences")
    
    # Datasources
    datasources = ET.SubElement(root, "datasources")
    datasource = ET.SubElement(datasources, "datasource", {
        "caption": "loan_data_cleaned",
        "inline": "true",
        "name": "federated.loan_data",
        "version": "18.1"
    })
    
    connection = ET.SubElement(datasource, "connection", {"class": "federated"})
    named_connections = ET.SubElement(connection, "named-connections")
    named_conn = ET.SubElement(named_connections, "named-connection", {
        "caption": "loan_data_cleaned",
        "name": "textscan.loan_data"
    })
    
    # Use relative path so workbook is fully portable across machines
    ET.SubElement(named_conn, "connection", {
        "class": "textscan",
        "directory": "../data/cleaned",
        "filename": "loan_data_cleaned.csv",
        "password": "",
        "server": ""
    })
    
    relation = ET.SubElement(connection, "relation", {
        "connection": "textscan.loan_data",
        "name": "loan_data_cleaned.csv",
        "table": "[loan_data_cleaned#csv]",
        "type": "table"
    })
    
    columns_elem = ET.SubElement(relation, "columns", {
        "character-set": "UTF-8",
        "header": "yes",
        "locale": "en_US",
        "separator": ","
    })
    
    cols = [
        ("id", "integer", "0"),
        ("address_state", "string", "1"),
        ("application_type", "string", "2"),
        ("emp_length", "string", "3"),
        ("emp_title", "string", "4"),
        ("grade", "string", "5"),
        ("home_ownership", "string", "6"),
        ("issue_date", "date", "7"),
        ("last_credit_pull_date", "date", "8"),
        ("last_payment_date", "date", "9"),
        ("loan_status", "string", "10"),
        ("next_payment_date", "date", "11"),
        ("member_id", "integer", "12"),
        ("purpose", "string", "13"),
        ("sub_grade", "string", "14"),
        ("term", "string", "15"),
        ("verification_status", "string", "16"),
        ("annual_income", "real", "17"),
        ("dti", "real", "18"),
        ("installment", "real", "19"),
        ("int_rate", "real", "20"),
        ("loan_amount", "real", "21"),
        ("total_acc", "integer", "22"),
        ("total_payment", "real", "23")
    ]
    
    for cname, ctype, ord_val in cols:
        ET.SubElement(columns_elem, "column", {
            "datatype": ctype,
            "name": cname,
            "ordinal": ord_val
        })
        
    aliases = ET.SubElement(datasource, "aliases", {"enabled": "yes"})
    
    # Calculated Fields
    calc_fields = [
        ("Default Flag", "[Calculation_DefaultFlag]", "IF [loan_status] = 'Charged Off' THEN 1 ELSE 0 END", "integer", "measure"),
        ("Default Rate", "[Calculation_DefaultRate]", "SUM([Calculation_DefaultFlag]) / COUNT([id])", "real", "measure"),
        ("Good Loan Flag", "[Calculation_GoodLoanFlag]", "IF [loan_status] = 'Fully Paid' OR [loan_status] = 'Current' THEN 1 ELSE 0 END", "integer", "measure"),
        ("Good Loan Rate", "[Calculation_GoodLoanRate]", "SUM([Calculation_GoodLoanFlag]) / COUNT([id])", "real", "measure"),
        ("Recovery Rate", "[Calculation_RecoveryRate]", "SUM(IF [loan_status] = 'Charged Off' THEN [total_payment] ELSE 0 END) / NULLIF(SUM(IF [loan_status] = 'Charged Off' THEN [loan_amount] ELSE 0 END), 0)", "real", "measure"),
        ("Net Credit Loss", "[Calculation_NetCreditLoss]", "SUM(IF [loan_status] = 'Charged Off' THEN [loan_amount] - [total_payment] ELSE 0 END)", "real", "measure"),
        ("High Risk Flag", "[Calculation_HighRiskFlag]", "IF [dti] >= 0.20 OR [grade] = 'D' OR [grade] = 'E' OR [grade] = 'F' OR [grade] = 'G' THEN 'High Risk' ELSE 'Standard Risk' END", "string", "dimension"),
        ("Loan Amount Range", "[Calculation_LoanAmountRange]", "IF [loan_amount] < 5000 THEN '1. Under $5,000' ELSEIF [loan_amount] <= 9999.99 THEN '2. $5,000 - $9,999' ELSEIF [loan_amount] <= 14999.99 THEN '3. $10,000 - $14,999' ELSEIF [loan_amount] <= 19999.99 THEN '4. $15,000 - $19,999' ELSEIF [loan_amount] <= 24999.99 THEN '5. $20,000 - $24,999' ELSE '6. $25,000 and Above' END", "string", "dimension"),
        ("Income Range", "[Calculation_IncomeRange]", "IF [annual_income] < 30000 THEN '1. Under $30,000' ELSEIF [annual_income] <= 59999.99 THEN '2. $30,000 - $59,999' ELSEIF [annual_income] <= 89999.99 THEN '3. $60,000 - $89,999' ELSEIF [annual_income] <= 119999.99 THEN '4. $90,000 - $119,999' ELSE '5. $120,000 and Above' END", "string", "dimension"),
        ("DTI Range", "[Calculation_DTIRange]", "IF [dti] < 0.10 THEN '1. Under 10.0%' ELSEIF [dti] <= 0.1499 THEN '2. 10.0% - 14.99%' ELSEIF [dti] <= 0.1999 THEN '3. 15.0% - 19.99%' ELSEIF [dti] <= 0.2499 THEN '4. 20.0% - 24.99%' ELSE '5. 25.0% and Above' END", "string", "dimension")
    ]
    
    for caption, calc_id, formula, dtype, role in calc_fields:
        col_node = ET.SubElement(datasource, "column", {
            "caption": caption,
            "datatype": dtype,
            "name": calc_id,
            "role": role,
            "type": "quantitative" if role == "measure" else "nominal"
        })
        ET.SubElement(col_node, "calculation", {
            "class": "tableau",
            "formula": formula
        })
        
    # Worksheets
    worksheets = ET.SubElement(root, "worksheets")
    
    # Define 33 worksheets
    sheet_names = [
        # Dashboard 1 (11)
        "kpi_total_applications",
        "kpi_total_funded",
        "kpi_total_received",
        "kpi_avg_int_rate",
        "kpi_avg_loan_amount",
        "kpi_default_rate",
        "viz_loan_status_distribution",
        "viz_monthly_funded_trend",
        "viz_quarterly_funded",
        "viz_applications_by_year",
        "viz_top10_states_funded",
        # Dashboard 2 (11)
        "viz_cust_home_ownership",
        "viz_cust_emp_length",
        "viz_cust_verification_status",
        "viz_avg_loan_by_income",
        "viz_total_loan_by_income",
        "viz_cust_term_split",
        "viz_top5_purposes_by_rate",
        "viz_avg_dti_by_income",
        "viz_loan_count_by_grade",
        "viz_avg_loan_by_grade",
        "viz_top10_states_count",
        # Dashboard 3 (11)
        "viz_risk_default_rate_by_grade",
        "viz_risk_default_by_purpose",
        "viz_risk_default_by_dti",
        "viz_risk_default_by_int_rate",
        "viz_risk_charged_off_by_year",
        "viz_risk_recovery_rate_by_year",
        "viz_risk_default_by_home",
        "viz_risk_default_by_emp_length",
        "viz_risk_default_by_income",
        "kpi_high_risk_summary",
        "viz_risk_segment_distribution"
    ]
    
    for sname in sheet_names:
        ws = ET.SubElement(worksheets, "worksheet", {"name": sname})
        table = ET.SubElement(ws, "table")
        view = ET.SubElement(table, "view")
        datasources_view = ET.SubElement(view, "datasources")
        ET.SubElement(datasources_view, "datasource", {
            "caption": "loan_data_cleaned",
            "name": "federated.loan_data"
        })
        ET.SubElement(table, "rows")
        ET.SubElement(table, "cols")
        
    # Dashboards
    dashboards = ET.SubElement(root, "dashboards")
    
    dash_specs = [
        ("Dashboard 1 - Loan Portfolio Overview", sheet_names[0:11], 1600, 1000),
        ("Dashboard 2 - Customer & Loan Analysis", sheet_names[11:22], 1600, 1000),
        ("Dashboard 3 - Risk Analysis", sheet_names[22:33], 1600, 1050)
    ]
    
    for dname, dsheets, dwidth, dheight in dash_specs:
        dash = ET.SubElement(dashboards, "dashboard", {"name": dname})
        ET.SubElement(dash, "style")
        size = ET.SubElement(dash, "size", {
            "maxheight": str(dheight),
            "maxwidth": str(dwidth),
            "minheight": str(dheight),
            "minwidth": str(dwidth)
        })
        zones = ET.SubElement(dash, "zones")
        root_zone = ET.SubElement(zones, "zone", {
            "h": "100000",
            "id": "1",
            "type": "layout-basic",
            "w": "100000",
            "x": "0",
            "y": "0"
        })
        
        # Add zones for each worksheet
        zone_id = 2
        for sname in dsheets:
            ET.SubElement(root_zone, "zone", {
                "id": str(zone_id),
                "name": sname,
                "type": "box"
            })
            zone_id += 1
            
    # Windows
    windows = ET.SubElement(root, "windows")
    for dname, _, _, _ in dash_specs:
        win = ET.SubElement(windows, "window", {
            "class": "dashboard",
            "name": dname
        })
        ET.SubElement(win, "active")
        
    # Write to file with pretty formatting
    xml_str = ET.tostring(root, encoding="utf-8")
    parsed = minidom.parseString(xml_str)
    pretty_xml = parsed.toprettyxml(indent="  ", encoding="utf-8")
    
    os.makedirs(os.path.dirname(TWB_PATH), exist_ok=True)
    with open(TWB_PATH, "wb") as f:
        f.write(pretty_xml)
        
    print(f"Tableau Workbook successfully written to: {TWB_PATH}")
    print(f"Workbook size: {os.path.getsize(TWB_PATH) / 1024:.1f} KB")

if __name__ == "__main__":
    create_twb()

