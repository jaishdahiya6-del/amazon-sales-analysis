# Category-wise total sales (ya discounted price)
category_sales = df.groupby('category')['discounted_price'].sum().sort_values(ascending=False).head(10)

print("Top 10 Categories by Sales:")
print(category_sales)

# Iska insight: "Electronics category is generating 40% of total revenue."
# Check correlation between Discount Percentage and Rating
# Note: Pehle columns ko numeric mein convert karna pad sakta hai
correlation = df['discount_percentage'].corr(df['rating'])

print(f"Correlation between Discount and Rating: {correlation}")

# Insight: "High discounts do not necessarily lead to higher customer ratings."
# Rating ki distribution check karein
print(f"Average Product Rating: {df['rating'].mean():.2f}")

# Counting ratings (e.g., how many 5 stars vs 1 star)
rating_counts = df['rating'].value_counts().sort_index()
print(rating_counts)

# Insight: "80% of products have a rating above 4.0, showing high customer satisfaction."
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Data Load Karein
# File ka naam check kar lena (e.g., 'amazon.csv')
df = pd.read_csv('amazon.csv')

# 2. Data Cleaning (Zaruri Step)
# 'rating_count' ko numeric banayein taaki calculation sahi ho
df['rating_count'] = pd.to_numeric(df['rating_count'].str.replace(',', ''), errors='coerce')
df.dropna(subset=['rating_count'], inplace=True)

# 3. Grouping & Sorting
# Har product ke ratings ko total karke top 10 nikalna
top_10 = df.groupby('product_name')['rating_count'].sum().sort_values(ascending=False).head(10).reset_index()

# 4. Visualization Creation
plt.figure(figsize=(12, 8))
sns.set_style("whitegrid")

# Horizontal Bar Chart banayein
ax = sns.barplot(data=top_10, x='rating_count', y='product_name', palette='viridis')

# Labels aur Title
plt.title('Day 11: Top 10 Best Selling Products (by Rating Count)', fontsize=15, fontweight='bold')
plt.xlabel('Total Rating Count', fontsize=12)
plt.ylabel('Product Name', fontsize=12)

# Bars par numbers dikhayyein (Professional Look)
for i in ax.containers:
    ax.bar_label(i, padding=3)

# 5. Save the Image
# Ise save karna mat bhulna Day 14 ke task ke liye
plt.tight_layout()
plt.savefig('top_10_products.png')
plt.show()
