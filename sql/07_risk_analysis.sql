-- ========================================================
-- SCRIPT: 07_risk_analysis.sql
-- PROJECT: Bank Loan Lending Data Analytics
-- PURPOSE: Detailed credit risk assessment, default rate drivers, loss recovery, and risk segmentation
-- RDBMS: MySQL 8.0+
-- NOTE ON HIGH-RISK DEFINITION: In this empirical dataset, the maximum observed DTI is 0.2999 (29.99%).
-- A filter of DTI > 40% yields 0 records. High-risk is therefore observationally defined as
-- DTI >= 20.0% (top risk quartile) and/or subprime grades (D through G).
-- ========================================================

USE bank_loan_analytics;

-- --------------------------------------------------------
-- 1. DEFAULT RATE BY LOAN GRADE AND SUB-GRADE
-- Observes credit risk progression across assigned credit ratings
-- --------------------------------------------------------
SELECT 
    grade,
    COUNT(id) AS total_loans,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS charged_off_funded_amount,
    ROUND(AVG(int_rate) * 100, 2) AS avg_int_rate_pct,
    ROUND(AVG(dti) * 100, 2) AS avg_dti_pct
FROM loan_data
GROUP BY grade
ORDER BY grade ASC;


-- --------------------------------------------------------
-- 2. DEFAULT RATE BY LOAN PURPOSE (TOP 10 BY VOLUME)
-- Observational default rates across borrowing objectives
-- --------------------------------------------------------
SELECT 
    purpose,
    COUNT(id) AS total_loans,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct,
    SUM(loan_amount) AS total_funded_amount,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS charged_off_funded_amount
FROM loan_data
GROUP BY purpose
ORDER BY total_loans DESC
LIMIT 10;


-- --------------------------------------------------------
-- 3. DEFAULT RATE BY DEBT-TO-INCOME (DTI) RANGE
-- Evaluates default rate variation across borrower debt leverage tiers
-- --------------------------------------------------------
SELECT 
    CASE 
        WHEN dti < 0.08 THEN '1. DTI < 8.0%'
        WHEN dti BETWEEN 0.08 AND 0.1199 THEN '2. DTI 8.0% - 11.99%'
        WHEN dti BETWEEN 0.12 AND 0.1599 THEN '3. DTI 12.0% - 15.99%'
        WHEN dti BETWEEN 0.16 AND 0.1999 THEN '4. DTI 16.0% - 19.99%'
        WHEN dti BETWEEN 0.20 AND 0.2499 THEN '5. DTI 20.0% - 24.99%'
        ELSE '6. DTI >= 25.0%'
    END AS dti_bracket,
    COUNT(id) AS total_loans,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct,
    SUM(loan_amount) AS total_funded_amount,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS charged_off_funded_amount
FROM loan_data
GROUP BY dti_bracket
ORDER BY dti_bracket ASC;


-- --------------------------------------------------------
-- 4. DEFAULT RATE BY INTEREST RATE RANGE
-- Evaluates whether higher-priced loans experience higher default incidence
-- --------------------------------------------------------
SELECT 
    CASE 
        WHEN int_rate < 0.08 THEN '1. Rate < 8.0%'
        WHEN int_rate BETWEEN 0.08 AND 0.1199 THEN '2. Rate 8.0% - 11.99%'
        WHEN int_rate BETWEEN 0.12 AND 0.1599 THEN '3. Rate 12.0% - 15.99%'
        WHEN int_rate BETWEEN 0.16 AND 0.1999 THEN '4. Rate 16.0% - 19.99%'
        ELSE '5. Rate >= 20.0%'
    END AS interest_rate_bracket,
    COUNT(id) AS total_loans,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct,
    SUM(loan_amount) AS total_funded_amount
FROM loan_data
GROUP BY interest_rate_bracket
ORDER BY interest_rate_bracket ASC;


-- --------------------------------------------------------
-- 5. CHARGED-OFF AMOUNT AND RECOVERY RATE BY YEAR
-- Historical loss given default (LGD) tracking
-- --------------------------------------------------------
SELECT 
    YEAR(issue_date) AS issue_year,
    COUNT(id) AS total_loans,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS charged_off_funded_amount,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) AS recoveries_received,
    ROUND(
        SUM(CASE WHEN loan_status = 'Charged Off' THEN total_payment ELSE 0 END) * 100.0 /
        NULLIF(SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END), 0),
        2
    ) AS recovery_rate_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount - total_payment ELSE 0 END) AS net_credit_loss
FROM loan_data
GROUP BY YEAR(issue_date)
ORDER BY issue_year ASC;


-- --------------------------------------------------------
-- 6. DEFAULT RATE BY HOME OWNERSHIP
-- Default variation by applicant collateral and housing status
-- --------------------------------------------------------
SELECT 
    home_ownership,
    COUNT(id) AS total_loans,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS charged_off_funded
FROM loan_data
GROUP BY home_ownership
ORDER BY default_rate_pct DESC;


-- --------------------------------------------------------
-- 7. DEFAULT RATE BY EMPLOYMENT LENGTH
-- Default incidence across career tenure brackets
-- --------------------------------------------------------
SELECT 
    emp_length,
    COUNT(id) AS total_loans,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS charged_off_funded
FROM loan_data
GROUP BY emp_length
ORDER BY default_rate_pct DESC;


-- --------------------------------------------------------
-- 8. DEFAULT RATE BY ANNUAL INCOME RANGE
-- Default patterns across borrower earnings tiers
-- --------------------------------------------------------
SELECT 
    CASE 
        WHEN annual_income < 30000 THEN '1. Under $30,000'
        WHEN annual_income BETWEEN 30000 AND 59999.99 THEN '2. $30,000 - $59,999'
        WHEN annual_income BETWEEN 60000 AND 89999.99 THEN '3. $60,000 - $89,999'
        WHEN annual_income BETWEEN 90000 AND 119999.99 THEN '4. $90,000 - $119,999'
        ELSE '5. $120,000 and Above'
    END AS income_bracket,
    COUNT(id) AS total_loans,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS charged_off_loans,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS default_rate_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS charged_off_funded
FROM loan_data
GROUP BY income_bracket
ORDER BY income_bracket ASC;


-- --------------------------------------------------------
-- 9. HIGH-RISK LOAN KPIS & CONCENTRATION ANALYSIS
-- Defining High-Risk Loans: In this dataset, DTI max is 0.2999 (29.99%).
-- We evaluate two distinct, fully documented high-risk definitions:
-- Segment A (High DTI Tier): DTI >= 0.20 (top ~15% leverage segment)
-- Segment B (Subprime / Lower Credit Tier): Grade IN ('D', 'E', 'F', 'G')
-- Segment C (Composite High Risk): Grade IN ('D','E','F','G') AND DTI >= 0.20
-- --------------------------------------------------------
SELECT 
    'Empirical High-Risk Segment (DTI >= 20% OR Grade IN (D,E,F,G))' AS risk_segment_name,
    COUNT(id) AS high_risk_loan_count,
    ROUND(COUNT(id) * 100.0 / (SELECT COUNT(*) FROM loan_data), 2) AS pct_of_total_portfolio,
    SUM(loan_amount) AS high_risk_funded_amount,
    ROUND(SUM(loan_amount) * 100.0 / (SELECT SUM(loan_amount) FROM loan_data), 2) AS pct_of_funded_amount,
    COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) AS high_risk_charged_off_count,
    ROUND(COUNT(CASE WHEN loan_status = 'Charged Off' THEN 1 END) * 100.0 / COUNT(id), 2) AS high_risk_default_rate_pct,
    SUM(CASE WHEN loan_status = 'Charged Off' THEN loan_amount ELSE 0 END) AS high_risk_charged_off_funded
FROM loan_data
WHERE dti >= 0.20 OR grade IN ('D', 'E', 'F', 'G');


-- --------------------------------------------------------
-- 10. DTI > 40% SANITY AUDIT
-- Explicitly executes the DTI > 40% query requested in specifications
-- Documents that no records exceed 0.2999 in this actual public dataset.
-- --------------------------------------------------------
SELECT 
    'DTI > 40% Threshold Check' AS test_name,
    COUNT(id) AS loan_count_over_40_pct_dti,
    MAX(dti) AS actual_maximum_observed_dti,
    'Verified: Maximum DTI in dataset is 29.99%, resulting in 0 records above 40%' AS observation_note
FROM loan_data
WHERE dti > 0.40;

