-- ========================================================
-- SCRIPT: 06_customer_analysis.sql
-- PROJECT: Bank Loan Lending Data Analytics
-- PURPOSE: Detailed applicant demographic, income, employment, and underwriting profile analysis
-- RDBMS: MySQL 8.0+
-- ========================================================

USE bank_loan_analytics;

-- --------------------------------------------------------
-- 1. LOANS BY HOME OWNERSHIP STATUS
-- Portfolio split across RENT, MORTGAGE, OWN, OTHER, NONE
-- --------------------------------------------------------
SELECT 
    home_ownership,
    COUNT(id) AS total_loans,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_loans,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY home_ownership
ORDER BY total_loans DESC;


-- --------------------------------------------------------
-- 2. LOANS BY EMPLOYMENT LENGTH
-- Borrower stability and experience analysis
-- Standardized employment tenure buckets
-- --------------------------------------------------------
SELECT 
    emp_length,
    CASE 
        WHEN emp_length = '< 1 year' THEN 1
        WHEN emp_length = '1 year' THEN 2
        WHEN emp_length = '2 years' THEN 3
        WHEN emp_length = '3 years' THEN 4
        WHEN emp_length = '4 years' THEN 5
        WHEN emp_length = '5 years' THEN 6
        WHEN emp_length = '6 years' THEN 7
        WHEN emp_length = '7 years' THEN 8
        WHEN emp_length = '8 years' THEN 9
        WHEN emp_length = '9 years' THEN 10
        WHEN emp_length = '10+ years' THEN 11
        ELSE 12
    END AS sort_order,
    COUNT(id) AS total_loans,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_loans,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY emp_length, sort_order
ORDER BY sort_order ASC;


-- --------------------------------------------------------
-- 3. LOANS BY INCOME VERIFICATION STATUS
-- Underwriting rigor audit (Verified, Source Verified, Not Verified)
-- --------------------------------------------------------
SELECT 
    verification_status,
    COUNT(id) AS total_loans,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_loans,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(annual_income), 2) AS avg_annual_income,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY verification_status
ORDER BY total_loans DESC;


-- --------------------------------------------------------
-- 4. LOAN METRICS BY ANNUAL INCOME RANGE
-- Evaluates capital demand, average ticket size, and DTI across income brackets
-- --------------------------------------------------------
SELECT 
    CASE 
        WHEN annual_income < 30000 THEN '1. Under $30,000'
        WHEN annual_income BETWEEN 30000 AND 59999.99 THEN '2. $30,000 - $59,999'
        WHEN annual_income BETWEEN 60000 AND 89999.99 THEN '3. $60,000 - $89,999'
        WHEN annual_income BETWEEN 90000 AND 119999.99 THEN '4. $90,000 - $119,999'
        ELSE '5. $120,000 and Above'
    END AS income_range,
    COUNT(id) AS total_loans,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_loans,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY income_range
ORDER BY income_range ASC;


-- --------------------------------------------------------
-- 5. LOANS BY REPAYMENT TERM
-- 36 months vs 60 months breakdown
-- --------------------------------------------------------
SELECT 
    term,
    COUNT(id) AS total_loans,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_loans,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(SUM(loan_amount) * 100.0 / (SELECT SUM(loan_amount) FROM loan_data), 2) AS pct_of_funded_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY term
ORDER BY total_loans DESC;


-- --------------------------------------------------------
-- 6. TOP 5 LOAN PURPOSES BY AVERAGE INTEREST RATE
-- Identifies the highest risk-priced loan categories
-- --------------------------------------------------------
SELECT 
    purpose,
    COUNT(id) AS total_loans,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY purpose
ORDER BY avg_int_rate_pct DESC
LIMIT 5;


-- --------------------------------------------------------
-- 7. AVERAGE DTI BY INCOME RANGE
-- Inverse correlation analysis between income capacity and debt burden
-- --------------------------------------------------------
SELECT 
    CASE 
        WHEN annual_income < 30000 THEN '1. Under $30,000'
        WHEN annual_income BETWEEN 30000 AND 59999.99 THEN '2. $30,000 - $59,999'
        WHEN annual_income BETWEEN 60000 AND 89999.99 THEN '3. $60,000 - $89,999'
        WHEN annual_income BETWEEN 90000 AND 119999.99 THEN '4. $90,000 - $119,999'
        ELSE '5. $120,000 and Above'
    END AS income_range,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    ROUND(MIN(dti) * 100, 2) AS min_dti_pct,
    ROUND(MAX(dti) * 100, 2) AS max_dti_pct,
    ROUND(AVG(annual_income), 2) AS avg_annual_income
FROM loan_data
GROUP BY income_range
ORDER BY income_range ASC;


-- --------------------------------------------------------
-- 8. LOAN COUNT AND AVERAGE LOAN AMOUNT BY GRADE
-- Credit grade sizing profile
-- --------------------------------------------------------
SELECT 
    grade,
    COUNT(id) AS total_loans,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_loans,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    SUM(loan_amount) AS total_funded_amount
FROM loan_data
GROUP BY grade
ORDER BY grade ASC;


-- --------------------------------------------------------
-- 9. TOP 10 STATES BY LOAN APPLICATION COUNT
-- Geographic applicant volume ranking
-- --------------------------------------------------------
SELECT 
    address_state AS state_code,
    COUNT(id) AS total_applications,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_total_applications,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY address_state
ORDER BY total_applications DESC
LIMIT 10;

