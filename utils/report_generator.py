from datetime import datetime


def generate_sales_report(transactions, enriched_transactions, output_file='output/sales_report.txt'):
    """
    Generates a comprehensive formatted text report

    report must include (in this order):

    1. HEADER
       - Report title
       - Generation date and time
       - Total records processed

    2. OVERALL SUMMARY
       - Total revenue (formatted with commas)
       - Total transactions
       - Average order value
       - Date range of data

    3. REGION-WISE PERFORMANCE
       - Table showing each region with:
         * Total sales amount
         * Percentage of total
         * Transaction count
       - Sorted by sales amount descending

    4. TOP 5 PRODUCTS
       - Table with columns: rank, product name, quantity sold, revenue

    5. TOP 5 CUSTOMERS
       - Table with columns: rank, customer id, total spent, order count

    6. DAILY SALES TREND
       - Table showing: date, revenue, transactions, unique customers

    7. PRODUCT PERFORMANCE ANALYSIS
       - Best selling day
       - Low performing products (if any)
       - Average transaction value per region

    8. API ENRICHMENT SUMMARY
       - Total products enriched
       - Success rate percentage
       - List of products that couldn't be enriched
    """

    try:
        # calculate all required metrics
        total_revenue = 0.0
        total_transactions = len(transactions)

        if total_transactions == 0:
            print("- No transactions to report")
            return

        for t in transactions:
            amount = t['Quantity'] * t['UnitPrice']
            total_revenue += amount

        avg_order_value = total_revenue / total_transactions if total_transactions > 0 else 0.0

        # get date range
        dates = sorted([t['Date'] for t in transactions])
        date_range_start = dates[0] if dates else "N/A"
        date_range_end = dates[-1] if dates else "N/A"

        # region-wise analysis
        region_stats = {}
        for t in transactions:
            region = t['Region']
            amount = t['Quantity'] * t['UnitPrice']

            if region not in region_stats:
                region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}

            region_stats[region]['total_sales'] += amount
            region_stats[region]['transaction_count'] += 1

        # product analysis
        product_stats = {}
        for t in transactions:
            p_name = t['ProductName']
            qty = t['Quantity']
            revenue = qty * t['UnitPrice']

            if p_name not in product_stats:
                product_stats[p_name] = {'total_qty': 0, 'total_revenue': 0.0}

            product_stats[p_name]['total_qty'] += qty
            product_stats[p_name]['total_revenue'] += revenue

        top_products = sorted(
            [(name, data['total_qty'], data['total_revenue']) for name, data in product_stats.items()],
            key=lambda x: x[2],
            reverse=True
        )[:5]

        # customer analysis
        customer_stats = {}
        for t in transactions:
            c_id = t['CustomerID']
            amount = t['Quantity'] * t['UnitPrice']

            if c_id not in customer_stats:
                customer_stats[c_id] = {'total_spent': 0.0, 'purchase_count': 0}

            customer_stats[c_id]['total_spent'] += amount
            customer_stats[c_id]['purchase_count'] += 1

        top_customers = sorted(
            [(c_id, data['total_spent'], data['purchase_count']) for c_id, data in customer_stats.items()],
            key=lambda x: x[1],
            reverse=True
        )[:5]

        # daily sales trend
        daily_stats = {}
        for t in transactions:
            date = t['Date']
            amount = t['Quantity'] * t['UnitPrice']
            c_id = t['CustomerID']

            if date not in daily_stats:
                daily_stats[date] = {'revenue': 0.0, 'transaction_count': 0, 'customers_set': set()}

            daily_stats[date]['revenue'] += amount
            daily_stats[date]['transaction_count'] += 1
            daily_stats[date]['customers_set'].add(c_id)

        sorted_dates = sorted(daily_stats.keys())

        # peak sales day
        peak_date = None
        max_revenue = -1.0
        for date, stats in daily_stats.items():
            if stats['revenue'] > max_revenue:
                max_revenue = stats['revenue']
                peak_date = date

        # low performing products
        low_products = [(name, data['total_qty'], data['total_revenue'])
                       for name, data in product_stats.items() if data['total_qty'] < 10]
        low_products = sorted(low_products, key=lambda x: x[1])

        # api enrichment analysis
        api_enriched_count = sum(1 for t in enriched_transactions if t.get('API_Match', False))
        total_enriched = len(enriched_transactions)
        enrichment_rate = (api_enriched_count / total_enriched * 100) if total_enriched > 0 else 0.0

        unenriched_products = [t['ProductName'] for t in enriched_transactions if not t.get('API_Match', False)]
        unenriched_products = list(set(unenriched_products))  # unique products

        # build report content
        report_lines = []

        # header
        report_lines.append("=" * 50)
        report_lines.append(" " * 10 + "SALES ANALYTICS REPORT")
        report_lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append(f"Records Processed: {total_transactions}")
        report_lines.append("=" * 50)
        report_lines.append("")

        # overall summary
        report_lines.append("OVERALL SUMMARY")
        report_lines.append("-" * 50)
        report_lines.append(f"Total Revenue:        ₹{total_revenue:,.2f}")
        report_lines.append(f"Total Transactions:   {total_transactions}")
        report_lines.append(f"Average Order Value:  ₹{avg_order_value:,.2f}")
        report_lines.append(f"Date Range:           {date_range_start} to {date_range_end}")
        report_lines.append("")

        # region-wise performance
        report_lines.append("REGION-WISE PERFORMANCE")
        report_lines.append("-" * 50)
        report_lines.append(f"{'Region':<15} {'Sales':<20} {'% of Total':<15} {'Transactions':<10}")
        report_lines.append("-" * 50)

        sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True)
        for region, stats in sorted_regions:
            sales = stats['total_sales']
            percentage = (sales / total_revenue * 100) if total_revenue > 0 else 0.0
            count = stats['transaction_count']
            report_lines.append(f"{region:<15} ₹{sales:>17,.2f}  {percentage:>6.2f}%      {count:>6}")
        report_lines.append("")

        # top 5 products
        report_lines.append("TOP 5 PRODUCTS")
        report_lines.append("-" * 50)
        report_lines.append(f"{'Rank':<6} {'Product Name':<25} {'Quantity':<10} {'Revenue':<15}")
        report_lines.append("-" * 50)

        for idx, (product, qty, revenue) in enumerate(top_products, 1):
            report_lines.append(f"{idx:<6} {product:<25} {qty:<10} ₹{revenue:>12,.2f}")
        report_lines.append("")

        # top 5 customers
        report_lines.append("TOP 5 CUSTOMERS")
        report_lines.append("-" * 50)
        report_lines.append(f"{'Rank':<6} {'Customer ID':<15} {'Total Spent':<20} {'Order Count':<10}")
        report_lines.append("-" * 50)

        for idx, (c_id, total_spent, order_count) in enumerate(top_customers, 1):
            report_lines.append(f"{idx:<6} {c_id:<15} ₹{total_spent:>17,.2f}  {order_count:>6}")
        report_lines.append("")

        # daily sales trend
        report_lines.append("DAILY SALES TREND")
        report_lines.append("-" * 50)
        report_lines.append(f"{'Date':<15} {'Revenue':<20} {'Transactions':<15} {'Unique Customers':<15}")
        report_lines.append("-" * 50)

        for date in sorted_dates:
            stats = daily_stats[date]
            revenue = stats['revenue']
            count = stats['transaction_count']
            customers = len(stats['customers_set'])
            report_lines.append(f"{date:<15} ₹{revenue:>17,.2f}  {count:>6}           {customers:>6}")
        report_lines.append("")

        # product performance analysis
        report_lines.append("PRODUCT PERFORMANCE ANALYSIS")
        report_lines.append("-" * 50)
        report_lines.append(f"Best Selling Day: {peak_date} with revenue ₹{max_revenue:,.2f}")
        report_lines.append("")

        if low_products:
            report_lines.append("Low Performing Products (< 10 units):")
            for product, qty, revenue in low_products:
                report_lines.append(f"  - {product}: {qty} units - ₹{revenue:,.2f}")
        else:
            report_lines.append("No low performing products found")

        report_lines.append("")
        report_lines.append("Average Transaction Value Per Region:")
        for region in sorted(region_stats.keys()):
            stats = region_stats[region]
            avg_value = stats['total_sales'] / stats['transaction_count'] if stats['transaction_count'] > 0 else 0.0
            report_lines.append(f"  - {region}: ₹{avg_value:,.2f}")
        report_lines.append("")

        # api enrichment summary
        report_lines.append("API ENRICHMENT SUMMARY")
        report_lines.append("-" * 50)
        report_lines.append(f"Total Products Enriched: {api_enriched_count}/{total_enriched}")
        report_lines.append(f"Success Rate: {enrichment_rate:.2f}%")

        if unenriched_products:
            report_lines.append(f"Unenriched Products ({len(unenriched_products)}):")
            for product in unenriched_products:
                report_lines.append(f"  - {product}")
        else:
            report_lines.append("All Products Successfully Enriched")

        report_lines.append("")
        report_lines.append("=" * 50)
        report_lines.append("END OF REPORT")
        report_lines.append("=" * 50)

        # write to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(report_lines))

        print(f"✓ Sales Report Generated: {output_file}")

    except Exception as e:
        print(f"✗ Error Generating Report: {e}")
