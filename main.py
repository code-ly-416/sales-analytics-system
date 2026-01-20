from utils.file_handler import *
import os

def main():
    file_path = os.path.join("data", "sales_data.txt")

    print("Starting Sales Analytics System...")

    # reading raw file
    print(f"\n[1] Reading file: {file_path}")
    raw_lines = read_sales_data(file_path)
    print(f"Raw lines read: {len(raw_lines)}")

    if not raw_lines:
        print("Terminating: no data found.")
        return

    # step 2: parse raw lines into dictionaries
    print("\n[2] Parsing transactions...")
    transactions = parse_transactions(raw_lines)
    print(f"Transactions parsed: {len(transactions)}")

    # step 3: validate and filter
    print("\n[3] Validating data...")
    # running without filters first to get the baseline valid count
    valid_data, invalid_count, summary = validate_and_filter(transactions)

if __name__ == "__main__":
    main()
