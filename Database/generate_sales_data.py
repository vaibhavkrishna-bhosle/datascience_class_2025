"""
Generate Sales Dataset for Statistical Analysis Tutorial
This script creates a dataset for learning pandas statistical methods
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Set seeds for reproducibility
np.random.seed(42)
random.seed(42)

# Configuration
num_records = 500

# Define categories
regions = ['North', 'South', 'East', 'West', 'Central']
product_categories = ['Electronics', 'Clothing', 'Food', 'Books', 'Toys', 'Sports', 'Home & Garden']
products = {
    'Electronics': ['Laptop', 'Smartphone', 'Tablet', 'Headphones', 'Smart Watch'],
    'Clothing': ['T-Shirt', 'Jeans', 'Jacket', 'Shoes', 'Dress'],
    'Food': ['Coffee', 'Snacks', 'Beverages', 'Frozen Food', 'Fresh Produce'],
    'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Comics', 'Magazines'],
    'Toys': ['Action Figures', 'Board Games', 'Puzzles', 'Dolls', 'Building Blocks'],
    'Sports': ['Basketball', 'Football', 'Tennis Racket', 'Yoga Mat', 'Dumbbells'],
    'Home & Garden': ['Furniture', 'Kitchen Appliances', 'Decor', 'Gardening Tools', 'Bedding']
}

sales_channels = ['Online', 'Store', 'Phone']
customer_segments = ['Individual', 'Corporate', 'Small Business']

# Generate data
data = {
    'order_id': [],
    'date': [],
    'region': [],
    'sales_channel': [],
    'customer_segment': [],
    'category': [],
    'product': [],
    'quantity': [],
    'unit_price': [],
    'total_sales': [],
    'discount_percent': [],
    'shipping_cost': [],
    'profit_margin': []
}

start_date = datetime(2023, 1, 1)
end_date = datetime(2024, 12, 31)

for i in range(num_records):
    # Generate order_id
    order_id = f"ORD{2023 + random.randint(0, 1)}{random.randint(10000, 99999)}"
    
    # Generate random date
    days_between = (end_date - start_date).days
    random_days = random.randint(0, days_between)
    order_date = start_date + timedelta(days=random_days)
    
    # Select category and product
    category = random.choice(product_categories)
    product = random.choice(products[category])
    
    # Generate sales data with realistic distributions
    quantity = np.random.randint(1, 50)
    
    # Different price ranges for different categories
    if category == 'Electronics':
        unit_price = round(np.random.uniform(200, 2000), 2)
        profit_margin = round(np.random.uniform(15, 40), 2)
    elif category == 'Clothing':
        unit_price = round(np.random.uniform(20, 200), 2)
        profit_margin = round(np.random.uniform(30, 60), 2)
    elif category == 'Food':
        unit_price = round(np.random.uniform(5, 50), 2)
        profit_margin = round(np.random.uniform(20, 45), 2)
    elif category == 'Books':
        unit_price = round(np.random.uniform(10, 60), 2)
        profit_margin = round(np.random.uniform(35, 55), 2)
    elif category == 'Toys':
        unit_price = round(np.random.uniform(15, 150), 2)
        profit_margin = round(np.random.uniform(25, 50), 2)
    elif category == 'Sports':
        unit_price = round(np.random.uniform(30, 300), 2)
        profit_margin = round(np.random.uniform(28, 48), 2)
    else:  # Home & Garden
        unit_price = round(np.random.uniform(50, 500), 2)
        profit_margin = round(np.random.uniform(22, 45), 2)
    
    total_sales = round(quantity * unit_price, 2)
    discount_percent = round(np.random.uniform(0, 25), 2)
    
    # Shipping cost based on channel
    channel = random.choice(sales_channels)
    if channel == 'Online':
        shipping_cost = round(np.random.uniform(5, 30), 2)
    elif channel == 'Phone':
        shipping_cost = round(np.random.uniform(10, 40), 2)
    else:
        shipping_cost = 0.0
    
    # Add to data
    data['order_id'].append(order_id)
    data['date'].append(order_date.strftime('%Y-%m-%d'))
    data['region'].append(random.choice(regions))
    data['sales_channel'].append(channel)
    data['customer_segment'].append(random.choice(customer_segments))
    data['category'].append(category)
    data['product'].append(product)
    data['quantity'].append(quantity)
    data['unit_price'].append(unit_price)
    data['total_sales'].append(total_sales)
    data['discount_percent'].append(discount_percent)
    data['shipping_cost'].append(shipping_cost)
    data['profit_margin'].append(profit_margin)

# Create DataFrame
df = pd.DataFrame(data)

# Calculate additional columns
df['discount_amount'] = (df['total_sales'] * df['discount_percent'] / 100).round(2)
df['net_sales'] = (df['total_sales'] - df['discount_amount']).round(2)
df['profit'] = (df['net_sales'] * df['profit_margin'] / 100).round(2)
df['total_cost'] = (df['net_sales'] + df['shipping_cost']).round(2)

# Save to CSV
df.to_csv('sales_data.csv', index=False)

print(f"Dataset created successfully!")
print(f"Total records: {len(df)}")
print(f"\nDataset preview:")
print(df.head(10))
print(f"\nDataset info:")
print(df.info())
print(f"\nBasic statistics:")
print(df.describe())
print(f"\nCategories:")
print(f"Regions: {df['region'].unique()}")
print(f"Categories: {df['category'].unique()}")
print(f"Sales Channels: {df['sales_channel'].unique()}")
print(f"\nDataset saved as 'sales_data.csv'")
