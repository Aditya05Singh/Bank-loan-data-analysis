-- ========================================================
-- SCRIPT: 05_portfolio_analysis.sql
-- PROJECT: Bank Loan Lending Data Analytics
-- PURPOSE: In-depth portfolio composition, credit grade, loan purpose, and geographic allocation
-- RDBMS: MySQL 8.0+
-- ========================================================

USE bank_loan_analytics;

-- --------------------------------------------------------
-- 1. LOAN STATUS DISTRIBUTION
-- Complete breakdown of counts, percentages, funded amounts, and cash collections by status
-- --------------------------------------------------------
SELECT 
    loan_status,
    COUNT(id) AS total_loans,
    ROUND(COUNT(id) * 100.0 / SUM(COUNT(id)) OVER (), 2) AS pct_of_total_loans,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(SUM(loan_amount) * 100.0 / SUM(SUM(loan_amount)) OVER (), 2) AS pct_of_total_funded,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct
FROM loan_data
GROUP BY loan_status
ORDER BY total_funded_amount DESC;


-- --------------------------------------------------------
-- 2. FUNDED AMOUNT AND APPLICATIONS BY MONTH
-- Monthly chronological progression across the portfolio
-- --------------------------------------------------------
SELECT 
    MONTH(issue_date) AS month_number,
    MONTHNAME(issue_date) AS month_name,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct
FROM loan_data
GROUP BY MONTH(issue_date), MONTHNAME(issue_date)
ORDER BY month_number ASC;


-- --------------------------------------------------------
-- 3. FUNDED AMOUNT AND LOAN AMOUNT BY QUARTER
-- Quarterly cohort performance
-- --------------------------------------------------------
SELECT 
    CONCAT('Q', QUARTER(issue_date)) AS quarter_label,
    QUARTER(issue_date) AS quarter_number,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount
FROM loan_data
GROUP BY QUARTER(issue_date)
ORDER BY quarter_number ASC;


-- --------------------------------------------------------
-- 4. APPLICATIONS AND LOAN AMOUNT BY YEAR
-- Annual portfolio totals
-- --------------------------------------------------------
SELECT 
    YEAR(issue_date) AS issue_year,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    SUM(total_payment) AS total_received_amount,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct
FROM loan_data
GROUP BY YEAR(issue_date)
ORDER BY issue_year ASC;


-- --------------------------------------------------------
-- 5. TOP 5 LOAN PURPOSES BY FUNDED AMOUNT
-- Identifies top capital deployment categories using CTE and RANK()
-- --------------------------------------------------------
WITH ranked_purposes AS (
    SELECT 
        purpose,
        COUNT(id) AS total_loans,
        SUM(loan_amount) AS total_funded_amount,
        SUM(total_payment) AS total_received_amount,
        ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
        DENSE_RANK() OVER (ORDER BY SUM(loan_amount) DESC) AS ranking
    FROM loan_data
    GROUP BY purpose
)
SELECT 
    ranking,
    purpose,
    total_loans,
    total_funded_amount,
    total_received_amount,
    avg_int_rate_pct,
    ROUND(total_funded_amount * 100.0 / (SELECT SUM(loan_amount) FROM loan_data), 2) AS pct_of_portfolio_funded
FROM ranked_purposes
WHERE ranking <= 5
ORDER BY ranking ASC;


-- --------------------------------------------------------
-- 6. TOP 5 LOAN GRADES BY FUNDED AMOUNT
-- Portfolio allocation across credit tiers
-- --------------------------------------------------------
SELECT 
    grade,
    COUNT(id) AS total_loans,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(SUM(loan_amount) * 100.0 / (SELECT SUM(loan_amount) FROM loan_data), 2) AS pct_of_portfolio_funded,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount
FROM loan_data
GROUP BY grade
ORDER BY total_funded_amount DESC
LIMIT 5;


-- --------------------------------------------------------
-- 7. LOAN AMOUNT RANGE DISTRIBUTION
-- Categorizes loan sizes into standardized financial brackets
-- --------------------------------------------------------
SELECT 
    CASE 
        WHEN loan_amount < 5000 THEN '1. Under $5,000'
        WHEN loan_amount BETWEEN 5000 AND 9999.99 THEN '2. $5,000 - $9,999'
        WHEN loan_amount BETWEEN 10000 AND 14999.99 THEN '3. $10,000 - $14,999'
        WHEN loan_amount BETWEEN 15000 AND 19999.99 THEN '4. $15,000 - $19,999'
        WHEN loan_amount BETWEEN 20000 AND 24999.99 THEN '5. $20,000 - $24,999'
        ELSE '6. $25,000 and Above'
    END AS loan_amount_bracket,
    COUNT(id) AS total_loans,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_loans,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY loan_amount_bracket
ORDER BY loan_amount_bracket ASC;


-- --------------------------------------------------------
-- 8. INTEREST RATE RANGE DISTRIBUTION
-- Pricing tiers across portfolio
-- --------------------------------------------------------
SELECT 
    CASE 
        WHEN int_rate < 0.08 THEN '1. Below 8.0%'
        WHEN int_rate BETWEEN 0.08 AND 0.1199 THEN '2. 8.0% - 11.99%'
        WHEN int_rate BETWEEN 0.12 AND 0.1599 THEN '3. 12.0% - 15.99%'
        WHEN int_rate BETWEEN 0.16 AND 0.1999 THEN '4. 16.0% - 19.99%'
        ELSE '5. 20.0% and Above'
    END AS interest_rate_tier,
    COUNT(id) AS total_loans,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_loans,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY interest_rate_tier
ORDER BY interest_rate_tier ASC;


-- --------------------------------------------------------
-- 9. AVERAGE INTEREST RATE AND AVERAGE LOAN AMOUNT BY GRADE
-- Relationship between assigned risk grade, pricing, and sizing
-- --------------------------------------------------------
SELECT 
    grade,
    COUNT(id) AS total_loans,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_interest_rate_pct,
    ROUND(MIN(int_rate) * 100, 2) AS min_int_rate_pct,
    ROUND(MAX(int_rate) * 100, 2) AS max_int_rate_pct,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY grade
ORDER BY grade ASC;


-- --------------------------------------------------------
-- 10. TOP 10 STATES BY TOTAL LOAN AMOUNT
-- Geographic capital concentration across US states
-- --------------------------------------------------------
SELECT 
    address_state AS state_code,
    COUNT(id) AS total_applications,
    SUM(loan_amount) AS total_funded_amount,
    ROUND(SUM(loan_amount) * 100.0 / (SELECT SUM(loan_amount) FROM loan_data), 2) AS pct_of_portfolio_funded,
    ROUND(AVG(loan_amount), 2) AS avg_loan_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct
FROM loan_data
GROUP BY address_state
ORDER BY total_funded_amount DESC
LIMIT 10;

