# Tableau Calculated Fields Reference

This document provides the exact syntax for all Tableau calculated fields used across the 3 dashboards.
All formulas maintain 100% mathematical and logical consistency with the underlying MySQL database views in `sql/09_tableau_views.sql`.

---

### 1. Default Flag (`[Default Flag]`)
Identifies whether a loan is classified as a credit default (Charged Off).
```tableau
IF [Loan Status] = 'Charged Off' THEN 1 ELSE 0 END
```

---

### 2. Default Rate (`[Default Rate]`)
Calculates the portfolio or cohort default rate as an aggregate measure.
```tableau
SUM([Default Flag]) / COUNT([Loan Id])
```
*Format: Percentage with 2 decimal places (`0.00%`).*

---

### 3. Fully Paid Flag (`[Fully Paid Flag]`)
Identifies loans where obligations were fully settled.
```tableau
IF [Loan Status] = 'Fully Paid' THEN 1 ELSE 0 END
```

---

### 4. Good Loan Flag (`[Good Loan Flag]`)
Identifies performing loans and fully satisfied loans.
```tableau
IF [Loan Status] = 'Fully Paid' OR [Loan Status] = 'Current' THEN 1 ELSE 0 END
```

---

### 5. Good Loan Rate (`[Good Loan Rate]`)
```tableau
SUM([Good Loan Flag]) / COUNT([Loan Id])
```
*Format: Percentage (`0.00%`).*

---

### 6. Loan Amount Range (`[Loan Amount Range]`)
Segments loan sizes into standardized commercial ticket-size brackets.
```tableau
IF [Loan Amount] < 5000 THEN '1. Under $5,000'
ELSEIF [Loan Amount] <= 9999.99 THEN '2. $5,000 - $9,999'
ELSEIF [Loan Amount] <= 14999.99 THEN '3. $10,000 - $14,999'
ELSEIF [Loan Amount] <= 19999.99 THEN '4. $15,000 - $19,999'
ELSEIF [Loan Amount] <= 24999.99 THEN '5. $20,000 - $24,999'
ELSE '6. $25,000 and Above'
END
```

---

### 7. Income Range (`[Income Range]`)
Segments borrower annual income into analytical capacity tiers.
```tableau
IF [Annual Income] < 30000 THEN '1. Under $30,000'
ELSEIF [Annual Income] <= 59999.99 THEN '2. $30,000 - $59,999'
ELSEIF [Annual Income] <= 89999.99 THEN '3. $60,000 - $89,999'
ELSEIF [Annual Income] <= 119999.99 THEN '4. $90,000 - $119,999'
ELSE '5. $120,000 and Above'
END
```

---

### 8. DTI Range (`[DTI Range]`)
Groups applicant Debt-to-Income leverage ratios into empirical brackets.
*Note: In this dataset, DTI is stored as a decimal (0.00 to 0.2999).*
```tableau
IF [DTI] < 0.10 THEN '1. Under 10.0%'
ELSEIF [DTI] <= 0.1499 THEN '2. 10.0% - 14.99%'
ELSEIF [DTI] <= 0.1999 THEN '3. 15.0% - 19.99%'
ELSEIF [DTI] <= 0.2499 THEN '4. 20.0% - 24.99%'
ELSE '5. 25.0% and Above'
END
```

---

### 9. Interest Rate Range (`[Interest Rate Range]`)
Categorizes commercial loan pricing tiers.
```tableau
IF [Int Rate] < 0.08 THEN '1. Below 8.0%'
ELSEIF [Int Rate] <= 0.1199 THEN '2. 8.0% - 11.99%'
ELSEIF [Int Rate] <= 0.1599 THEN '3. 12.0% - 15.99%'
ELSEIF [Int Rate] <= 0.1999 THEN '4. 16.0% - 19.99%'
ELSE '5. 20.0% and Above'
END
```

---

### 10. Employment Length Group (`[Employment Length Group]`)
Aggregates granular employment tenures into executive career stages.
```tableau
IF [Emp Length] = '< 1 year' OR [Emp Length] = '1 year' OR [Emp Length] = '2 years' THEN 'Junior (0-2 Years)'
ELSEIF [Emp Length] = '3 years' OR [Emp Length] = '4 years' OR [Emp Length] = '5 years' THEN 'Mid-Level (3-5 Years)'
ELSEIF [Emp Length] = '6 years' OR [Emp Length] = '7 years' OR [Emp Length] = '8 years' OR [Emp Length] = '9 years' THEN 'Senior (6-9 Years)'
ELSEIF [Emp Length] = '10+ years' THEN 'Established (10+ Years)'
ELSE 'Unspecified'
END
```

---

### 11. Chronological Date Parts
Used for time-series aggregation and strict chronological sorting.

**Year**:
```tableau
YEAR([Issue Date])
```

**Quarter**:
```tableau
'Q' + STR(QUARTER([Issue Date]))
```

**Month**:
```tableau
MONTH([Issue Date])
```

**Month Name**:
```tableau
DATENAME('month', [Issue Date])
```

**Year-Month**:
```tableau
STR(YEAR([Issue Date])) + '-' + IF MONTH([Issue Date]) < 10 THEN '0' + STR(MONTH([Issue Date])) ELSE STR(MONTH([Issue Date])) END
```

---

### 12. Recovery Rate on Defaults (`[Recovery Rate]`)
Calculates post-default cash collections relative to the principal disbursed on charged-off loans.
```tableau
SUM(IF [Loan Status] = 'Charged Off' THEN [Total Payment] ELSE 0 END) /
NULLIF(SUM(IF [Loan Status] = 'Charged Off' THEN [Loan Amount] ELSE 0 END), 0)
```
*Format: Percentage (`0.00%`). Evaluates to 56.89% across the full portfolio.*

---

### 13. Net Credit Loss (`[Net Credit Loss]`)
Measures unrecovered principal capital on defaulted loans.
```tableau
SUM(IF [Loan Status] = 'Charged Off' THEN [Loan Amount] - [Total Payment] ELSE 0 END)
```
*Format: Currency (`$#,##0`). Evaluates to $28,247,462 across the full portfolio.*

---

### 14. High Risk Flag (`[High Risk Flag]`)
Identifies loans with elevated leverage (`DTI >= 20%`) or subprime credit ratings (`Grade D, E, F, G`).
```tableau
IF [DTI] >= 0.20 OR [Grade] = 'D' OR [Grade] = 'E' OR [Grade] = 'F' OR [Grade] = 'G' THEN 'High Risk'
ELSE 'Standard Risk'
END
```

