import pandas as pd

# Read CSV file
df = pd.read_csv("sales_data.csv")

# Display first 5 records
print(df.head())

# Check missing values
print(df.isnull().sum())

# Remove duplicate records
df = df.drop_duplicates()

# Handle missing values
df = df.dropna()

# Convert date column
df["date"] = pd.to_datetime(df["date"])

# Calculate revenue
df["revenue"] = df["quantity"] * df["unit_price"]

print("\nCleaned Data:")
print(df)

# Save cleaned data
df.to_csv("cleaned_sales.csv", index=False)

# Total Revenue
total_revenue = df["revenue"].sum()

# Total Orders
total_orders = df["order_id"].nunique()

# Total Quantity Sold
total_quantity = df["quantity"].sum()

# Average Order Revenue
average_revenue = total_revenue / total_orders

print("Total Revenue:", total_revenue)
print("Total Orders:", total_orders)
print("Total Quantity:", total_quantity)
print("Average Order Revenue:", average_revenue)

# Revenue by Category
category_sales = df.groupby("category")["revenue"].sum()

print("\nCategory-wise Revenue:")
print(category_sales)

# Revenue by Region
region_sales = df.groupby("region")["revenue"].sum()

print("\nRegion-wise Revenue:")
print(region_sales)

# Best Selling Product
best_product = (
    df.groupby("product")["quantity"]
    .sum()
    .idxmax()
)

print("\nBest Selling Product:", best_product)

import sqlite3

# Connect to database
conn = sqlite3.connect("sales.db")

# Store cleaned data
df.to_sql(
    "sales",
    conn,
    if_exists="replace",
    index=False
)

# Execute SQL query
query = """
SELECT region, SUM(revenue) AS total_revenue
FROM sales
GROUP BY region
ORDER BY total_revenue DESC
"""

result = pd.read_sql(query, conn)

print("\nSQL Analysis:")
print(result)

conn.close()

import matplotlib.pyplot as plt

# Region-wise revenue chart
region_sales.plot(kind="bar")

plt.title("Revenue by Region")
plt.xlabel("Region")
plt.ylabel("Revenue")

plt.tight_layout()
plt.savefig("sales_chart.png")
plt.show()