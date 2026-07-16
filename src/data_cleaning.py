import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("amazon_sales.csv")

# Show first rows
print(data.head())

# Total Sales
total_sales = data["Sales"].sum()

print("Total Sales:", total_sales)

# Sales by Category
category_sales = data.groupby("Category")["Sales"].sum()

# Plot
category_sales.plot(kind="bar", title="Sales by Category")
plt.show()
