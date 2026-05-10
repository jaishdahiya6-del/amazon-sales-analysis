import pandas as pd
import numpy as np

def optimize_sales_data(df):
    """
    Optimizes data types and performs vectorized calculations for Amazon Sales data.
    """
    # 1. Memory Optimization: Convert 'Category' to category type
    if 'Category' in df.columns:
        df['Category'] = df['Category'].astype('category')

    # 2. Vectorized Calculation: Profit Margin
    # Avoiding loops for speed
    df['Profit_Margin'] = (df['Profit'] / df['Sales']) * 100

    # 3. High-Performance Grouping
    # Calculate average shipping time and total sales per category
    category_metrics = df.groupby('Category').agg({
        'Sales': 'sum',
        'Profit': 'mean',
        'Quantity': 'sum'
    }).sort_values(by='Sales', ascending=False)

    print("🚀 Optimization complete. Calculated metrics for", len(category_metrics), "categories.")
    return df, category_metrics

if __name__ == "__main__":
    # Test with a mock setup or your actual amazon_sales.csv
    try:
        data = pd.read_csv('amazon_sales.csv')
        optimized_df, metrics = optimize_sales_data(data)
        metrics.to_csv('category_performance.csv')
    except FileNotFoundError:
        print("⚠️ File not found. Please ensure amazon_sales.csv is in the directory.")
