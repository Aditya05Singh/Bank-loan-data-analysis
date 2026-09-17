-- ========================================================
-- SCRIPT: 02_schema.sql
-- PROJECT: Bank Loan Lending Data Analytics
-- PURPOSE: Define table schema, constraints, indexes, and import scripts
-- RDBMS: MySQL 8.0+
-- ========================================================

USE bank_loan_analytics;

-- Drop table if recreating
DROP TABLE IF EXISTS loan_data;

-- 1. Main Table Definition
CREATE TABLE loan_data (
    id                      INT NOT NULL COMMENT 'Unique identifier for the loan application (Primary Key)',
    address_state           VARCHAR(2) NOT NULL COMMENT 'Two-letter US state code of applicant residence',
    application_type        VARCHAR(50) NOT NULL COMMENT 'Type of application (e.g. INDIVIDUAL)',
    emp_length              VARCHAR(20) NOT NULL COMMENT 'Employment length in years (e.g. 10+ years, < 1 year)',
    emp_title               VARCHAR(255) DEFAULT 'Unspecified' COMMENT 'Job title or employer provided by borrower',
    grade                   VARCHAR(2) NOT NULL COMMENT 'Lender credit grade assigned to loan (A through G)',
    home_ownership          VARCHAR(20) NOT NULL COMMENT 'Home ownership status (RENT, MORTGAGE, OWN, OTHER, NONE)',
    issue_date              DATE NOT NULL COMMENT 'Date the loan was originated/funded',
    last_credit_pull_date   DATE NULL COMMENT 'Date of most recent credit report pull',
    last_payment_date       DATE NULL COMMENT 'Date of most recent payment received',
    loan_status             VARCHAR(50) NOT NULL COMMENT 'Current status (Fully Paid, Charged Off, Current)',
    next_payment_date       DATE NULL COMMENT 'Scheduled date for next upcoming installment payment',
    member_id               INT NOT NULL COMMENT 'Unique borrower member identifier',
    purpose                 VARCHAR(50) NOT NULL COMMENT 'Borrower stated category/purpose for the loan',
    sub_grade               VARCHAR(5) NOT NULL COMMENT 'Detailed risk sub-grade (e.g. A1 through G5)',
    term                    VARCHAR(20) NOT NULL COMMENT 'Repayment term in months (36 months, 60 months)',
    verification_status     VARCHAR(50) NOT NULL COMMENT 'Income verification status (Verified, Source Verified, Not Verified)',
    annual_income           DECIMAL(12, 2) NOT NULL COMMENT 'Self-reported annual income in USD',
    dti                     DECIMAL(6, 4) NOT NULL COMMENT 'Debt-to-income ratio expressed as decimal (0.0000 - 1.0000)',
    installment             DECIMAL(10, 2) NOT NULL COMMENT 'Monthly payment owed by the borrower in USD',
    int_rate                DECIMAL(6, 4) NOT NULL COMMENT 'Annual interest rate expressed as decimal (e.g. 0.1205 = 12.05%)',
    loan_amount             DECIMAL(12, 2) NOT NULL COMMENT 'Principal loan amount funded in USD',
    total_acc               INT NOT NULL COMMENT 'Total credit accounts on applicant credit profile',
    total_payment           DECIMAL(12, 2) NOT NULL COMMENT 'Total cash received to date from borrower payments in USD',
    
    -- Primary Key Constraint
    CONSTRAINT pk_loan_data PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 2. Indexes for Query Performance and Filtering
-- Index on loan status for fast KPI filtering (Good vs Bad loans)
CREATE INDEX idx_loan_status ON loan_data (loan_status);

-- Composite index on grade and sub-grade for credit risk tier analysis
CREATE INDEX idx_grade_subgrade ON loan_data (grade, sub_grade);

-- Index on issue date for chronological and time-series aggregation
CREATE INDEX idx_issue_date ON loan_data (issue_date);

-- Index on loan purpose for portfolio allocation queries
CREATE INDEX idx_purpose ON loan_data (purpose);

-- Index on state for geographic regional reporting
CREATE INDEX idx_address_state ON loan_data (address_state);

-- Index on home ownership for customer demographic queries
CREATE INDEX idx_home_ownership ON loan_data (home_ownership);

-- Index on verification status for underwriting audits
CREATE INDEX idx_verification_status ON loan_data (verification_status);

-- Index on member ID for borrower-level joins and lookups
CREATE INDEX idx_member_id ON loan_data (member_id);

-- ========================================================
-- DATA IMPORT INSTRUCTIONS
-- ========================================================

/*
METHOD 1: LOAD DATA LOCAL INFILE (Fastest & Reproducible)
--------------------------------------------------------
Execute the following query from MySQL client or terminal.
Make sure local_infile is enabled on both client and server:

mysql --local-infile=1 -u root -p bank_loan_analytics

LOAD DATA LOCAL INFILE '/path/to/BANK_LOAN_LENDING_DATA_ANALYTICS/data/cleaned/loan_data_cleaned.csv'
INTO TABLE loan_data
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
    id,
    address_state,
    application_type,
    emp_length,
    emp_title,
    grade,
    home_ownership,
    issue_date,
    last_credit_pull_date,
    last_payment_date,
    loan_status,
    next_payment_date,
    member_id,
    purpose,
    sub_grade,
    term,
    verification_status,
    annual_income,
    dti,
    installment,
    int_rate,
    loan_amount,
    total_acc,
    total_payment
);

METHOD 2: MySQL Workbench Table Data Import Wizard
--------------------------------------------------
1. Open MySQL Workbench and connect to your MySQL instance.
2. In the Schemas tab, expand `bank_loan_analytics` -> `Tables`.
3. Right-click `loan_data` and choose "Table Data Import Wizard".
4. Browse to `data/cleaned/loan_data_cleaned.csv` and click "Next".
5. Select "Use existing table: loan_data".
6. Verify the field mappings correspond 1:1 with table columns.
7. Click "Next" to execute the import of all 38,576 records.

METHOD 3: Python Automated Loader (Using SQLAlchemy)
----------------------------------------------------
Run the provided python loader script if preferred:
python scripts/load_to_mysql.py
*/

