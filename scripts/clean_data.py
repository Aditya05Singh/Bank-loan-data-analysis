"""
clean_data.py - Bank Loan Lending Data Cleaning Pipeline

Reproducible data cleaning and validation for the Bank Loan Lending dataset.
Input:  data/raw/loan_data_raw.csv
Output: data/cleaned/loan_data_cleaned.csv
"""

import csv
from datetime import datetime
import os
import sys

def parse_date(date_str):
    """Parses date string in M/D/YYYY format and returns YYYY-MM-DD."""
    if not date_str or not date_str.strip():
        return ""
    val = date_str.strip()
    try:
        dt = datetime.strptime(val, "%m/%d/%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        try:
            dt = datetime.strptime(val, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return ""

def standardize_purpose(purpose_str):
    """Standardizes loan purpose string to Title Case with consistent spacing."""
    if not purpose_str:
        return "Other"
    p = purpose_str.strip().lower().replace("_", " ")
    mapping = {
        "debt consolidation": "Debt Consolidation",
        "credit card": "Credit Card",
        "home improvement": "Home Improvement",
        "major purchase": "Major Purchase",
        "small business": "Small Business",
        "car": "Car",
        "wedding": "Wedding",
        "medical": "Medical",
        "moving": "Moving",
        "vacation": "Vacation",
        "house": "House",
        "educational": "Educational",
        "renewable energy": "Renewable Energy",
        "other": "Other"
    }
    return mapping.get(p, p.title())

def clean_dataset(raw_path, cleaned_path):
    if not os.path.exists(raw_path):
        print(f"Error: Raw file {raw_path} not found.")
        sys.exit(1)

    print(f"Reading raw data from {raw_path}...")
    with open(raw_path, mode="r", encoding="utf-8", errors="replace") as f_in:
        reader = csv.DictReader(f_in)
        raw_rows = list(reader)

    initial_row_count = len(raw_rows)
    print(f"Initial raw rows: {initial_row_count}")

    cleaned_rows = []
    seen_ids = set()
    duplicate_count = 0
    records_removed = 0
    null_emp_title_count = 0

    for idx, row in enumerate(raw_rows):
        loan_id = row.get("id", "").strip()
        if not loan_id:
            records_removed += 1
            continue

        if loan_id in seen_ids:
            duplicate_count += 1
            records_removed += 1
            continue
        seen_ids.add(loan_id)

        # Clean strings
        address_state = row.get("address_state", "").strip().upper()
        application_type = row.get("application_type", "").strip().upper()
        emp_length = row.get("emp_length", "").strip()
        
        emp_title = row.get("emp_title", "").strip()
        if not emp_title:
            emp_title = "Unspecified"
            null_emp_title_count += 1
        
        grade = row.get("grade", "").strip().upper()
        sub_grade = row.get("sub_grade", "").strip().upper()
        home_ownership = row.get("home_ownership", "").strip().upper()
        loan_status = row.get("loan_status", "").strip()
        member_id = row.get("member_id", "").strip()
        purpose = standardize_purpose(row.get("purpose", ""))
        
        # Term: strip whitespace, ensure format '36 months' or '60 months'
        term = row.get("term", "").strip()

        verification_status = row.get("verification_status", "").strip()

        # Financial values & numeric checks
        try:
            annual_income = round(float(row.get("annual_income", 0)), 2)
            dti = round(float(row.get("dti", 0)), 4)
            installment = round(float(row.get("installment", 0)), 2)
            int_rate = round(float(row.get("int_rate", 0)), 4)
            loan_amount = round(float(row.get("loan_amount", 0)), 2)
            total_acc = int(float(row.get("total_acc", 0)))
            total_payment = round(float(row.get("total_payment", 0)), 2)
        except (ValueError, TypeError) as e:
            print(f"Row {idx} numeric parse error: {e}. Skipping row.")
            records_removed += 1
            continue

        # Range validation: amounts cannot be negative
        if loan_amount <= 0 or annual_income < 0 or int_rate < 0 or dti < 0:
            print(f"Row {idx} failed sanity range checks. Skipping row.")
            records_removed += 1
            continue

        # Dates to ISO YYYY-MM-DD
        issue_date = parse_date(row.get("issue_date", ""))
        last_credit_pull_date = parse_date(row.get("last_credit_pull_date", ""))
        last_payment_date = parse_date(row.get("last_payment_date", ""))
        next_payment_date = parse_date(row.get("next_payment_date", ""))

        if not issue_date:
            print(f"Row {idx} missing valid issue_date. Skipping row.")
            records_removed += 1
            continue

        cleaned_row = {
            "id": loan_id,
            "address_state": address_state,
            "application_type": application_type,
            "emp_length": emp_length,
            "emp_title": emp_title,
            "grade": grade,
            "home_ownership": home_ownership,
            "issue_date": issue_date,
            "last_credit_pull_date": last_credit_pull_date,
            "last_payment_date": last_payment_date,
            "loan_status": loan_status,
            "next_payment_date": next_payment_date,
            "member_id": member_id,
            "purpose": purpose,
            "sub_grade": sub_grade,
            "term": term,
            "verification_status": verification_status,
            "annual_income": f"{annual_income:.2f}",
            "dti": f"{dti:.4f}",
            "installment": f"{installment:.2f}",
            "int_rate": f"{int_rate:.4f}",
            "loan_amount": f"{loan_amount:.2f}",
            "total_acc": total_acc,
            "total_payment": f"{total_payment:.2f}",
        }
        cleaned_rows.append(cleaned_row)

    final_row_count = len(cleaned_rows)
    print(f"Cleaned rows: {final_row_count}")
    print(f"Duplicate IDs: {duplicate_count}")
    print(f"Records removed: {records_removed}")
    print(f"Null emp_title standardized: {null_emp_title_count}")

    # Write cleaned CSV
    fieldnames = list(cleaned_rows[0].keys())
    os.makedirs(os.path.dirname(cleaned_path), exist_ok=True)
    with open(cleaned_path, mode="w", encoding="utf-8", newline="") as f_out:
        writer = csv.DictWriter(f_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cleaned_rows)

    print(f"Cleaned dataset written successfully to: {cleaned_path}")
    return initial_row_count, final_row_count, len(fieldnames)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    raw_csv = os.path.join(base_dir, "data", "raw", "loan_data_raw.csv")
    cleaned_csv = os.path.join(base_dir, "data", "cleaned", "loan_data_cleaned.csv")
    clean_dataset(raw_csv, cleaned_csv)

