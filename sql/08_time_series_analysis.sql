-- ========================================================
-- SCRIPT: 08_time_series_analysis.sql
-- PROJECT: Bank Loan Lending Data Analytics
-- PURPOSE: Comprehensive chronological time-series analysis (Monthly, Quarterly, Annual, MoM, and Cumulative)
-- RDBMS: MySQL 8.0+
-- ========================================================

USE bank_loan_analytics;

-- --------------------------------------------------------
-- 1. COMPLETE MONTHLY TIME-SERIES WITH CHRONOLOGICAL SORTING
-- Generates year, quarter, month, month_name, year_month, and core metrics
-- --------------------------------------------------------
SELECT 
    YEAR(issue_date) AS issue_year,
    CONCAT('Q', QUARTER(issue_date)) AS issue_quarter,
    MONTH(issue_date) AS month_number,
    MONTHNAME(issue_date) AS month_name,
    DATE_FORMAT(issue_date, '%Y-%m') AS year_month,
    
    -- Volume & Monetary Aggregations
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    
    -- Pricing & Sizing Averages
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct,
    
    -- Performance & Defaults
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS charged_off_amount,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) AS recoveries_amount
FROM loan_data
GROUP BY 
    YEAR(issue_date), 
    QUARTER(issue_date), 
    MONTH(issue_date), 
    MONTHNAME(issue_date), 
    DATE_FORMAT(issue_date, '%Y-%m')
ORDER BY 
    issue_year ASC, 
    month_number ASC;


-- --------------------------------------------------------
-- 2. MONTH-OVER-MONTH (MoM) GROWTH ANALYSIS USING WINDOW FUNCTIONS
-- Calculates preceding month values and percentage change using LAG()
-- --------------------------------------------------------
WITH monthly_metrics AS (
    SELECT 
        MONTH(issue_date) AS month_num,
        MONTHNAME(issue_date) AS month_name,
        DATE_FORMAT(issue_date, '%Y-%m') AS year_month,
        COUNT(id) AS applications,
        SUM(loan_amount) AS funded_amount,
        SUM(total_payment) AS received_amount,
        AVG(int_rate) AS avg_int_rate
    FROM loan_data
    GROUP BY MONTH(issue_date), MONTHNAME(issue_date), DATE_FORMAT(issue_date, '%Y-%m')
)
SELECT 
    month_num,
    month_name,
    year_month,
    applications,
    LAG(applications, 1) OVER (ORDER BY month_num) AS prev_month_applications,
    ROUND(
        (applications - LAG(applications, 1) OVER (ORDER BY month_num)) * 100.0 / 
        LAG(applications, 1) OVER (ORDER BY month_num), 
        2
    ) AS mom_applications_growth_pct,
    
    funded_amount,
    LAG(funded_amount, 1) OVER (ORDER BY month_num) AS prev_month_funded,
    ROUND(
        (funded_amount - LAG(funded_amount, 1) OVER (ORDER BY month_num)) * 100.0 / 
        LAG(funded_amount, 1) OVER (ORDER BY month_num), 
        2
    ) AS mom_funded_growth_pct,
    
    received_amount,
    LAG(received_amount, 1) OVER (ORDER BY month_num) AS prev_month_received,
    ROUND(
        (received_amount - LAG(received_amount, 1) OVER (ORDER BY month_num)) * 100.0 / 
        LAG(received_amount, 1) OVER (ORDER BY month_num), 
        2
    ) AS mom_received_growth_pct
FROM monthly_metrics
ORDER BY month_num ASC;


-- --------------------------------------------------------
-- 3. CUMULATIVE (RUNNING TOTAL) CAPITAL DISBURSEMENT & COLLECTIONS
-- Evaluates capital inflow vs outflow over time using SUM() OVER (ORDER BY ...)
-- --------------------------------------------------------
WITH monthly_totals AS (
    SELECT 
        MONTH(issue_date) AS month_num,
        MONTHNAME(issue_date) AS month_name,
        SUM(loan_amount) AS monthly_funded,
        SUM(total_payment) AS monthly_received
    FROM loan_data
    GROUP BY MONTH(issue_date), MONTHNAME(issue_date)
)
SELECT 
    month_num,
    month_name,
    monthly_funded,
    SUM(monthly_funded) OVER (ORDER BY month_num) AS cumulative_funded_amount,
    monthly_received,
    SUM(monthly_received) OVER (ORDER BY month_num) AS cumulative_received_amount,
    ROUND(
        SUM(monthly_received) OVER (ORDER BY month_num) * 100.0 /
        SUM(monthly_funded) OVER (ORDER BY month_num),
        2
    ) AS cumulative_collection_ratio_pct
FROM monthly_totals
ORDER BY month_num ASC;


-- --------------------------------------------------------
-- 4. QUARTERLY SUMMARY
-- High-level quarterly pacing of lending volume
-- --------------------------------------------------------
SELECT 
    YEAR(issue_date) AS issue_year,
    CONCAT('Q', QUARTER(issue_date)) AS issue_quarter,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS quarterly_default_rate_pct
FROM loan_data
GROUP BY YEAR(issue_date), QUARTER(issue_date)
ORDER BY issue_year ASC, QUARTER(issue_date) ASC;


-- --------------------------------------------------------
-- 5. ANNUAL SUMMARY WITH RECOVERY RATE
-- Annual aggregate portfolio performance metrics
-- --------------------------------------------------------
SELECT 
    YEAR(issue_date) AS issue_year,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS total_charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS annual_default_rate_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS total_charged_off_amount,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) AS total_recoveries_received,
    ROUND(
        SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) * 100.0 /
        NULLIF(SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END), 0),
        2
    ) AS annual_recovery_rate_pct
FROM loan_data
GROUP BY YEAR(issue_date)
ORDER BY issue_year ASC;

