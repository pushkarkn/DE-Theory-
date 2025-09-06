# DE Assignment 1: College Campus Merch Store Sales Data Pipeline

A Python-based data engineering project demonstrating a complete ETL pipeline from data generation to visualization for retail sales analysis.

## Project Overview

This project implements a data pipeline that:
1. Generates synthetic retail sales data with realistic data quality issues
2. Cleans and processes the raw data
3. Analyzes sales performance through multiple visualizations
4. Produces actionable business insights

## Folder Structure

```
DE Assignment 1/
│
├── data_generation.py          # Script to generate synthetic raw sales data
├── data_analyse.py             # Main ETL script: cleaning + visualization
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
│
└── data/                       # Data directory
    ├── raw_sales_data.csv      # Generated raw data (with intentional issues)
    └── cleaned_sales_data.csv  # Processed clean data (output from cleaning)
```

## Data Lifecycle Implementation

### 1. Data Generation
The `data_generation.py` script creates a synthetic dataset simulating real-world retail transactions with common data quality issues including:
- Missing values
- Inconsistent product naming conventions
- Invalid date formats
- Negative and outlier values
- Duplicate records

### 2. Data Processing & Cleaning
The `data_analyse.py` script performs comprehensive data cleaning:
- Handles missing values and duplicates
- Standardizes product names and date formats
- Removes invalid transactions and outliers
- Validates data integrity

### 3. Analysis & Visualization
The pipeline generates multiple visualizations:
- Monthly sales revenue trends
- Top products by quantity sold
- Top products by revenue generated
- Sales distribution across product categories
- Daily sales performance
- Average product pricing
- Summary business metrics

## Output

The project produces:
- Cleaned dataset ready for analysis (`data/cleaned_sales_data.csv`)
- Comprehensive sales dashboard visualizations
- Console output with key business metrics including total revenue, units sold, and performance insights
## Dependencies

- pandas
- matplotlib
- numpy
