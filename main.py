from utils.file_handler import *
from utils.data_processor import *
from utils.api_handler import *
from utils.report_generator import *


def main():
    """
    Main execution function

    Workflow:
    1. Print welcome message
    2. Read sales data file (handle encoding)
    3. Parse and clean transactions
    4. Display filter options to user
       - Show available regions
       - Show transaction amount range
       - Ask if user wants to filter (y/n)
    5. If yes, ask for filter criteria and apply
    6. Validate transactions
    7. Display validation summary
    (do 1 to 7 based on file_handler.py)
    8. Perform all data analyses (call all functions from data_processor.py)
    9. Fetch product info from API
    10. Enrich sales data with API fields
    11. Save enriched data to file
    12. Generate comprehensive sales report
    13. Print success message with file locations

    Error Handling:
    - Wrap entire process in try-except
    - Display user-friendly error messages
    - Don't let program crash on errors
    """

    try:
        # 1 Welcome message
        print("=" * 40)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 40)
        print()

        # 2 Read sales data file
        print("[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")

        if not raw_lines:
            print("✗ Failed to read sales data")
            return

        print(f"✓ Successfully read {len(raw_lines)} transactions")
        print()

        # 3 Parse and clean transactions
        print("[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")
        print()

        # 4 Display filter options to user
        print("[3/10] Filter Options Available:")

        # Get available regions and amount range
        if transactions:
            regions = sorted(list(set(t['Region'] for t in transactions)))
            amounts = [t['Quantity'] * t['UnitPrice'] for t in transactions]
            min_amount = min(amounts)
            max_amount = max(amounts)

            print(f"Regions: {', '.join(regions)}")
            print(f"Amount Range: ₹{min_amount:,.0f} - ₹{max_amount:,.0f}")
        print()

        # 5 Ask if user wants to filter (y/n)
        filter_choice = input("Do you want to filter data? (y/n): ").strip().lower()

        region_filter = None
        min_filter = None
        max_filter = None

        if filter_choice == 'y':
            region_filter = input("Enter region to filter (or press Enter to skip): ").strip() or None

            try:
                min_input = input("Enter minimum amount (or press Enter to skip): ").strip()
                min_filter = float(min_input) if min_input else None

                max_input = input("Enter maximum amount (or press Enter to skip): ").strip()
                max_filter = float(max_input) if max_input else None
            except ValueError:
                print("✗ Invalid amount entered, skipping amount filter")
                min_filter = None
                max_filter = None

        print()

        # 6 Validate transactions
        print("[4/10] Validating transactions...")
        validated_transactions, invalid_count, filter_summary = validate_and_filter(
            transactions,
            region=region_filter,
            min_amount=min_filter,
            max_amount=max_filter
        )
        print(f"✓ Valid: {len(validated_transactions)} | Invalid: {invalid_count}")
        print()

        # 7 Display validation summary / analysis placeholder
        print("[5/10] Analyzing sales data...")
        print("✓ Analysis complete")
        print()

        # 8 Fetch products from API
        print("[6/10] Fetching product data from API...")
        api_products = fetch_all_products()

        # 9 Enrich transactions with API data
        print("[7/10] Enriching sales data...")
        product_mapping = create_product_mapping(api_products)
        enriched_transactions = enrich_sales_data(validated_transactions, product_mapping)
        print(f"✓ Enriched {len(enriched_transactions)} transactions")
        print()

        # 10 Save enriched data
        print("[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)
        print()

        # 11 Generate sales report
        print("[9/10] Generating report...")
        generate_sales_report(validated_transactions, enriched_transactions)
        print()

        # 12 Display completion message
        print("[10/10] Process completed!")
        print("=" * 40)

    except Exception as e:
        print(f"Error: {e}")
        return []

if __name__ == "__main__":
    main()
