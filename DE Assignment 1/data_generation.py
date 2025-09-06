import pandas as pd
import numpy as np
import os
from datetime import datetime

# Set a random seed for reproducibility
np.random.seed(42)

# Create a larger, more realistic synthetic dataset with common data issues
num_transactions = 50
products = ['T-Shirt', 'Coffee Mug', 'Hoodie', 'Water Bottle', 'Sticker Pack', 'Notebook', 'Pen Set']
base_prices = [25.99, 12.50, 45.00, 18.75, 5.99, 8.50, 15.25]

data = []
for i in range(num_transactions):
    # Generate a date spread across 3 months (Jan-Mar 2024)
    date_str = f"2024-0{np.random.randint(1, 4)}-{np.random.randint(1, 29):02d}"
    
    # Select a random product
    product_idx = np.random.randint(0, len(products))
    product = products[product_idx]
    
    # Generate quantity (mostly 1-3, occasionally more)
    quantity = np.random.choice([1, 1, 1, 2, 2, 3, 5], p=[0.15, 0.15, 0.15, 0.2, 0.2, 0.1, 0.05])
    
    # Calculate sales amount with occasional issues
    base_price = base_prices[product_idx]
    
    # Introduce various data quality issues
    if np.random.random() < 0.05:  # 5% chance of missing product name
        product = np.nan
    elif np.random.random() < 0.03:  # 3% chance of inconsistent naming
        if product == 'T-Shirt':
            product = 'Tshirt'  # Inconsistent naming
        elif product == 'Coffee Mug':
            product = 'Mug'  # Inconsistent naming
    
    if np.random.random() < 0.04:  # 4% chance of negative quantity
        quantity = -1 * quantity
    elif np.random.random() < 0.06:  # 6% chance of zero quantity
        quantity = 0
    
    if np.random.random() < 0.05:  # 5% chance of extreme price outlier
        sales_amount = base_price * quantity * 100  # Way too high
    elif np.random.random() < 0.03:  # 3% chance of negative price
        sales_amount = -base_price * quantity
    elif np.random.random() < 0.07:  # 7% chance of missing sales amount
        sales_amount = np.nan
    else:
        sales_amount = base_price * quantity
    
    # Add some date format inconsistencies
    if np.random.random() < 0.04:  # 4% chance of different date format
        date_str = f"{np.random.randint(1, 13)}/{np.random.randint(1, 29)}/2024"
    elif np.random.random() < 0.03:  # 3% chance of invalid date
        date_str = "2024-02-30"  # February 30th doesn't exist
    
    # Add some completely empty rows (missing values)
    if np.random.random() < 0.02:  # 2% chance of empty row
        data.append([np.nan, np.nan, np.nan, np.nan])
    else:
        data.append([date_str, product, sales_amount, quantity])

# Create DataFrame
df = pd.DataFrame(data, columns=['date', 'product', 'sales_amount', 'quantity'])

# Add some duplicate rows (3% chance of duplicating previous row)
duplicate_indices = np.random.choice(range(1, num_transactions), 
                                    size=int(num_transactions * 0.03), 
                                    replace=False)
for idx in duplicate_indices:
    df.loc[idx] = df.loc[idx-1]

# Save the "unclean" data

df.to_csv('data/reatail_sales_data.csv', index=False)

print("Realistic (unclean) sample data created and saved!")
print(f"Dataset shape: {df.shape}")
print("\nFirst 10 rows with some issues:")
print(df.head(10))
print("\nSample of issues in data:")
print("- Missing values:", df.isnull().sum().to_dict())
print("- Negative quantities:", (df['quantity'] < 0).sum())
print("- Negative sales:", (df['sales_amount'] < 0).sum() if 'sales_amount' in df.columns else 0)
