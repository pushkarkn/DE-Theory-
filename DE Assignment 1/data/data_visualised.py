import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

def analyze_and_visualize(cleaned_data_file):
    """
    Analyze the cleaned data and create visualizations without generating CSV files.
    """
    print("Loading cleaned data for visualization...")
    df = pd.read_csv(cleaned_data_file)
    df['date'] = pd.to_datetime(df['date'])
    
    print(f"Data shape for analysis: {df.shape}")
    
    # 1. ANALYSIS (in-memory only, no CSV output)
    print("\nPerforming analysis for visualization...")
    
    # Create month column for time-based analysis
    df['month'] = df['date'].dt.to_period('M')
    df['month_str'] = df['month'].astype(str)
    
    # Calculate analysis metrics in memory
    monthly_sales = df.groupby('month')['sales_amount'].sum().reset_index()
    monthly_sales['month_str'] = monthly_sales['month'].astype(str)
    
    top_products_qty = df.groupby('product')['quantity'].sum().nlargest(5).reset_index()
    top_products_revenue = df.groupby('product')['sales_amount'].sum().nlargest(5).reset_index()
    
    daily_sales = df.groupby('date')['sales_amount'].sum().reset_index()
    product_avg_price = (df.groupby('product')['sales_amount'].sum() / 
                        df.groupby('product')['quantity'].sum()).sort_values(ascending=False).reset_index()
    product_avg_price.columns = ['product', 'average_price']
    
    # 2. VISUALIZATION - Create a comprehensive dashboard
    print("Creating comprehensive visualizations...")
    
    # Create a figure with multiple subplots
    fig = plt.figure(figsize=(18, 14))
    fig.suptitle('📊 Retail Sales Performance Dashboard\nComprehensive Analysis & Visualization', 
                 fontsize=18, fontweight='bold', y=0.98)
    
    # Define the grid layout
    gs = fig.add_gridspec(3, 3)
    
    # Plot 1: Monthly Sales Trend (top left)
    ax1 = fig.add_subplot(gs[0, 0])
    bars = ax1.bar(monthly_sales['month_str'], monthly_sales['sales_amount'], 
                   color=['#FF6B6B', '#4ECDC4', '#45B7D1'], alpha=0.8)
    ax1.set_title('📈 Monthly Sales Revenue', fontweight='bold', fontsize=12)
    ax1.set_xlabel('Month')
    ax1.set_ylabel('Sales Amount ($)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 5,
                f'${height:.0f}', ha='center', va='bottom', fontweight='bold')
    
    # Plot 2: Top Products by Quantity (top middle)
    ax2 = fig.add_subplot(gs[0, 1])
    colors = plt.cm.Set3(np.linspace(0, 1, len(top_products_qty)))
    bars = ax2.bar(top_products_qty['product'], top_products_qty['quantity'], 
                   color=colors, alpha=0.8)
    ax2.set_title('🏆 Top 5 Products by Quantity Sold', fontweight='bold', fontsize=12)
    ax2.set_xlabel('Product')
    ax2.set_ylabel('Quantity Sold')
    ax2.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                f'{int(height)}', ha='center', va='bottom', fontweight='bold')
    
    # Plot 3: Top Products by Revenue (top right)
    ax3 = fig.add_subplot(gs[0, 2])
    colors = plt.cm.Pastel1(np.linspace(0, 1, len(top_products_revenue)))
    bars = ax3.bar(top_products_revenue['product'], top_products_revenue['sales_amount'], 
                   color=colors, alpha=0.8)
    ax3.set_title('💰 Top 5 Products by Revenue', fontweight='bold', fontsize=12)
    ax3.set_xlabel('Product')
    ax3.set_ylabel('Revenue ($)')
    ax3.tick_params(axis='x', rotation=45)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'${height:.0f}', ha='center', va='bottom', fontweight='bold')
    
    # Plot 4: Sales Distribution Pie Chart (middle left)
    ax4 = fig.add_subplot(gs[1, 0])
    product_sales = df.groupby('product')['sales_amount'].sum()
    colors = plt.cm.Set3(np.linspace(0, 1, len(product_sales)))
    wedges, texts, autotexts = ax4.pie(product_sales.values, labels=product_sales.index, 
                                       autopct='%1.1f%%', colors=colors, startangle=90)
    ax4.set_title('📊 Sales Distribution by Product', fontweight='bold', fontsize=12)
    
    # Make autopct text larger and bold
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')
    
    # Plot 5: Daily Sales Trend (middle right)
    ax5 = fig.add_subplot(gs[1, 1:])
    ax5.plot(daily_sales['date'], daily_sales['sales_amount'], 
             marker='o', markersize=4, linewidth=2, color='#6A0DAD', alpha=0.8)
    ax5.set_title('📅 Daily Sales Trend', fontweight='bold', fontsize=12)
    ax5.set_xlabel('Date')
    ax5.set_ylabel('Daily Sales ($)')
    ax5.grid(True, alpha=0.3)
    ax5.tick_params(axis='x', rotation=45)
    
    # Plot 6: Average Product Prices (bottom left)
    ax6 = fig.add_subplot(gs[2, 0])
    colors = plt.cm.viridis(np.linspace(0, 1, len(product_avg_price)))
    bars = ax6.barh(product_avg_price['product'], product_avg_price['average_price'], 
                    color=colors, alpha=0.8)
    ax6.set_title('🏷️ Average Product Prices', fontweight='bold', fontsize=12)
    ax6.set_xlabel('Average Price ($)')
    ax6.set_ylabel('Product')
    
    # Add value labels on bars
    for bar in bars:
        width = bar.get_width()
        ax6.text(width + 0.5, bar.get_y() + bar.get_height()/2.,
                f'${width:.2f}', ha='left', va='center', fontweight='bold')
    
    # Plot 7: Summary Statistics (bottom middle/right)
    ax7 = fig.add_subplot(gs[2, 1:])
    ax7.axis('off')  # Turn off axis for text display
    
    # Calculate summary statistics
    total_sales = df['sales_amount'].sum()
    total_quantity = df['quantity'].sum()
    avg_transaction = total_sales / len(df)
    total_products = df['product'].nunique()
    date_range = f"{df['date'].min().strftime('%Y-%m-%d')} to {df['date'].max().strftime('%Y-%m-%d')}"
    
    # Create summary text
    summary_text = (
        f"📊 BUSINESS SUMMARY\n\n"
        f"• Total Revenue: ${total_sales:,.2f}\n"
        f"• Total Units Sold: {total_quantity:,}\n"
        f"• Average Transaction: ${avg_transaction:.2f}\n"
        f"• Unique Products: {total_products}\n"
        f"• Total Transactions: {len(df):,}\n"
        f"• Date Range: {date_range}\n"
        f"• Best Selling Product: {top_products_qty.iloc[0]['product']}\n"
        f"• Highest Revenue Product: {top_products_revenue.iloc[0]['product']}"
    )
    
    ax7.text(0.1, 0.9, summary_text, fontsize=12, fontfamily='monospace',
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.7))
    
    # Adjust layout
    plt.tight_layout()
    plt.subplots_adjust(top=0.93, hspace=0.4, wspace=0.3)
    
    # Save the comprehensive dashboard
    plt.savefig('assets/sales_dashboard.png', dpi=120, bbox_inches='tight')
    plt.show()
    
    # Print summary to console
    print("\n" + "="*60)
    print("VISUALIZATION SUMMARY")
    print("="*60)
    print(f"Total Revenue: ${total_sales:,.2f}")
    print(f"Total Units Sold: {total_quantity}")
    print(f"Average Transaction Value: ${avg_transaction:.2f}")
    print(f"Date Range: {date_range}")
    print(f"Best Selling Product: {top_products_qty.iloc[0]['product']} ({top_products_qty.iloc[0]['quantity']} units)")
    print(f"Highest Revenue Product: {top_products_revenue.iloc[0]['product']} (${top_products_revenue.iloc[0]['sales_amount']:.2f})")
    print("="*60)
    
    print("\nVisualization complete! Dashboard saved to: assets/sales_dashboard.png")

if __name__ == "__main__":
    cleaned_data_file = "data/cleaned_sales_data.csv"
    analyze_and_visualize(cleaned_data_file)