import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def clean_and_generate_transactions():
    print("Beginning data cleaning and transactional simulation...")

    # 1. Load raw dataset
    raw_path = "data/raw/amazon_sales.csv"
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found at {raw_path}")

    df = pd.read_csv(raw_path)
    print(f"Loaded raw dataset with {len(df)} rows.")

    # 2. Clean Product Category
    # Extract the main category (first part of the category string)
    def extract_main_category(cat_str):
        if not isinstance(cat_str, str):
            return "Other"
        parts = cat_str.split("|")
        main_cat = parts[0].strip()
        # Clean up some category names to look more professional
        mapping = {
            "Computers&Accessories": "Computers & Accessories",
            "Home&Kitchen": "Home & Kitchen",
            "OfficeProducts": "Office Products",
            "MusicalInstruments": "Musical Instruments",
            "HomeImprovement": "Home Improvement",
            "Toys&Games": "Toys & Games",
            "Car&Motorbike": "Car & Motorbike",
            "Health&PersonalCare": "Health & Personal Care"
        }
        return mapping.get(main_cat, main_cat)

    df["clean_category"] = df["category"].apply(extract_main_category)

    # 3. Clean Prices
    # Clean 'discounted_price' and 'actual_price' columns
    def clean_price(price_str):
        if not isinstance(price_str, str):
            return 0.0
        # Remove ₹, commas, and other non-numeric symbols
        cleaned = price_str.replace("₹", "").replace(",", "").strip()
        try:
            return float(cleaned)
        except ValueError:
            return 0.0

    df["clean_price"] = df["discounted_price"].apply(clean_price)

    # Filter out entries with invalid prices or very low price
    valid_products = df[df["clean_price"] > 0].copy()
    if len(valid_products) == 0:
        valid_products = df.copy()
        valid_products["clean_price"] = 500.0  # Fallback

    print(f"Number of products with valid prices: {len(valid_products)}")

    # 4. Generate Transactions
    # We want to generate ~5000 realistic transaction records over the period Jan 1, 2022 to Dec 31, 2024
    np.random.seed(42)  # For reproducibility
    num_transactions = 5000

    # Sample products
    sampled_indices = np.random.choice(valid_products.index, size=num_transactions, replace=True)
    products_sampled = valid_products.loc[sampled_indices].reset_index(drop=True)

    # Generate dates from 2022-01-01 to 2024-12-31
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2024, 12, 31)
    days_between = (end_date - start_date).days

    random_days = np.random.randint(0, days_between + 1, size=num_transactions)
    order_dates = [start_date + timedelta(days=int(d)) for d in random_days]

    # Introduce seasonality: boost sales in Q4 (holiday season) and certain months
    # E.g., Nov and Dec have a higher probability of sales
    # Let's adjust order dates to represent more realistic seasonality
    adjusted_dates = []
    for d in order_dates:
        # 15% chance to shift to Oct/Nov/Dec if not already there, creating seasonality
        if d.month not in [10, 11, 12] and np.random.rand() < 0.20:
            holiday_month = np.random.choice([10, 11, 12])
            holiday_day = np.random.randint(1, 28)
            d = d.replace(month=holiday_month, day=holiday_day)
        adjusted_dates.append(d)

    # Quantities (1 to 5 units, with higher probability for 1 and 2)
    quantities = np.random.choice([1, 2, 3, 4, 5], size=num_transactions, p=[0.5, 0.3, 0.12, 0.05, 0.03])

    # Regions and States (US-focused or Global/India, let's use US for clean global sales visualization)
    regions = ["Northeast", "Midwest", "South", "West", "Central"]
    region_states = {
        "Northeast": ["New York", "Massachusetts", "Pennsylvania", "New Jersey"],
        "Midwest": ["Illinois", "Ohio", "Michigan", "Wisconsin"],
        "South": ["Texas", "Florida", "Georgia", "North Carolina"],
        "West": ["California", "Washington", "Oregon", "Arizona"],
        "Central": ["Colorado", "Kansas", "Nebraska", "Utah"]
    }

    transaction_regions = np.random.choice(regions, size=num_transactions, p=[0.20, 0.18, 0.28, 0.24, 0.10])
    transaction_states = []
    for r in transaction_regions:
        states = region_states[r]
        transaction_states.append(np.random.choice(states))

    # Customer segments
    segments = ["Consumer", "Corporate", "Home Office"]
    transaction_segments = np.random.choice(segments, size=num_transactions, p=[0.55, 0.30, 0.15])

    # Construct transactional dataframe
    transactions_df = pd.DataFrame({
        "Order_Date": adjusted_dates,
        "Product_ID": products_sampled["product_id"],
        "Product_Name": products_sampled["product_name"],
        "Category": products_sampled["clean_category"],
        "Price": products_sampled["clean_price"],
        "Quantity": quantities,
        "Region": transaction_regions,
        "State": transaction_states,
        "Segment": transaction_segments
    })

    # Calculate Revenue (Price * Quantity)
    transactions_df["Revenue"] = transactions_df["Price"] * transactions_df["Quantity"]

    # Add a Profit Margin and Profit column for richer analysis (e.g. margin between 10% and 40%)
    # Let's assign margin based on category to make it consistent and realistic
    category_margins = {
        "Electronics": 0.15,
        "Computers & Accessories": 0.12,
        "Home & Kitchen": 0.25,
        "Office Products": 0.30,
        "Musical Instruments": 0.20,
        "Home Improvement": 0.22,
        "Toys & Games": 0.28,
        "Car & Motorbike": 0.18,
        "Health & Personal Care": 0.35,
        "Other": 0.20
    }

    margins = transactions_df["Category"].map(category_margins).fillna(0.20)
    # Add some random noise to margins (-5% to +5%)
    noise = np.random.uniform(-0.05, 0.05, size=num_transactions)
    final_margins = (margins + noise).clip(0.05, 0.50)

    transactions_df["Profit_Margin"] = final_margins * 100
    transactions_df["Profit"] = transactions_df["Revenue"] * final_margins

    # Sort by Order Date
    transactions_df = transactions_df.sort_values(by="Order_Date").reset_index(drop=True)

    # 5. Save the output
    processed_dir = "data/processed"
    os.makedirs(processed_dir, exist_ok=True)

    output_file = os.path.join(processed_dir, "amazon_sales_transactions.csv")
    transactions_df.to_csv(output_file, index=False)

    print(f"Successfully generated {len(transactions_df)} transactions.")
    print(f"Data saved to {output_file}")

    # Let's save a copy of product_performance too if needed
    return transactions_df

if __name__ == "__main__":
    clean_and_generate_transactions()
