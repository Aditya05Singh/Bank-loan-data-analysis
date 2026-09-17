-- ========================================================
-- SCRIPT: 01_database_setup.sql
-- PROJECT: Bank Loan Lending Data Analytics
-- PURPOSE: Create and configure MySQL database bank_loan_analytics
-- RDBMS: MySQL 8.0+
-- ========================================================

-- 1. Create database with UTF-8 character encoding
CREATE DATABASE IF NOT EXISTS bank_loan_analytics
    DEFAULT CHARACTER SET utf8mb4
    DEFAULT COLLATE utf8mb4_unicode_ci;

-- 2. Switch to the target database
USE bank_loan_analytics;

-- 3. Configure optimal session parameters
-- Enforce strict SQL mode for data integrity
SET SESSION sql_mode = 'STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Enable local infile loading if needed for bulk data import
SET GLOBAL local_infile = 1;

-- 4. User and privilege setup (sample configuration for development)
-- Uncomment and adjust passwords if setting up a dedicated analytics user:
/*
CREATE USER IF NOT EXISTS 'loan_analyst'@'localhost' IDENTIFIED BY 'SecureLoan#2026';
GRANT SELECT, INSERT, UPDATE, CREATE, DROP, ALTER, CREATE VIEW, SHOW VIEW 
    ON bank_loan_analytics.* TO 'loan_analyst'@'localhost';
FLUSH PRIVILEGES;
*/

SELECT 'Database bank_loan_analytics created and configured successfully.' AS status_message;

