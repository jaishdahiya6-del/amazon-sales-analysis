# =============================================================
# FILE: src/data_cleaning.py
# PURPOSE: Load, inspect, and clean the Amazon Sales dataset
# =============================================================

# ---- WHY WE IMPORT THESE ----
# pandas  → loads CSV and lets us work with it like a table
# numpy   → helps with number operations and handling missing values
# os      → lets us build file paths that work on any computer

import pandas as pd
import numpy as np
import os

# =============================================================
# SECTION 1: LOAD THE DATA
# =============================================================

def load_data():
    """
    This function loads the raw CSV file into a pandas DataFrame.
    A DataFrame is like an Excel spreadsheet inside Python.
    """

    # Build the file path — works on any Windows machine
    # os.path.dirname(__file__) = folder where THIS script lives (src/)
    # We go up one level (..) to reach the project root, then into data/raw/
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.join(base_dir, "data", "raw", "amazon_sales.csv")

    print(f"📂 Loading data from: {file_path}")

    # Read the CSV file
    # encoding='latin1' handles special characters common in Amazon datasets
    df = pd.read_csv(file_path, encoding='latin1')

    print(f"✅ Data loaded successfully!")
    print(f"📊 Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

    return df


# =============================================================
# SECTION 2: INSPECT THE DATA
# =============================================================

def inspect_data(df):
    """
    This function gives us a full picture of the dataset
    before we touch anything. Always inspect before cleaning!
    """

    print("\n" + "="*60)
    print("📋 STEP 1: FIRST 5 ROWS (What does our data look like?)")
    print("="*60)
    print(df.head())

    print("\n" + "="*60)
    print("📐 STEP 2: SHAPE (How big is our dataset?)")
    print("="*60)
    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")

    print("\n" + "="*60)
    print("🏷️  STEP 3: COLUMN NAMES & DATA TYPES")
    print("="*60)
    print(df.dtypes)

    print("\n" + "="*60)
    print("❓ STEP 4: MISSING VALUES (How many nulls per column?)")
    print("="*60)
    missing = df.isnull().sum()
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    missing_df = pd.DataFrame({
        'Missing Count': missing,
        'Missing %': missing_pct
    })
    # Only show columns that actually have missing values
    print(missing_df[missing_df['Missing Count'] > 0])

    print("\n" + "="*60)
    print("🔢 STEP 5: BASIC STATISTICS (For numeric columns)")
    print("="*60)
    print(df.describe())

    print("\n" + "="*60)
    print("🔁 STEP 6: DUPLICATE ROWS")
    print("="*60)
    duplicates = df.duplicated().sum()
    print(f"Total duplicate rows: {duplicates:,}")

    print("\n" + "="*60)
    print("📦 STEP 7: UNIQUE VALUES IN KEY COLUMNS")
    print("="*60)
    # These are the columns from YOUR dataset
    key_cols = ['Category', 'Size', 'Courier Status', 'Sales Channel']
    for col in key_cols:
        if col in df.columns:
            print(f"\n{col} ({df[col].nunique()} unique values):")
            print(df[col].value_counts().head(10))

    return df


# =============================================================
# SECTION 3: CLEAN THE DATA
# =============================================================

def clean_data(df):
    """
    Clean the dataset step by step.
    We fix: column names, missing values, duplicates, data types.
    """

    print("\n" + "="*60)
    print("🧹 STARTING DATA CLEANING...")
    print("="*60)

    # ---- STEP 1: Standardize Column Names ----
    # Remove spaces, make lowercase, replace spaces with underscores
    # Example: "Order ID" → "order_id"
    # Why? Easier to type and avoids bugs with spaces in names
    print("\n📝 Step 1: Cleaning column names...")
    df.columns = (df.columns
                  .str.strip()           # remove leading/trailing spaces
                  .str.lower()           # convert to lowercase
                  .str.replace(' ', '_') # spaces → underscores
                  .str.replace('-', '_') # hyphens → underscores
                  )
    print(f"✅ Columns renamed: {list(df.columns)}")

    # ---- STEP 2: Remove Duplicate Rows ----
    # Why? Duplicate orders inflate revenue and distort analysis
    print("\n🔁 Step 2: Removing duplicates...")
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"✅ Removed {before - after:,} duplicate rows")
    print(f"   Remaining rows: {after:,}")

    # ---- STEP 3: Handle Missing Values ----
    print("\n❓ Step 3: Handling missing values...")

    # For text/category columns → fill with 'Unknown'
    text_cols = df.select_dtypes(include=['object']).columns
    for col in text_cols:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            df[col] = df[col].fillna('Unknown')
            print(f"   ✅ '{col}': filled {missing_count:,} nulls with 'Unknown'")

    # For numeric columns → fill with median (more robust than mean)
    num_cols = df.select_dtypes(include=['number']).columns
    for col in num_cols:
        missing_count = df[col].isnull().sum()
        if missing_count > 0:
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)
            print(f"   ✅ '{col}': filled {missing_count:,} nulls with median ({median_val})")

    # ---- STEP 4: Fix Date Column ----
    # Why? Dates stored as text can't be used for time-series analysis
    print("\n📅 Step 4: Converting date columns...")
    date_cols = [col for col in df.columns if 'date' in col.lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
        print(f"   ✅ '{col}' converted to datetime")

    # Extract useful time features from date
    if date_cols:
        main_date_col = date_cols[0]
        df['month'] = df[main_date_col].dt.month
        df['month_name'] = df[main_date_col].dt.strftime('%B')
        df['year'] = df[main_date_col].dt.year
        df['day_of_week'] = df[main_date_col].dt.day_name()
        df['quarter'] = df[main_date_col].dt.quarter
        print(f"   ✅ Extracted: month, month_name, year, day_of_week, quarter")

    # ---- STEP 5: Clean Amount/Price Column ----
    print("\n💰 Step 5: Cleaning numeric amount columns...")
    amount_cols = [col for col in df.columns if any(
        x in col.lower() for x in ['amount', 'price', 'revenue', 'sales']
    )]
    for col in amount_cols:
        if df[col].dtype == 'object':
            # Remove currency symbols and commas: "₹1,234.56" → 1234.56
            df[col] = (df[col]
                      .str.replace('₹', '', regex=False)
                      .str.replace(',', '', regex=False)
                      .str.strip()
                      )
            df[col] = pd.to_numeric(df[col], errors='coerce')
            print(f"   ✅ '{col}' cleaned and converted to numeric")

    # ---- STEP 6: Strip Whitespace from Text Columns ----
    print("\n✂️  Step 6: Stripping whitespace from text columns...")
    for col in df.select_dtypes(include='object').columns:
        df[col] = df[col].str.strip()
    print("   ✅ Whitespace removed from all text columns")

    print("\n" + "="*60)
    print("✅ DATA CLEANING COMPLETE!")
    print(f"   Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")
    print("="*60)

    return df


# =============================================================
# SECTION 4: SAVE CLEANED DATA
# =============================================================

def save_cleaned_data(df):
    """
    Save the cleaned DataFrame to data/processed/ folder.
    We NEVER overwrite the original raw file.
    """

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, "data", "processed", "amazon_sales_cleaned.csv")

    df.to_csv(output_path, index=False)
    print(f"\n💾 Cleaned data saved to: {output_path}")
    print(f"   Rows: {df.shape[0]:,} | Columns: {df.shape[1]}")


# =============================================================
# SECTION 5: RUN EVERYTHING
# =============================================================

if __name__ == "__main__":
    # This block runs when you execute this file directly
    # Step 1: Load
    df = load_data()

    # Step 2: Inspect (understand before cleaning)
    df = inspect_data(df)

    # Step 3: Clean
    df_clean = clean_data(df)

    # Step 4: Save
    save_cleaned_data(df_clean)

    print("\n🎉 All done! Your cleaned data is ready for EDA.")