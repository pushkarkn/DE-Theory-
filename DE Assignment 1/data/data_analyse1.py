import pandas as pd
import numpy as np
from datetime import datetime
import os
import matplotlib.pyplot as plt

def clean_retail_data(input_file, output_file):
    """
    Cleans the retail sales data by handling various data quality issues.
    
    Parameters:
    input_file (str): Path to the raw data CSV file
    output_file (str): Path to save the cleaned data CSV file
    
    Returns:
    pandas.DataFrame: Cleaned DataFrame
    """
    
    print("Loading raw data...")
    df = pd.read_csv(input_file)
    print(f"Original data shape: {df.shape}")
    print("Initial missing values:")
    print(df.isnull().sum())
    print("\n" + "="*50)
    
    # 1. Handle completely empty rows
    print("1. Removing completely empty rows...")
    initial_count = len(df)
    df = df.dropna(how='all')
    print(f"   Removed {initial_count - len(df)} completely empty rows")
    
    # 2. Handle duplicates
    print("2. Removing duplicate rows...")
    initial_count = len(df)
    df = df.drop_duplicates()
    print(f"   Removed {initial_count - len(df)} duplicate rows")
    
    # 3. Clean and standardize the date column
    print("3. Cleaning date column...")
    
    def clean_date(date_val):
        """Helper function to clean and parse dates from various formats"""
        if pd.isna(date_val):
            return pd.NaT
        
        date_str = str(date_val).strip()
        
        # Handle different date formats
        try:
            if '/' in date_str:
                # Handle MM/DD/YYYY format
                return pd.to_datetime(date_str, format='%m/%d/%Y', errors='coerce')
            else:
                # Handle YYYY-MM-DD format
                return pd.to_datetime(date_str, format='%Y-%m-%d', errors='coerce')
        except:
            return pd.NaT
    
    df['date'] = df['date'].apply(clean_date)
    
    # Remove rows with invalid dates
    initial_count = len(df)
    df = df[df['date'].notna()]
    print(f"   Removed {initial_count - len(df)} rows with invalid dates")
    
    # 4. Clean and standardize product names
    print("4. Standardizing product names...")
    
    # First, handle missing product names
    initial_missing_products = df['product'].isna().sum()
    df = df[df['product'].notna()]  # Remove rows with missing product names
    
    # Standardize product naming
    product_mapping = {
        'tshirt': 'T-Shirt',
        't-shirt': 'T-Shirt',
        'Tshirt': 'T-Shirt',
        'mug': 'Coffee Mug',
        'Mug': 'Coffee Mug',
        'hoodie': 'Hoodie',
        'water bottle': 'Water Bottle',
        'sticker': 'Sticker Pack',
        'sticker pack': 'Sticker Pack',
        'notebook': 'Notebook',
        'pen': 'Pen Set',
        'pen set': 'Pen Set'
    }
    
    df['product'] = df['product'].str.strip().str.lower()
    df['product'] = df['product'].replace(product_mapping)
    
    print(f"   Removed {initial_missing_products} rows with missing product names")
    print(f"   Standardized {len(product_mapping)} product names")
    
    # 5. Clean quantity column
    print("5. Cleaning quantity column...")
    
    # Convert to numeric, handling errors
    df['quantity'] = pd.to_numeric(df['quantity'], errors='coerce')
    
    # Remove rows with invalid, negative, or zero quantities
    initial_count = len(df)
    df = df[(df['quantity'] > 0) & (df['quantity'].notna())]
    print(f"   Removed {initial_count - len(df)} rows with invalid quantities")
    
    # 6. Clean sales_amount column
    print("6. Cleaning sales amount column...")
    
    # Convert to numeric, handling errors
    df['sales_amount'] = pd.to_numeric(df['sales_amount'], errors='coerce')
    
    # Remove negative sales amounts and extreme outliers
    initial_count = len(df)
    
    # Calculate reasonable bounds for sales amounts
    if not df.empty:
        Q1 = df['sales_amount'].quantile(0.25)
        Q3 = df['sales_amount'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        df = df[(df['sales_amount'] > 0) & 
                (df['sales_amount'] <= upper_bound) &
                (df['sales_amount'].notna())]
    else:
        df = df[(df['sales_amount'] > 0) & (df['sales_amount'].notna())]
    
    print(f"   Removed {initial_count - len(df)} rows with invalid sales amounts")
    
    # 7. Handle remaining missing sales amounts by calculating from average prices
    print("7. Calculating missing sales amounts...")
    
    missing_sales = df['sales_amount'].isna().sum()
    if missing_sales > 0:
        # Calculate average price per product
        valid_data = df[df['sales_amount'].notna()]
        if not valid_data.empty:
            avg_prices = (valid_data.groupby('product')['sales_amount'].sum() / 
                         valid_data.groupby('product')['quantity'].sum()).to_dict()
            
            def fill_missing_sales(row):
                if pd.isna(row['sales_amount']) and row['product'] in avg_prices:
                    return avg_prices[row['product']] * row['quantity']
                return row['sales_amount']
            
            df['sales_amount'] = df.apply(fill_missing_sales, axis=1)
            print(f"   Calculated {missing_sales} missing sales amounts")
    
    # Remove any rows that still have missing values in critical columns
    initial_count = len(df)
    df = df.dropna(subset=['date', 'product', 'quantity', 'sales_amount'])
    print(f"   Removed {initial_count - len(df)} rows with remaining missing values")
    
    # 8. Final data quality check
    print("8. Final data quality check...")
    print(f"   Final data shape: {df.shape}")
    print("   Final missing values:")
    print(df.isnull().sum())
    
    # Basic statistics
    if not df.empty:
        print(f"\n   Data range: {df['date'].min()} to {df['date'].max()}")
        print(f"   Unique products: {df['product'].nunique()}")
        print(f"   Total transactions: {len(df)}")
        print(f"   Total quantity sold: {df['quantity'].sum()}")
        print(f"   Total sales amount: ${df['sales_amount'].sum():.2f}")
    
    # 9. Save cleaned data
    df.to_csv(output_file, index=False)
    print(f"\nCleaned data saved to: {output_file}")
    
    return df

if __name__ == "__main__":
    # File paths
    input_file = "data/raw_sales_data.csv"
    output_file = "data/cleaned_sales_data.csv"
    
    # Clean the data
    cleaned_df = clean_retail_data(input_file, output_file)
    
    print("\n" + "="*50)
    print("DATA CLEANING COMPLETE!")
    print("="*50)
    
    # Show sample of cleaned data
    if not cleaned_df.empty:
        print("\nSample of cleaned data:")
        print(cleaned_df.head(10))

        # Load cleaned data for analysis
        df = pd.read_csv(output_file)
        df['date'] = pd.to_datetime(df['date'])

        # 1. Items ranked by most revenue generated
        revenue_by_product = df.groupby('product')['sales_amount'].sum().sort_values(ascending=False)
        plt.figure(figsize=(8, 6))
        plt.bar(revenue_by_product.index, revenue_by_product.values, color='skyblue')
        plt.title('Items Ranked by Most Revenue Generated')
        plt.xlabel('Product')
        plt.ylabel('Revenue ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # 2. Items ranked by most quantity bought
        quantity_by_product = df.groupby('product')['quantity'].sum().sort_values(ascending=False)
        plt.figure(figsize=(8, 6))
        plt.bar(quantity_by_product.index, quantity_by_product.values, color='lightgreen')
        plt.title('Items Ranked by Most Quantity Bought')
        plt.xlabel('Product')
        plt.ylabel('Quantity')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()

        # 3. Monthly sales
        df['month'] = df['date'].dt.to_period('M')
        monthly_sales = df.groupby('month')['sales_amount'].sum()
        plt.figure(figsize=(8, 6))
        plt.bar(monthly_sales.index.astype(str), monthly_sales.values, color='salmon')
        plt.title('Monthly Sales')
        plt.xlabel('Month')
        plt.ylabel('Sales ($)')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
