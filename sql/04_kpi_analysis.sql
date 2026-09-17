-- ========================================================
-- SCRIPT: 04_kpi_analysis.sql
-- PROJECT: Bank Loan Lending Data Analytics
-- PURPOSE: Compute core executive financial KPIs, Good vs Bad metrics, and MTD/MoM growth
-- RDBMS: MySQL 8.0+
-- ========================================================

USE bank_loan_analytics;

-- ========================================================
-- 1. OVERALL PORTFOLIO CORE FINANCIAL KPIS
-- Computes the 11 primary financial metrics across the entire loan portfolio
-- ========================================================
SELECT 
    -- 1. Total Loan Applications
    COUNT(id) AS total_loan_applications,
    
    -- 2. Total Funded Amount (Principal Disbursed)
    SUM(loan_amount) AS total_funded_amount,
    
    -- 3. Total Received Amount (Cash Collected from Principal + Interest + Fees)
    SUM(total_payment) AS total_received_amount,
    
    -- 4. Average Interest Rate (Decimal and Percentage)
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    
    -- 5. Average Loan Amount
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    
    -- 6. Default / Charged-Off Rate (Charged-Off Count / Total Applications)
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) / COUNT(id) * 100, 2) AS default_rate_pct,
    
    -- 7. Fully Paid Rate (Fully Paid Count / Total Applications)
    ROUND(COUNT(CASE WHEN loan_status = 'Fully Paid' THEN 1 END) / COUNT(id) * 100, 2) AS fully_paid_rate_pct,
    
    -- 8. Average Debt-to-Income (DTI) Ratio
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    
    -- 9. Total Charged-Off Amount (Gross Principal Disbursed on Defaulted Loans)
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS total_charged_off_funded,
    
    -- 10. Total Recoveries / Cash Collected on Defaulted Loans
    SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) AS total_recoveries_received,
    
    -- 11. Recovery Rate on Defaulted Loans (Cash Collected / Funded Amount on Charged Off loans)
    ROUND(
        SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) /
        NULLIF(SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END), 0) * 100, 
        2
    ) AS recovery_rate_pct,
    
    -- Net Default Loss (Principal Disbursed minus Cash Collected on Defaults)
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount - total_payment ELSE 0 END) AS net_default_loss
FROM loan_data;


-- ========================================================
-- 2. GOOD LOAN VS BAD LOAN PORTFOLIO SEGMENTATION
-- Good Loans: 'Fully Paid' + 'Current' (performing or satisfied obligations)
-- Bad Loans: 'Charged Off' (uncollectible / written off)
-- ========================================================
SELECT
    'Good Loans' AS loan_category,
    COUNT(id) AS total_applications,
    ROUND(COUNT(id) / (SELECT COUNT(*) FROM loan_data) * 100, 2) AS application_pct,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct
FROM loan_data
WHERE loan_status IN ('Fully Paid', 'Current')

UNION ALL

SELECT
    'Bad Loans (Charged Off)' AS loan_category,
    COUNT(id) AS total_applications,
    ROUND(COUNT(id) / (SELECT COUNT(*) FROM loan_data) * 100, 2) AS application_pct,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct
FROM loan_data
WHERE loan_status = 'Charged Off';


-- ========================================================
-- 3. MONTH-TO-DATE (MTD) AND MONTH-OVER-MONTH (MoM) GROWTH
-- Context: In the 2021 dataset, Month 12 (December) is the latest month (MTD),
-- and Month 11 (November) represents Previous Month-to-Date (PMTD).
-- ========================================================
WITH monthly_cohorts AS (
    SELECT 
        MONTH(issue_date) AS issue_month,
        MONTHNAME(issue_date) AS month_name,
        COUNT(id) AS monthly_applications,
        SUM(loan_amount) AS monthly_funded,
        SUM(total_payment) AS monthly_received,
        AVG(int_rate) AS monthly_avg_int_rate,
        AVG(dti) AS monthly_avg_dti
    FROM loan_data
    WHERE YEAR(issue_date) = 2021
    GROUP BY MONTH(issue_date), MONTHNAME(issue_date)
),
mom_comparison AS (
    SELECT
        curr.issue_month,
        curr.month_name,
        curr.monthly_applications AS mtd_applications,
        prev.monthly_applications AS pmtd_applications,
        ROUND((curr.monthly_applications - prev.monthly_applications) / prev.monthly_applications * 100, 2) AS mom_applications_pct,
        
        curr.monthly_funded AS mtd_funded,
        prev.monthly_funded AS pmtd_funded,
        ROUND((curr.monthly_funded - prev.monthly_funded) / prev.monthly_funded * 100, 2) AS mom_funded_pct,
        
        curr.monthly_received AS mtd_received,
        prev.monthly_received AS pmtd_received,
        ROUND((curr.monthly_received - prev.monthly_received) / prev.monthly_received * 100, 2) AS mom_received_pct,
        
        ROUND(curr.monthly_avg_int_rate * 100, 2) AS mtd_avg_int_rate,
        ROUND(prev.monthly_avg_int_rate * 100, 2) AS pmtd_avg_int_rate,
        ROUND((curr.monthly_avg_int_rate - prev.monthly_avg_int_rate) / prev.monthly_avg_int_rate * 100, 2) AS mom_int_rate_pct,
        
        ROUND(curr.monthly_avg_dti * 100, 2) AS mtd_avg_dti,
        ROUND(prev.monthly_avg_dti * 100, 2) AS pmtd_avg_dti,
        ROUND((curr.monthly_avg_dti - prev.monthly_avg_dti) / prev.monthly_avg_dti * 100, 2) AS mom_dti_pct
    FROM monthly_cohorts curr
    LEFT JOIN monthly_cohorts prev ON curr.issue_month = prev.issue_month + 1
)
SELECT *
FROM mom_comparison
WHERE issue_month = 12;

