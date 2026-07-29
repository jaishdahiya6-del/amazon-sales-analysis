import os
import pandas as pd

def generate_insights():
    print("==================================================")
    print("        AMAZON SALES BUSINESS INSIGHTS           ")
    print("==================================================")

    # 1. Load the cleaned transactional data
    filepath = "data/processed/amazon_sales_transactions.csv"
    if not os.path.exists(filepath):
        print(f"⚠️ Error: Cleaned data file not found at {filepath}")
        print("Please run `python3 src/data_cleaning.py` first.")
        return

    df = pd.read_csv(filepath)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    # 2. High-Level Aggregated Metrics
    total_revenue = df["Revenue"].sum()
    total_profit = df["Profit"].sum()
    total_orders = len(df)
    total_qty = df["Quantity"].sum()
    avg_order_value = total_revenue / total_orders
    overall_margin = (total_profit / total_revenue) * 100

    print(f"Total Transactions:      {total_orders:,}")
    print(f"Total Units Sold:        {total_qty:,}")
    print(f"Total Sales Revenue:     ${total_revenue:,.2f}")
    print(f"Total Gross Profit:      ${total_profit:,.2f}")
    print(f"Overall Profit Margin:   {overall_margin:.2f}%")
    print(f"Average Order Value:     ${avg_order_value:,.2f}")
    print("--------------------------------------------------")

    # 3. Product Category Performance
    print("\n[Sales and Profit by Product Category]")
    cat_df = df.groupby("Category").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    ).sort_values(by="Total_Revenue", ascending=False)

    for cat, row in cat_df.iterrows():
        cat_margin = (row["Total_Profit"] / row["Total_Revenue"]) * 100
        print(f" - {cat:<25}: Sales: ${row['Total_Revenue']:13,.2f} | Profit: ${row['Total_Profit']:11,.2f} ({cat_margin:.1f}% margin)")

    # 4. Regional Performance
    print("\n[Sales and Profit by Region]")
    region_df = df.groupby("Region").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Profit=("Profit", "sum"),
        Units_Sold=("Quantity", "sum")
    ).sort_values(by="Total_Revenue", ascending=False)

    for reg, row in region_df.iterrows():
        reg_share = (row["Total_Revenue"] / total_revenue) * 100
        print(f" - {reg:<12}: Sales: ${row['Total_Revenue']:12,.2f} ({reg_share:5.1f}% share) | Profit: ${row['Total_Profit']:11,.2f}")

    # 5. Customer Segment Performance
    print("\n[Sales and Profit by Customer Segment]")
    segment_df = df.groupby("Segment").agg(
        Total_Revenue=("Revenue", "sum"),
        Total_Profit=("Profit", "sum")
    ).sort_values(by="Total_Revenue", ascending=False)

    for seg, row in segment_df.iterrows():
        print(f" - {seg:<12}: Sales: ${row['Total_Revenue']:12,.2f} | Profit: ${row['Total_Profit']:11,.2f}")

    # 6. Year-over-Year Growth Analysis
    print("\n[Year-over-Year Sales & Profit Growth]")
    df["Year"] = df["Order_Date"].dt.year
    yoy_df = df.groupby("Year").agg(
        Sales=("Revenue", "sum"),
        Profit=("Profit", "sum"),
        Orders=("Revenue", "count")
    ).sort_index()

    prev_sales = None
    prev_profit = None
    for yr, row in yoy_df.iterrows():
        sales_growth_str = "N/A"
        profit_growth_str = "N/A"
        if prev_sales is not None:
            sales_growth = ((row["Sales"] - prev_sales) / prev_sales) * 100
            sales_growth_str = f"{sales_growth:+.2f}%"
        if prev_profit is not None:
            profit_growth = ((row["Profit"] - prev_profit) / prev_profit) * 100
            profit_growth_str = f"{profit_growth:+.2f}%"

        print(f" - Year {yr}: Sales: ${row['Sales']:12,.2f} (Growth: {sales_growth_str:<8}) | Profit: ${row['Profit']:11,.2f} (Growth: {profit_growth_str})")
        prev_sales = row["Sales"]
        prev_profit = row["Profit"]

    # 7. Top 5 Best-Selling Products by Revenue
    print("\n[Top 5 Best-Selling Products by Revenue]")
    top_products = df.groupby(["Product_ID", "Product_Name", "Category"]).agg(
        Total_Revenue=("Revenue", "sum"),
        Units_Sold=("Quantity", "sum")
    ).sort_values(by="Total_Revenue", ascending=False).head(5)

    rank = 1
    for idx, row in top_products.iterrows():
        prod_name = idx[1]
        # Truncate product name for clean output
        if len(prod_name) > 60:
            prod_name = prod_name[:57] + "..."
        print(f" {rank}. {prod_name}")
        print(f"    Category: {idx[2]} | Sales: ${row['Total_Revenue']:,.2f} | Units Sold: {row['Units_Sold']}")
        rank += 1

    print("==================================================")

if __name__ == "__main__":
    generate_insights()
