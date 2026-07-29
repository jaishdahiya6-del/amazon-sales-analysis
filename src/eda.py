import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def optimize_data_types(df):
    """
    Optimizes data types for low-cardinality strings to category dtype
    to improve performance and memory usage.
    """
    print("⚡ Optimizing dataframe memory footprint...")
    for col in ["Category", "Region", "State", "Segment"]:
        if col in df.columns:
            df[col] = df[col].astype("category")
    return df

def run_eda():
    print("🚀 Starting Exploratory Data Analysis & Visualization...")

    # Set seaborn style for professional looks
    sns.set_theme(style="whitegrid")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["font.size"] = 12

    # 1. Load Clean Dataset
    filepath = "data/processed/amazon_sales_transactions.csv"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Cleaned dataset not found at {filepath}. Please run data_cleaning.py first.")

    df = pd.read_csv(filepath)
    df["Order_Date"] = pd.to_datetime(df["Order_Date"])

    # Optimize data types
    df = optimize_data_types(df)

    # Ensure visualizations directory exists
    vis_dir = "visualizations"
    os.makedirs(vis_dir, exist_ok=True)

    # --- CHART 1: Monthly and Quarterly Sales Trends over Time ---
    print("Generating Chart 1: Sales trends over time (Monthly/Quarterly)...")
    # Group by Year-Month
    df["Year_Month"] = df["Order_Date"].dt.to_period("M")
    monthly_sales = df.groupby("Year_Month")["Revenue"].sum().reset_index()
    monthly_sales["Year_Month_Str"] = monthly_sales["Year_Month"].astype(str)

    fig, ax1 = plt.subplots(figsize=(12, 6))

    color = "royalblue"
    ax1.set_xlabel("Month-Year", fontweight="bold", labelpad=10)
    ax1.set_ylabel("Monthly Revenue ($)", color=color, fontweight="bold")
    ax1.plot(monthly_sales["Year_Month_Str"], monthly_sales["Revenue"], marker="o", linewidth=2.5, color=color, label="Monthly Sales")
    ax1.tick_params(axis="y", labelcolor=color)
    ax1.set_xticks(range(0, len(monthly_sales), 2))
    ax1.set_xticklabels(monthly_sales["Year_Month_Str"].iloc[::2], rotation=45, ha="right")

    # Group by Year-Quarter on second axis or separate panel
    df["Year_Quarter"] = df["Order_Date"].dt.to_period("Q")
    quarterly_sales = df.groupby("Year_Quarter")["Revenue"].sum().reset_index()
    quarterly_sales["Year_Quarter_Str"] = quarterly_sales["Year_Quarter"].astype(str)

    # Let's save a unified trend plot
    plt.title("Amazon Monthly Sales Trends (2022 - 2024)", fontsize=16, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "01_sales_trends_over_time.png"), dpi=150)
    plt.close()

    # --- CHART 2: Revenue by Product Category & Region ---
    print("Generating Chart 2: Revenue by Category and Region...")
    cat_region = df.groupby(["Category", "Region"], observed=False)["Revenue"].sum().unstack().fillna(0)

    # Plot stacked bar chart or grouped bar chart
    fig, ax = plt.subplots(figsize=(12, 7))
    cat_region_sorted = cat_region.loc[cat_region.sum(axis=1).sort_values(ascending=False).index]

    cat_region_sorted.plot(kind="bar", stacked=True, colormap="viridis", ax=ax, width=0.75)
    plt.title("Revenue by Product Category and Region ($)", fontsize=16, fontweight="bold", pad=15)
    plt.xlabel("Product Category", fontweight="bold")
    plt.ylabel("Total Revenue ($)", fontweight="bold")
    plt.xticks(rotation=30, ha="right")
    plt.legend(title="Region", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "02_revenue_by_category_and_region.png"), dpi=150)
    plt.close()

    # --- CHART 3: Top-Selling Products (SKUs) and Categories ---
    print("Generating Chart 3: Top-selling products and categories...")
    # Top selling categories by total quantity sold
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    top_cats_qty = df.groupby("Category", observed=False)["Quantity"].sum().sort_values(ascending=False).head(5)
    sns.barplot(x=top_cats_qty.values, y=top_cats_qty.index, palette="Blues_r", ax=ax1, hue=top_cats_qty.index, legend=False)
    ax1.set_title("Top 5 Categories by Units Sold", fontsize=14, fontweight="bold")
    ax1.set_xlabel("Total Quantity Sold")
    ax1.set_ylabel("Category")

    # Top 5 selling products by revenue
    top_prods_rev = df.groupby("Product_Name")["Revenue"].sum().sort_values(ascending=False).head(5)
    # Truncate long names for presentation
    short_names = [name[:30] + "..." if len(name) > 30 else name for name in top_prods_rev.index]
    sns.barplot(x=top_prods_rev.values, y=short_names, palette="Oranges_r", ax=ax2, hue=short_names, legend=False)
    ax2.set_title("Top 5 Products by Revenue Contribution", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Total Sales Revenue ($)")
    ax2.set_ylabel("Product Name")

    plt.suptitle("Top Products & Categories Performance Analysis", fontsize=18, fontweight="bold")
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "03_top_products_and_categories.png"), dpi=150)
    plt.close()

    # --- CHART 4: Year-over-Year Growth Rate ---
    print("Generating Chart 4: YoY Sales and Profit growth...")
    df["Year"] = df["Order_Date"].dt.year
    yearly_perf = df.groupby("Year").agg({"Revenue": "sum", "Profit": "sum"}).reset_index()

    # Calculate YoY change percentages
    yearly_perf["Sales_YoY_Growth"] = yearly_perf["Revenue"].pct_change() * 100
    yearly_perf["Profit_YoY_Growth"] = yearly_perf["Profit"].pct_change() * 100

    # Bar plot comparing Revenue vs Profit over years
    fig, ax1 = plt.subplots(figsize=(10, 6))

    years = yearly_perf["Year"].astype(str)
    x = np.arange(len(years))
    width = 0.35

    rects1 = ax1.bar(x - width/2, yearly_perf["Revenue"], width, label="Revenue", color="teal")
    ax2 = ax1.twinx()
    rects2 = ax2.bar(x + width/2, yearly_perf["Profit"], width, label="Profit", color="orange")

    ax1.set_xlabel("Year", fontweight="bold")
    ax1.set_ylabel("Revenue ($)", color="teal", fontweight="bold")
    ax1.tick_params(axis="y", labelcolor="teal")
    ax2.set_ylabel("Profit ($)", color="orange", fontweight="bold")
    ax2.tick_params(axis="y", labelcolor="orange")

    ax1.set_xticks(x)
    ax1.set_xticklabels(years)

    # Add legends
    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

    plt.title("Year-over-Year (YoY) Sales and Profit Growth", fontsize=16, fontweight="bold", pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "04_yoy_growth.png"), dpi=150)
    plt.close()

    # --- CHART 5: Segment Analysis ---
    print("Generating Chart 5: Sales and Profit share by Customer Segment...")
    segment_data = df.groupby("Segment", observed=False).agg({"Revenue": "sum", "Profit": "sum"}).reset_index()

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    colors = ["#ff9999","#66b3ff","#99ff99"]

    # Revenue Pie Chart
    ax1.pie(segment_data["Revenue"], labels=segment_data["Segment"], autopct="%1.1f%%", startangle=90, colors=colors, shadow=True,
            textprops={"fontweight": "bold"})
    ax1.axis("equal")
    ax1.set_title("Revenue Contribution by Segment", fontsize=14, fontweight="bold")

    # Profit Pie Chart
    ax2.pie(segment_data["Profit"], labels=segment_data["Segment"], autopct="%1.1f%%", startangle=90, colors=colors, shadow=True,
            textprops={"fontweight": "bold"})
    ax2.axis("equal")
    ax2.set_title("Profit Contribution by Segment", fontsize=14, fontweight="bold")

    plt.suptitle("Customer Segment Sales and Profit Distribution", fontsize=16, fontweight="bold", y=0.98)
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "05_customer_segments_share.png"), dpi=150)
    plt.close()

    # Backwards compatibility/Clean-up: Let's copy/create equivalent files
    # so that the README links aren't broken if they depend on specific file names.
    # We will save sales by category to visualizations/01_sales_by_category.png
    fig, ax = plt.subplots(figsize=(10, 6))
    cat_sales = df.groupby("Category", observed=False)["Revenue"].sum().sort_values(ascending=False)
    sns.barplot(x=cat_sales.values, y=cat_sales.index, palette="viridis", ax=ax, hue=cat_sales.index, legend=False)
    plt.title("Sales Distribution by Category ($)", fontsize=16, fontweight="bold")
    plt.xlabel("Total Sales Revenue ($)")
    plt.ylabel("Category")
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "01_sales_by_category.png"), dpi=150)
    plt.close()

    # We will save top products to visualizations/08_top_skus.png
    fig, ax = plt.subplots(figsize=(10, 6))
    top_skus = df.groupby("Product_Name")["Quantity"].sum().sort_values(ascending=False).head(10)
    truncated_sku_names = [name[:40] + "..." if len(name) > 40 else name for name in top_skus.index]
    sns.barplot(x=top_skus.values, y=truncated_sku_names, palette="rocket", ax=ax, hue=truncated_sku_names, legend=False)
    plt.title("Top 10 Best Selling Products (SKUs) by Quantity", fontsize=16, fontweight="bold")
    plt.xlabel("Total Units Sold")
    plt.ylabel("Product SKU Name")
    plt.tight_layout()
    plt.savefig(os.path.join(vis_dir, "08_top_skus.png"), dpi=150)
    plt.close()

    print("🎉 All 5 high-quality visualizations generated and saved in the 'visualizations/' folder.")

if __name__ == "__main__":
    run_eda()
