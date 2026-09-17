-- ========================================================
-- SCRIPT: 03_data_quality.sql
-- PROJECT: Bank Loan Lending Data Analytics
-- PURPOSE: Execute and validate comprehensive data quality checks
-- RDBMS: MySQL 8.0+
-- ========================================================

USE bank_loan_analytics;

-- --------------------------------------------------------
-- CHECK 1: Total Record Count Validation
-- Purpose: Verify that the exact expected number of records (38,576) was loaded.
-- Expected Result: total_records = 38576, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 1: Total Record Count' AS check_name,
    COUNT(*) AS observed_count,
    38576 AS expected_count,
    CASE 
        WHEN COUNT(*) = 38576 THEN 'PASS' 
        ELSE 'FAIL: Record count mismatch' 
    END AS status
FROM loan_data;


-- --------------------------------------------------------
-- CHECK 2: Primary Key (ID) Uniqueness & Duplicates
-- Purpose: Ensure every loan record has a distinct, non-duplicate primary key.
-- Expected Result: duplicate_id_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 2: Duplicate Loan IDs' AS check_name,
    COUNT(*) - COUNT(DISTINCT id) AS duplicate_id_count,
    CASE 
        WHEN COUNT(*) = COUNT(DISTINCT id) THEN 'PASS' 
        ELSE 'FAIL: Duplicate primary keys found' 
    END AS status
FROM loan_data;


-- --------------------------------------------------------
-- CHECK 3: Member ID (Customer) Uniqueness Check
-- Purpose: Verify uniqueness of borrower identifiers across the portfolio.
-- Expected Result: duplicate_member_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 3: Duplicate Member IDs' AS check_name,
    COUNT(*) - COUNT(DISTINCT member_id) AS duplicate_member_count,
    CASE 
        WHEN COUNT(*) = COUNT(DISTINCT member_id) THEN 'PASS' 
        ELSE 'INFO: Borrowers with multiple loans exist' 
    END AS status
FROM loan_data;


-- --------------------------------------------------------
-- CHECK 4: Critical Mandatory Financial Fields NULL Check
-- Purpose: Ensure no core financial, status, or date columns contain NULLs.
-- Expected Result: null_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 4: Mandatory Financial NULLs' AS check_name,
    SUM(CASE WHEN id IS NULL THEN 1 ELSE 0 END) AS null_id,
    SUM(CASE WHEN loan_amount IS NULL THEN 1 ELSE 0 END) AS null_loan_amount,
    SUM(CASE WHEN total_payment IS NULL THEN 1 ELSE 0 END) AS null_total_payment,
    SUM(CASE WHEN int_rate IS NULL THEN 1 ELSE 0 END) AS null_int_rate,
    SUM(CASE WHEN dti IS NULL THEN 1 ELSE 0 END) AS null_dti,
    SUM(CASE WHEN annual_income IS NULL THEN 1 ELSE 0 END) AS null_annual_income,
    SUM(CASE WHEN loan_status IS NULL THEN 1 ELSE 0 END) AS null_loan_status,
    SUM(CASE WHEN issue_date IS NULL THEN 1 ELSE 0 END) AS null_issue_date,
    CASE 
        WHEN SUM(
            CASE 
                WHEN id IS NULL OR loan_amount IS NULL OR total_payment IS NULL 
                     OR int_rate IS NULL OR dti IS NULL OR annual_income IS NULL 
                     OR loan_status IS NULL OR issue_date IS NULL 
                THEN 1 ELSE 0 
            END
        ) = 0 THEN 'PASS'
        ELSE 'FAIL: NULLs in mandatory columns'
    END AS status
FROM loan_data;


-- --------------------------------------------------------
-- CHECK 5: Non-Positive Loan Amounts
-- Purpose: Identify any loans where loan_amount is zero or negative.
-- Expected Result: invalid_loan_amount_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 5: Non-Positive Loan Amount' AS check_name,
    COUNT(*) AS invalid_loan_amount_count,
    MIN(loan_amount) AS min_loan_amount,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS' 
        ELSE 'FAIL: Negative or zero loan amount found' 
    END AS status
FROM loan_data
WHERE loan_amount <= 0;


-- --------------------------------------------------------
-- CHECK 6: Negative Payments Received Check
-- Purpose: Ensure total_payment cannot be negative.
-- Expected Result: negative_payment_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 6: Negative Total Payments' AS check_name,
    COUNT(*) AS negative_payment_count,
    MIN(total_payment) AS min_total_payment,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS' 
        ELSE 'FAIL: Negative payment amounts detected' 
    END AS status
FROM loan_data
WHERE total_payment < 0;


-- --------------------------------------------------------
-- CHECK 7: Negative Annual Income Check
-- Purpose: Ensure borrower annual income is non-negative.
-- Expected Result: negative_income_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 7: Negative Annual Income' AS check_name,
    COUNT(*) AS negative_income_count,
    MIN(annual_income) AS min_annual_income,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS' 
        ELSE 'FAIL: Negative income detected' 
    END AS status
FROM loan_data
WHERE annual_income < 0;


-- --------------------------------------------------------
-- CHECK 8: Interest Rate Range Validation
-- Purpose: Verify interest rates fall within valid commercial lending bounds (0.01 to 0.40).
-- Expected Result: invalid_rate_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 8: Interest Rate Range (0.01 - 0.40)' AS check_name,
    COUNT(*) AS invalid_rate_count,
    MIN(int_rate) AS min_observed_rate,
    MAX(int_rate) AS max_observed_rate,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS' 
        ELSE 'FAIL: Interest rate out of bounds' 
    END AS status
FROM loan_data
WHERE int_rate <= 0 OR int_rate > 0.40;


-- --------------------------------------------------------
-- CHECK 9: Debt-to-Income (DTI) Ratio Bounds Check
-- Purpose: Verify DTI ratio falls between 0.0000 and 1.0000.
-- Expected Result: invalid_dti_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 9: DTI Ratio Range (0.00 - 1.00)' AS check_name,
    COUNT(*) AS invalid_dti_count,
    MIN(dti) AS min_observed_dti,
    MAX(dti) AS max_observed_dti,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS' 
        ELSE 'FAIL: DTI out of bounds' 
    END AS status
FROM loan_data
WHERE dti < 0 OR dti > 1.00;


-- --------------------------------------------------------
-- CHECK 10: Date Sequence Chronology Check
-- Purpose: Verify that last payment date is chronologically on or after the issue date.
-- Expected Result: invalid_date_seq_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 10: Date Sequence Chronology' AS check_name,
    COUNT(*) AS invalid_date_seq_count,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS' 
        ELSE 'FAIL: Last payment date precedes issue date' 
    END AS status
FROM loan_data
WHERE last_payment_date IS NOT NULL 
  AND last_payment_date < issue_date;


-- --------------------------------------------------------
-- CHECK 11: Loan Status Domain Check
-- Purpose: Verify loan_status contains only known banking statuses.
-- Expected Result: invalid_status_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 11: Valid Loan Status Domain' AS check_name,
    COUNT(*) AS invalid_status_count,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS' 
        ELSE 'FAIL: Unexpected loan statuses found' 
    END AS status
FROM loan_data
WHERE loan_status NOT IN ('Fully Paid', 'Charged Off', 'Current');


-- --------------------------------------------------------
-- CHECK 12: Credit Grade Domain Check
-- Purpose: Verify grade contains standard credit ratings A through G.
-- Expected Result: invalid_grade_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 12: Credit Grade Domain (A-G)' AS check_name,
    COUNT(*) AS invalid_grade_count,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS' 
        ELSE 'FAIL: Invalid credit grade assigned' 
    END AS status
FROM loan_data
WHERE grade NOT IN ('A', 'B', 'C', 'D', 'E', 'F', 'G');


-- --------------------------------------------------------
-- CHECK 13: Loan Term Domain Check
-- Purpose: Ensure loan term is strictly either '36 months' or '60 months'.
-- Expected Result: invalid_term_count = 0, status = 'PASS'
-- --------------------------------------------------------
SELECT 
    'Check 13: Loan Term Domain' AS check_name,
    COUNT(*) AS invalid_term_count,
    CASE 
        WHEN COUNT(*) = 0 THEN 'PASS' 
        ELSE 'FAIL: Invalid term format found' 
    END AS status
FROM loan_data
WHERE term NOT IN ('36 months', '60 months');


-- --------------------------------------------------------
-- CHECK 14: Outlier and Financial Sanity Profiling
-- Purpose: Identify extreme values in income, loan amounts, and payment ratios for analytical awareness.
-- --------------------------------------------------------
SELECT 
    'Check 14: Financial Outlier Profiling' AS check_name,
    COUNT(CASE WHEN annual_income > 1000000 THEN 1 END) AS high_earners_over_1m,
    COUNT(CASE WHEN loan_amount = 35000 THEN 1 END) AS max_loans_at_ceiling_35k,
    COUNT(CASE WHEN total_payment > loan_amount * 2 THEN 1 END) AS payments_exceeding_2x_principal,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    'PASS: Outlier distribution documented' AS status
FROM loan_data;

