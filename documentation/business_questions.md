# 25+ Core Business Questions Answered by the Project

This document outlines 26 essential commercial banking business questions addressed by the SQL analytical queries and Tableau dashboards.

---

### Category A: Executive Portfolio Health & Capital Allocation
1. **What is the total volume and capital commitment of our originated loan portfolio?**
   - *Answered by*: `04_kpi_analysis.sql` / Dashboard 1, Area 1 & 2.
   - *Finding*: 38,576 approved loan applications totaling $435,757,075 ($435.8M) in funded principal.

2. **How much cumulative cash has been collected, and what is our portfolio collection ratio?**
   - *Answered by*: `04_kpi_analysis.sql` / Dashboard 1, Area 3.
   - *Finding*: $473,070,933 ($473.1M) collected, representing 108.56% of total principal disbursed.

3. **What is the overall portfolio default rate, and what portion of loans are performing?**
   - *Answered by*: `04_kpi_analysis.sql` / Dashboard 1, Area 6 & 7.
   - *Finding*: 13.82% default rate (5,333 Charged Off loans); 86.18% Good Loans (32,145 Fully Paid, 1,098 Current).

4. **What is the average ticket size and interest rate charged across all borrowers?**
   - *Answered by*: `04_kpi_analysis.sql` / Dashboard 1, Area 4 & 5.
   - *Finding*: Average loan size of $11,296.07; portfolio weighted average interest rate of 12.05%.

5. **What was the Month-over-Month (MoM) growth in originations between November and December 2021?**
   - *Answered by*: `04_kpi_analysis.sql` & `08_time_series_analysis.sql` / Dashboard 1, KPI Subtitles.
   - *Finding*: Applications grew +6.91% (4,035 to 4,314); funded capital grew +13.04% ($47.8M to $54.0M).

---

### Category B: Product Structure & Category Segmentation
6. **Which borrowing purpose accounts for the largest share of our balance sheet capital?**
   - *Answered by*: `05_portfolio_analysis.sql` / Dashboard 1, Area 12.
   - *Finding*: Debt Consolidation accounts for over 53% of all funded capital ($233.9M across 18,214 loans).

7. **How is our portfolio distributed between 36-month and 60-month loan terms?**
   - *Answered by*: `06_customer_analysis.sql` / Dashboard 2, Area 6.
   - *Finding*: Nearly three-quarters (73.2%, 28,237 loans) are 36-month contracts; 26.8% (10,339 loans) are 60-month contracts.

8. **Do 60-month loans carry higher credit risk than 36-month loans?**
   - *Answered by*: `06_customer_analysis.sql` / Dashboard 2, Area 6 Tooltip.
   - *Finding*: 60-month loans exhibit an observed default rate of ~22.6%, compared to ~10.6% for 36-month loans.

9. **What is the ticket-size distribution across our loan portfolio?**
   - *Answered by*: `05_portfolio_analysis.sql` / Dashboard 1, Area 14.
   - *Finding*: The $5,000–$9,999 and $10,000–$14,999 brackets comprise the majority of loan originations.

10. **Which loan purposes carry the highest average interest rate pricing?**
    - *Answered by*: `06_customer_analysis.sql` / Dashboard 2, Area 7.
    - *Finding*: Renewable Energy (13.5%), Small Business (13.2%), and House loans (13.1%).

---

### Category C: Borrower Demographics & Underwriting Capacity
11. **How does homeownership status impact loan application volume?**
    - *Answered by*: `06_customer_analysis.sql` / Dashboard 2, Area 1.
    - *Finding*: Renters represent 47.8% (18,447 loans) and Mortgage holders represent 44.6% (17,198 loans). Homeowners with no mortgage represent 7.4% (2,838 loans).

12. **Does homeowner status correlate with lower default rates?**
    - *Answered by*: `07_risk_analysis.sql` / Dashboard 3, Area 7.
    - *Finding*: Mortgage holders have the lowest observed default rate (12.98%), compared to 14.61% for renters.

13. **Which employment tenure bracket represents our primary customer base?**
    - *Answered by*: `06_customer_analysis.sql` / Dashboard 2, Area 2.
    - *Finding*: Borrowers with 10+ years of employment form the largest single group (8,879 loans, 23.0% of total).

14. **What percentage of our portfolio underwent rigorous income verification?**
    - *Answered by*: `06_customer_analysis.sql` / Dashboard 2, Area 3.
    - *Finding*: 35.8% were fully Verified, 27.8% Source Verified, and 36.4% Not Verified.

15. **How does average loan amount scale with borrower annual income?**
    - *Answered by*: `06_customer_analysis.sql` / Dashboard 2, Area 4 & 5.
    - *Finding*: Average loan size scales from $6,500 for incomes under $30,000 to over $15,800 for incomes over $120,000.

16. **How does borrower Debt-to-Income (DTI) ratio correlate with annual earnings?**
    - *Answered by*: `06_customer_analysis.sql` / Dashboard 2, Area 8.
    - *Finding*: Average DTI decreases moderately as income rises (13.8% for <$30k vs 11.9% for >$120k).

---

### Category D: Geographic Concentration & Regional Exposure
17. **Which US states represent our largest geographic credit exposures?**
    - *Answered by*: `05_portfolio_analysis.sql` / Dashboard 1, Area 11 & Dashboard 2, Area 11.
    - *Finding*: California is #1 ($64.4M funded, 6,894 loans), followed by New York ($41.4M), Texas ($37.8M), and Florida ($34.5M).

18. **Do top borrowing states show significant divergence in default rates?**
    - *Answered by*: `05_portfolio_analysis.sql` & `vw_state_analysis` / Dashboard 1, Area 11.
    - *Finding*: California has an observed default rate of ~14.9%, Florida ~15.8%, while New York is lower at ~13.4%.

---

### Category E: Credit Risk, Pricing & Sensitivity
19. **How well does our credit grading system (Grades A through G) differentiate default risk?**
    - *Answered by*: `07_risk_analysis.sql` / Dashboard 3, Area 1.
    - *Finding*: Default rates scale monotonically: Grade A = 5.98%, Grade B = 12.21%, Grade C = 17.15%, Grade D = 21.08%, Grade E = 26.85%, Grade F = 32.68%, Grade G = 33.78%.

20. **Is the interest rate spread sufficient to compensate for subprime default losses?**
    - *Answered by*: `05_portfolio_analysis.sql` & `07_risk_analysis.sql` / Dashboard 3, Area 1 & 4.
    - *Finding*: Grade G yields an average interest rate of 20.91% but incurs a 33.78% default rate, indicating negative risk-adjusted margin in the lowest tier.

21. **Which borrowing purpose has the highest observed default rate?**
    - *Answered by*: `07_risk_analysis.sql` / Dashboard 3, Area 2.
    - *Finding*: Small Business loans exhibit the highest observed default rate (27.08%), followed by Renewable Energy (18.6%).

22. **What is the observed default rate for high debt-burden borrowers (DTI >= 20%)?**
    - *Answered by*: `07_risk_analysis.sql` / Dashboard 3, Area 3.
    - *Finding*: Borrowers with DTI >= 20% exhibit an observed default rate of 16.4%, compared to 12.2% for borrowers with DTI < 10%.

23. **What is the default rate among lower-income borrowers (< $30,000)?**
    - *Answered by*: `07_risk_analysis.sql` / Dashboard 3, Area 9.
    - *Finding*: 18.25% default rate, compared to 10.42% for borrowers earning $120,000+.

---

### Category F: Loss Given Default & Recoveries
24. **What is the total gross capital written off to date on defaulted loans?**
    - *Answered by*: `04_kpi_analysis.sql` & `07_risk_analysis.sql` / Dashboard 3, Area 5.
    - *Finding*: $65,532,225 in gross funded principal was disbursed to Charged Off loans.

25. **How much cash was successfully recovered on defaulted loans, and what is the recovery rate?**
    - *Answered by*: `04_kpi_analysis.sql` & `07_risk_analysis.sql` / Dashboard 3, Area 6.
    - *Finding*: $37,284,763 was collected on defaulted loans, representing a 56.89% recovery rate.

26. **What is the bank's net economic credit loss across the entire portfolio?**
    - *Answered by*: `04_kpi_analysis.sql` / Dashboard 1 & 3.
    - *Finding*: Net economic credit loss ($65.53M funded minus $37.28M collected) is $28,247,462.

