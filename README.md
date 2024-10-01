# Data Cleaning and Merging Assignment

## Overview

This project involves cleaning, normalizing, and merging three datasets (Facebook, Google, and Website) using Python and Pandas. Below is a step-by-step breakdown of the process.

## Steps

### 1. Facebook CSV
- Imported the dataset and checked its structure (rows, columns, uniqueness percentages).
- **Null values check:**
  - `domain`: 0% null
  - `address`: 20% null
  - `categories`: 23% null
  - `description`: 61% null
  - `name`: 0% null
  - `phone`: 37% null
- Focused on columns: `name`, `address`, `categories`, `phone`, `domain`.
- Removed rows where `address`, `categories`, and `phone` were all null, reducing the dataset from 71,167 to 68,729 rows.
- **Uniqueness check after cleaning:**
  - `domain`: 100%, `name`: 99.8%, `phone`: 64%, `address`: 82%, `categories`: 14%.
- **Cleaning operations:**
  - Removed extra spaces and converted text to lowercase.
  - For `name`, removed special characters, digits, and company suffixes (e.g., inc, co).
  - For `address`, kept only letters and digits.
  - Converted `phone` to string, kept numbers, and formatted it to the pattern `+xx xxx-xxx-xxx` with a minimum of 10 digits.
- Filled NaN values with empty spaces and updated uniqueness percentages.

### 2. Google CSV
- Imported the dataset and checked null values:
  - `address`: 37%, `name`: 0.04%, `category`: 74%, `phone`: 47%.
- Removed rows with null values in `address`, `category`, and `phone`, leaving 344,372 rows from 346,925.
- Applied the same cleaning and normalization functions as in the Facebook dataset.
- Kept key columns like `domain`, `category`, `name`, `phone`, etc.
- Grouped by `domain`, showing 99% uniqueness for non-empty values.

### 3. Combining Facebook and Google CSVs
- Merged both datasets using a custom column merging function with fuzzy matching (FuzzyWuzzy).
- Checked for discrepancies between `domain_x` and `domain_y` and filtered rows where `company_name` was not empty, leaving 44,909 rows.
- Merged columns and removed duplicates, reducing the dataset to 41,899 rows.

### 4. Website CSV
- Imported the dataset with `;` as a delimiter and started with 72,018 rows.
- Applied cleaning functions to `name` and `phone` columns.
- Displayed relevant columns like `root_domain`, `site_name`, `main_country`, `main_region`, `main_city`, and `phone`.
- Filled NaN values, converted all text to lowercase, and trimmed extra spaces.
- Removed 3,417 rows where `company_name` was empty, ensuring no remaining duplicates.

### 5. Final Merge (df1 + df2 + df3)
- Merged all three datasets, resulting in 25,608 rows and 12 columns.
- Concatenated columns for `company_name`, `category`, `address`, and `phone` to consolidate information.
- **Final statistics:**
  - `company_name`: 99% unique, `phone`: 98%.
  - Most companies are based in Canada, primarily in Calgary.
- Grouped by `company_name` and handled duplicates, reducing to 25,299 rows.
- Combined unique values across columns, using fuzzy matching for phone numbers where necessary.

## Final Goal
The objective was to consolidate company information across multiple datasets, showing all associated addresses and phone numbers for each company, even if they had multiple branches. The final dataset contains approximately 25,000 unique companies with addresses and phone numbers combined in a readable format.

