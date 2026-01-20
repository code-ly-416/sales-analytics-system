# ------------------------------------SALES SUMMARY CALCULATOR----------------------------

def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions

    Returns: float (total revenue)
    """

    # initialize total
    total_revenue = 0.0

    # loop through transactions and sum up quantity * price
    for t in transactions:
        amount = t['Quantity'] * t['UnitPrice']
        total_revenue += amount

    return total_revenue

def region_wise_sales(transactions):
    """
    Analyzes sales by region

    Returns: dictionary with region statistics
    """

    # dictionary to store raw totals first
    region_stats = {}
    total_revenue_all = 0.0

    # first pass: aggregate sales and counts
    for t in transactions:
        region = t['Region']
        amount = t['Quantity'] * t['UnitPrice']

        if region not in region_stats:
            region_stats[region] = {'total_sales': 0.0, 'transaction_count': 0}

        region_stats[region]['total_sales'] += amount
        region_stats[region]['transaction_count'] += 1
        total_revenue_all += amount

    # second pass: calculate percentages and format final output
    final_output = {}

    # sort regions by total_sales descending (highest to lowest) lambda function used for sorting
    sorted_regions = sorted(region_stats.items(), key=lambda x: x[1]['total_sales'], reverse=True)

    for region, stats in sorted_regions:
        sales = stats['total_sales']
        count = stats['transaction_count']

        # div/0 check
        if total_revenue_all > 0:
            percentage = (sales / total_revenue_all) * 100
        else:
            percentage = 0.0

        final_output[region] = {
            'total_sales': round(sales, 2),
            'transaction_count': count,
            'percentage': round(percentage, 2)
        }

    return final_output

def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold

    Returns list of tuples
    """

    # dictionary to aggregate product stats
    product_stats = {}

    for t in transactions:
        p_name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']

        if p_name not in product_stats:
            product_stats[p_name] = {'total_qty': 0, 'total_revenue': 0.0}

        product_stats[p_name]['total_qty'] += qty
        product_stats[p_name]['total_revenue'] += revenue

    # convert to list of tuples for sorting items
    # tuple format (ProductName, TotalQuantity, TotalRevenue)
    stats_list = []
    for name, data in product_stats.items():
        stats_list.append((name, data['total_qty'], data['total_revenue']))

    # sort by quantity in descending order
    sorted_products = sorted(stats_list, key=lambda x: x[1], reverse=True)

    # return top n items
    return sorted_products[:n]

def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns

    Returns dictionary of customer statistics
    """

    # dictionary to aggregate raw customer data
    customer_stats = {}

    for t in transactions:
        c_id = t['CustomerID']
        amount = t['Quantity'] * t['UnitPrice']
        p_name = t['ProductName']

        if c_id not in customer_stats:
            customer_stats[c_id] = {
                'total_spent': 0.0,
                'purchase_count': 0,
                'products_set': set()  # to keep products unique (set is unique)
            }

        customer_stats[c_id]['total_spent'] += amount
        customer_stats[c_id]['purchase_count'] += 1
        customer_stats[c_id]['products_set'].add(p_name)

    # sort customers by total_spent descending
    sorted_customers = sorted(customer_stats.items(), key=lambda x: x[1]['total_spent'], reverse=True)

    final_output = {}

    for c_id, stats in sorted_customers:
        spent = stats['total_spent']
        count = stats['purchase_count']

        # calculate average order value
        if count > 0:
            avg_value = spent / count
        else:
            avg_value = 0.0

        final_output[c_id] = {
            'total_spent': round(spent, 2),
            'purchase_count': count,
            'avg_order_value': round(avg_value, 2),
            'products_bought': list(stats['products_set']) # convert set back to list
        }

    return final_output

# ------------------------------------DATE BASED ANALYSIS----------------------------

def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date

    Returns dictionary sorted by date
    """

    # dictionary to aggregate daily stats
    daily_stats = {}

    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']
        c_id = t['CustomerID']

        if date not in daily_stats:
            daily_stats[date] = {
                'revenue': 0.0,
                'transaction_count': 0,
                'customers_set': set() # using set for unique counting
            }

        daily_stats[date]['revenue'] += amount
        daily_stats[date]['transaction_count'] += 1
        daily_stats[date]['customers_set'].add(c_id)

    # sort dates chronologically
    sorted_dates = sorted(daily_stats.keys())

    final_output = {}

    for date in sorted_dates:
        stats = daily_stats[date]

        final_output[date] = {
            'revenue': round(stats['revenue'], 2),
            'transaction_count': stats['transaction_count'],
            'unique_customers': len(stats['customers_set'])
        }

    return final_output

def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue

    Returns tuple (date, revenue, transaction_count)
    """

    # dictionary to store daily totals
    daily_totals = {}

    for t in transactions:
        date = t['Date']
        amount = t['Quantity'] * t['UnitPrice']

        if date not in daily_totals:
            daily_totals[date] = {'revenue': 0.0, 'count': 0}

        daily_totals[date]['revenue'] += amount
        daily_totals[date]['count'] += 1

    # find the day with max revenue
    peak_date = None
    max_revenue = -1.0
    peak_count = 0

    for date, stats in daily_totals.items():
        if stats['revenue'] > max_revenue:
            max_revenue = stats['revenue']
            peak_date = date
            peak_count = stats['count']

    return (peak_date, round(max_revenue, 2), peak_count)

# ------------------------------------PRODUCT PERFORMANCE----------------------------

def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales

    Returns list of tuples
    """

    # dictionary to aggregate product stats
    product_stats = {}

    for t in transactions:
        p_name = t['ProductName']
        qty = t['Quantity']
        revenue = qty * t['UnitPrice']

        if p_name not in product_stats:
            product_stats[p_name] = {'total_qty': 0, 'total_revenue': 0.0}

        product_stats[p_name]['total_qty'] += qty
        product_stats[p_name]['total_revenue'] += revenue

    # filter products below threshold and convert to tuple list
    low_performers = []

    for name, data in product_stats.items():
        qty = data['total_qty']
        if qty < threshold:
            low_performers.append((name, qty, data['total_revenue']))

    # sort by quantity (index 1) in ascending order (lowest first)
    sorted_low_performers = sorted(low_performers, key=lambda x: x[1])

    return sorted_low_performers
