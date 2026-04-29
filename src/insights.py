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
