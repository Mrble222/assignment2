# Assignment 2 Report: Data Validation & Testing

## 1. Great Expectations Validation Results

![[Pasted image 20260626233003.png]]

## 2. Data Quality Issues Found

The expectation suite `customer_data_expectations` was run against `customer_data.csv`. All 8 expectations failed, indicating significant data quality issues across the dataset (5015 total rows).

| Column        | Expectation                        | Issue                                        | Failing Rows | % Affected |
| ------------- | ---------------------------------- | -------------------------------------------- | ------------ | ---------- |
| `customer_id` | Unique values                      | Duplicate records                            | 568          | 11.68%     |
| `customer_id` | Not null                           | Missing customer IDs                         | 150          | 2.99%      |
| `age`         | Between 0 and 120                  | Out-of-range ages                            | 384          | 7.89%      |
| `email`       | Valid email format                 | Invalid or malformed emails                  | 346          | 7.56%      |
| `salary`      | Not null (95% threshold)           | Missing salary values                        | 425          | 8.47%      |
| `country`     | One of: USA, Canada, UK, Australia | Invalid country values                       | 301          | 6.05%      |
| `signup_date` | Datetime format (YYYY-MM-DD)       | Dates not in expected format                 | 4823         | 96.44%     |
| Table-level   | Row count between 500 and 1000     | Dataset has 5015 rows, exceeding max of 1000 | –            | N/A        |

**Total rows in dataset:** 5015  
**Overall validation result:** ❌ FAILED

## 3. pytest Execution Results

![[Screenshot 2026-06-26 at 11.27.39 PM.png]]


## 4. Reflection: Most Impactful Data Quality Issue on ML Model Performance

The most impactful data quality issue on ML model performance would be the **missing and inconsistent salary values**, closely followed by the **duplicate customer records**.

Salary is likely a key numerical feature in any customer-related ML model (e.g., churn prediction, credit scoring). With 425 missing values (8.47% of rows), any model trained on this data would either need to drop those rows. This reduces the training set significantly. Or they could impute the values, which introduces bias if not done carefully. Additionally, the assignment notes that salary is stored as a string with dollar signs, meaning it cannot be used numerically until cleaned. A model receiving raw string salary values would either fail entirely or treat salary as a categorical feature, producing meaningless results.

Duplicate customer records (568 duplicates, 11.68%) makes this problem even worse. Duplicates cause data leakage when the same customer appears in both the training and test sets, leading to overly optimistic evaluation metrics that do not reflect real-world performance. Models trained on duplicate-heavy data learn to memorize specific records rather than generalize patterns, which directly undermines the goal of machine learning.

Together, these two issues (dirty salary data and duplicate records) would heavily distort both model training and evaluation, making them the highest priority to address before any model development begins.
