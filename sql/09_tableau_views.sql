-- ========================================================
-- SCRIPT: 09_tableau_views.sql
-- PROJECT: Bank Loan Lending Data Analytics
-- PURPOSE: Create 10 production-ready analytical views optimized for Tableau & BI consumption
-- RDBMS: MySQL 8.0+
-- ========================================================

USE bank_loan_analytics;

-- Drop views if recreating
DROP VIEW IF EXISTS vw_loan_kpis;
DROP VIEW IF EXISTS vw_monthly_loan_summary;
DROP VIEW IF EXISTS vw_loan_status_distribution;
DROP VIEW IF EXISTS vw_grade_analysis;
DROP VIEW IF EXISTS vw_purpose_analysis;
DROP VIEW IF EXISTS vw_customer_analysis;
DROP VIEW IF EXISTS vw_risk_analysis;
DROP VIEW IF EXISTS vw_state_analysis;
DROP VIEW IF EXISTS vw_income_analysis;
DROP VIEW IF EXISTS vw_recovery_analysis;

-- ========================================================
-- 1. VIEW: vw_loan_kpis
-- Purpose: Feeds high-level KPI cards on Dashboard 1 (Total, MTD, MoM, and Good/Bad splits)
-- ========================================================
CREATE VIEW vw_loan_kpis AS
SELECT 
    COUNT(id) AS total_loan_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    
    -- Good Loan Metrics
    COUNT(CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN 1 END) AS good_loan_applications,
    ROUND(COUNT(CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN 1 END) * 100.0 / COUNT(id), 2) AS good_loan_pct,
    SUM(CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN loan_amount ELSE 0 END) AS good_loan_funded_amount,
    SUM(CASE WHEN loan_status IN ('Fully Paid', 'Current') THEN total_payment ELSE 0 END) AS good_loan_received_amount,
    
    -- Bad Loan Metrics
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS bad_loan_applications,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS bad_loan_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS bad_loan_funded_amount,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) AS bad_loan_received_amount,
    
    -- MTD Metrics (December 2021)
    COUNT(CASE WHEN MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021 THEN 1 END) AS mtd_applications,
    SUM(CASE WHEN MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021 THEN loan_amount ELSE 0 END) AS mtd_funded_amount,
    SUM(CASE WHEN MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021 THEN total_payment ELSE 0 END) AS mtd_received_amount,
    ROUND(AVG(CASE WHEN MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021 THEN int_rate END) * 100, 2) AS mtd_avg_int_rate_pct,
    ROUND(AVG(CASE WHEN MONTH(issue_date) = 12 AND YEAR(issue_date) = 2021 THEN dti END) * 100, 2) AS mtd_avg_dti_pct
FROM loan_data;


-- ========================================================
-- 2. VIEW: vw_monthly_loan_summary
-- Purpose: Powers chronological line/area charts, MoM tables, and seasonal analysis
-- ========================================================
CREATE VIEW vw_monthly_loan_summary AS
SELECT 
    YEAR(issue_date) AS issue_year,
    MONTH(issue_date) AS month_number,
    MONTHNAME(issue_date) AS month_name,
    DATE_FORMAT(issue_date, '%Y-%m') AS year_month,
    CONCAT('Q', QUARTER(issue_date)) AS issue_quarter,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS default_count,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY 
    YEAR(issue_date), 
    MONTH(issue_date), 
    MONTHNAME(issue_date), 
    DATE_FORMAT(issue_date, '%Y-%m'), 
    CONCAT('Q', QUARTER(issue_date));


-- ========================================================
-- 3. VIEW: vw_loan_status_distribution
-- Purpose: Powers summary grid by loan status on Dashboard 1
-- ========================================================
CREATE VIEW vw_loan_status_distribution AS
SELECT 
    loan_status,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    
    -- MTD Metrics (Month 12)
    SUM(CASE WHEN MONTH(issue_date) = 12 THEN loan_amount ELSE 0 END) AS mtd_funded_amount,
    SUM(CASE WHEN MONTH(issue_date) = 12 THEN total_payment ELSE 0 END) AS mtd_received_amount,
    
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount
FROM loan_data
GROUP BY loan_status;


-- ========================================================
-- 4. VIEW: vw_grade_analysis
-- Purpose: Credit risk ladder and pricing vs default matrix by grade and subgrade
-- ========================================================
CREATE VIEW vw_grade_analysis AS
SELECT 
    grade,
    sub_grade,
    COUNT(id) AS total_loans,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS default_count,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY grade, sub_grade;


-- ========================================================
-- 5. VIEW: vw_purpose_analysis
-- Purpose: Lending volume, pricing, and default risk by borrowing purpose
-- ========================================================
CREATE VIEW vw_purpose_analysis AS
SELECT 
    purpose,
    COUNT(id) AS total_loans,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS default_count,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY purpose;


-- ========================================================
-- 6. VIEW: vw_customer_analysis
-- Purpose: Borrower demographics: employment length, home ownership, verification status, and term
-- ========================================================
CREATE VIEW vw_customer_analysis AS
SELECT 
    id AS loan_id,
    member_id AS customer_id,
    home_ownership,
    emp_length,
    verification_status,
    term,
    grade,
    purpose,
    address_state AS state,
    annual_income,
    CASE 
        WHEN annual_income < 30000 THEN 'Under $30,000'
        WHEN annual_income BETWEEN 30000 AND 59999.99 THEN '$30,000 - $59,999'
        WHEN annual_income BETWEEN 60000 AND 89999.99 THEN '$60,000 - $89,999'
        WHEN annual_income BETWEEN 90000 AND 119999.99 THEN '$90,000 - $119,999'
        ELSE '$120,000 and Above'
    END AS income_range,
    dti,
    CASE 
        WHEN dti < 0.10 THEN 'Under 10%'
        WHEN dti BETWEEN 0.10 AND 0.1499 THEN '10% - 14.99%'
        WHEN dti BETWEEN 0.15 AND 0.1999 THEN '15% - 19.99%'
        WHEN dti BETWEEN 0.20 AND 0.2499 THEN '20% - 24.99%'
        ELSE '25% and Above'
    END AS dti_range,
    int_rate,
    loan_amount,
    total_payment,
    loan_status,
    issue_date
FROM loan_data;


-- ========================================================
-- 7. VIEW: vw_risk_analysis
-- Purpose: Risk metrics, high-risk flag, and loss assessment
-- ========================================================
CREATE VIEW vw_risk_analysis AS
SELECT 
    id AS loan_id,
    grade,
    sub_grade,
    purpose,
    home_ownership,
    emp_length,
    annual_income,
    dti,
    int_rate,
    loan_amount,
    total_payment,
    loan_status,
    issue_date,
    CASE WHEN loan_status = 'Charged Off' THEN 1 ELSE 0 END AS is_default,
    CASE 
        WHEN loan_status = 'Charged Off' THEN loan_amount 
        ELSE 0 
    END AS charged_off_amount,
    CASE 
        WHEN loan_status = 'Charged Off' THEN total_payment 
        ELSE 0 
    END AS recovered_amount,
    CASE 
        WHEN loan_status = 'Charged Off' THEN loan_amount - total_payment 
        ELSE 0 
    END AS net_loss_amount,
    CASE 
        WHEN dti >= 0.20 OR grade IN ('D', 'E', 'F', 'G') THEN 'High Risk'
        ELSE 'Standard Risk'
    END AS risk_segment
FROM loan_data;


-- ========================================================
-- 8. VIEW: vw_state_analysis
-- Purpose: Geographic choropleth map and state performance rankings
-- ========================================================
CREATE VIEW vw_state_analysis AS
SELECT 
    address_state AS state_code,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS default_count,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY address_state;


-- ========================================================
-- 9. VIEW: vw_income_analysis
-- Purpose: Income bracket performance, debt leverage, and default rates
-- ========================================================
CREATE VIEW vw_income_analysis AS
SELECT 
    CASE 
        WHEN annual_income < 30000 THEN '1. Under $30,000'
        WHEN annual_income BETWEEN 30000 AND 59999.99 THEN '2. $30,000 - $59,999'
        WHEN annual_income BETWEEN 60000 AND 89999.99 THEN '3. $60,000 - $89,999'
        WHEN annual_income BETWEEN 90000 AND 119999.99 THEN '4. $90,000 - $119,999'
        ELSE '5. $120,000 and Above'
    END AS income_bracket,
    COUNT(id) AS total_loans,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS default_count,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY income_bracket;


-- ========================================================
-- 10. VIEW: vw_recovery_analysis
-- Purpose: In-depth recovery and Loss Given Default (LGD) metrics on defaulted loans
-- ========================================================
CREATE VIEW vw_recovery_analysis AS
SELECT 
    YEAR(issue_date) AS issue_year,
    grade,
    purpose,
    COUNT(id) AS total_charged_off_loans,
    SUM(loan_amount) AS gross_charged_off_amount,
    SUM(total_payment) AS total_recoveries_received,
    SUM(loan_amount - total_payment) AS net_credit_loss,
    ROUND(
        SUM(total_payment) * 100.0 / NULLIF(SUM(loan_amount), 0),
        2
    ) AS recovery_rate_pct
FROM loan_data
WHERE loan_status = 'Charged Off'
GROUP BY YEAR(issue_date), grade, purpose;

