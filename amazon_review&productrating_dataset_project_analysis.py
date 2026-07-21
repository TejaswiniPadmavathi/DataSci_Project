import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns 
df=pd.read_csv(r"C:/Users/TEJU/Downloads/amazon_sales_dataset_CLEANED.csv")
# print(df.dtypes)

# Convert rating_count to numeric
df['rating_count'] = df['rating_count'].astype(str).str.replace(',', '')
df['rating_count'] = pd.to_numeric(df['rating_count'], errors='coerce')

# Convert rating to numeric
df['rating'] = pd.to_numeric(df['rating'], errors='coerce')

# Convert discount percentage to numeric
df['discount_percentage'] = (
    df['discount_percentage']
    .astype(str)
    .str.replace('%', '')
)

df['discount_percentage'] = pd.to_numeric(
    df['discount_percentage'],
    errors='coerce'
)
# print(df.dtypes)

# 1. Rating Distribution
plt.figure(figsize=(8,5))
sns.histplot(df['rating'], bins=10, kde=True)
plt.title("Distribution of Product Ratings")
plt.xlabel("Rating")
plt.ylabel("Frequency")
plt.show()

# 2. Discount Trends
plt.figure(figsize=(8,5))
sns.histplot(df['discount_percentage'], bins=15, color='orange')
plt.title("Discount Percentage Distribution")
plt.xlabel("Discount Percentage")
plt.ylabel("Number of Products")
plt.show()

# 3. Price Comparison
avg_prices = pd.DataFrame({
    'Price Type': ['Actual Price', 'Discounted Price'],
    'Average Price': [
        df['actual_price'].mean(),
        df['discounted_price'].mean()
    ]
})
plt.figure(figsize=(6,5))
sns.barplot(
    data=avg_prices,
    x='Price Type',
    y='Average Price'
)
plt.title("Average Actual Price vs Discounted Price")
plt.ylabel("Price (₹)")
plt.show()

# 4. Customer Review Frequency
top_reviews = (
    df[['product_name', 'rating_count']]
    .sort_values(by='rating_count', ascending=False)
    .head(10)
)
plt.figure(figsize=(12,6))
sns.barplot(
    data=top_reviews,
    x='rating_count',
    y='product_name'
)
plt.title("Top 10 Products by Review Count")
plt.xlabel("Review Count")
plt.ylabel("Product Name")
plt.show()

# 5. Category Performance
category_rating = (
    df.groupby('category')['rating']
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
plt.figure(figsize=(12,6))
sns.barplot(
    x=category_rating.values,
    y=category_rating.index
)
plt.title("Top 10 Categories by Average Rating")
plt.xlabel("Average Rating")
plt.ylabel("Category")
plt.show()
