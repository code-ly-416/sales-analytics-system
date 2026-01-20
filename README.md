# Sales Analytics System

A Python tool that processes sales transaction data, enriches it with product info from an API, and generates detailed analytics reports.

## What It Does

Takes raw sales data from text files, validates and cleans it up, pulls extra product details from DummyJSON API, runs analytics on everything, and outputs a comprehensive report. Basically automates the whole sales analysis workflow.

**Key Features:**
- Reads and parses pipe-delimited sales data (handles encoding issues)
- Validates transactions (checks for missing fields, negative values, wrong formats)
- Interactive filtering by region and amount
- Enriches data with API product information
- Generates analytics: regional performance, top products, customer insights, daily trends
- Creates formatted text reports

## Setup

**Requirements:**
- Python 3.7+
- Internet connection (for API calls)

**Installation:**

```bash
# Clone the repo
git clone https://github.com/code-ly-416/sales-analytics-system.git
cd sales-analytics-system

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Running the Program

```bash
python main.py
```

The program will guide you through the process:
1. Reads data from `data/sales_data.txt`
2. Parses and cleans the transactions
3. Shows available filters (regions, amount ranges)
4. Asks if you want to filter data
5. Validates the data.
6. Fetches product data from API
7. Enriches your transactions with API data
8. Generates the report

**Outputs:**
- `data/enriched_sales_data.txt` - transactions with added API fields
- `output/sales_report.txt` - full analytics report

## Input Data Format

Your `sales_data.txt` should be pipe-delimited like this:

```
TransactionID|Date|ProductID|ProductName|Quantity|UnitPrice|CustomerID|Region
T001|2024-12-01|P101|Laptop|2|45000|C001|North
T002|2024-12-01|P102|Mouse|5|500|C002|South
```

**Field Requirements:**
- TransactionID: Must start with 'T'
- Quantity and UnitPrice: Must be positive numbers
- Region: North, South, East, or West

## Example Output

```
========================================
SALES ANALYTICS SYSTEM
========================================

[1/10] Reading sales data...
✓ Successfully read 95 transactions

[2/10] Parsing and cleaning data...
✓ Parsed 95 records

[3/10] Filter Options Available:
Regions: East, North, South, West
Amount Range: ₹500 - ₹90,000

Do you want to filter data? (y/n): n

[4/10] Validating transactions...
✓ Valid: 92 | Invalid: 3

[5/10] Analyzing sales data...
✓ Analysis complete

[6/10] Fetching product data from API...
   ✓ Fetched 194 products

[7/10] Enriching sales data...
✓ Enriched 92 transactions

[8/10] Saving enriched data...
✓ Enriched data saved to: data/enriched_sales_data.txt

[9/10] Generating comprehensive report...
✓ sales report generated: output/sales_report.txt

[10/10] Process completed successfully
```

## Project Structure

```
sales-analytics-system/
├── data/
│   ├── sales_data.txt           # Input file
│   └── enriched_sales_data.txt  # Enriched output
├── output/
│   └── sales_report.txt         # Final report
├── utils/
│   ├── file_handler.py          # Data reading/parsing/validation
│   ├── data_processor.py        # Analytics functions
│   ├── api_handler.py           # API integration
│   └── report_generator.py      # Report generation
├── main.py                      # Run this
└── requirements.txt
```

## What's in the Report

The generated report includes:
- Overall summary (total revenue, transactions, average order value)
- Region-wise performance breakdown
- Top 5 products by revenue
- Top 5 customers by spending
- Daily sales trends
- Best selling day
- Low-performing products
- API enrichment stats
