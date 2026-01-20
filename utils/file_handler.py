import os

def read_sales_data(filename):
    """
    Reads sales data file, handling encoding issues
    Returns: list of raw lines (strings)
    """
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        return []

    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []
    read_success = False

    for enc in encodings:
        try:
            with open(filename, 'r', encoding=enc) as f:
                lines = f.readlines()
            read_success = True
            break
        except UnicodeDecodeError:
            continue
        except Exception as e:
            print(f"Error reading file: {e}")
            return []

    if not read_success:
        print("Error: Could not read file with supported encodings.")
        return []

    # remove empty lines and strip whitespace
    cleaned_lines = [l.strip() for l in lines if l.strip()]

    # skip the header row
    if len(cleaned_lines) > 0:
        return cleaned_lines[1:]

    return []

def parse_transactions(raw_lines):
    """
    Parses raw lines into clean list of dictionaries

    Returns: list of dictionaries with keys:
    ['TransactionID', 'Date', 'ProductID', 'ProductName',
     'Quantity', 'UnitPrice', 'CustomerID', 'Region']
    """
    cleaned_data = []

    for line in raw_lines:
        # split by pipe delimiter |
        parts = line.strip().split('|')

        # skip rows with incorrect number of fields (must be 8)
        if len(parts) != 8:
            continue

        # unpack the list into variables for easier handling
        t_id, date, p_id, p_name, qty_str, price_str, c_id, region = parts

        try:
            # handle commas within ProductName
            clean_p_name = p_name.replace(',', '')

            # handle commas in numeric fields & Convert types (string to numeric)
            # Remove commas first, then convert
            qty = int(qty_str.replace(',', ''))
            unit_price = float(price_str.replace(',', ''))

            # Create the dictionary
            transaction = {
                'TransactionID': t_id,
                'Date': date,
                'ProductID': p_id,
                'ProductName': clean_p_name,
                'Quantity': qty,
                'UnitPrice': unit_price,
                'CustomerID': c_id,
                'Region': region
            }

            cleaned_data.append(transaction)

        except ValueError:
            # if conversion to numeric fails skip iteration
            continue

    return cleaned_data

def validate_and_filter(transactions, region=None, min_amount=None, max_amount=None):
    """
    Validates transactions and applies optional filters

    Parameters:
    - transactions: list of transaction dictionaries
    - region: filter by specific region (optional)
    - min_amount: minimum transaction amount (Quantity * UnitPrice) (optional)
    - max_amount: maximum transaction amount (optional)

    Returns tuple (valid_transactions, invalid_count, filter_summary)
    """

    # initialize counters
    total_input = len(transactions)
    valid_transactions = []
    invalid_count = 0

    # validate transaction rules
    for t in transactions:
        try:
            # check for empty or missing values
            if not all(t.values()):
                invalid_count += 1
                continue

            # check numeric positivity
            if t['Quantity'] <= 0 or t['UnitPrice'] <= 0:
                invalid_count += 1
                continue

            # check id formats
            if not t['TransactionID'].startswith('T'):
                invalid_count += 1
                continue
            if not t['ProductID'].startswith('P'):
                invalid_count += 1
                continue
            if not t['CustomerID'].startswith('C'):
                invalid_count += 1
                continue

            # if all checks pass, add to valid list
            valid_transactions.append(t)

        except (KeyError, AttributeError, TypeError):
            # catch any structural errors
            invalid_count += 1
            continue

    # calculate statistics for user display
    if valid_transactions:
        # get unique regions
        available_regions = sorted(list(set(t['Region'] for t in valid_transactions)))

        # calculate amounts
        amounts = [t['Quantity'] * t['UnitPrice'] for t in valid_transactions]
        min_avail = min(amounts)
        max_avail = max(amounts)

        # print available options to user
        print("\n--- Available filter options ---")
        print(f"Regions: {', '.join(available_regions)}")
        print(f"Transaction Amount Range: {min_avail} to {max_avail}")
        print("--------------------------------")

    # apply filters
    filtered_list = valid_transactions
    initial_valid_count = len(valid_transactions)

    # filter by region
    if region:
        filtered_list = [t for t in filtered_list if t['Region'] == region]

    count_after_region = len(filtered_list)
    removed_by_region = initial_valid_count - count_after_region

    # filter by amount range
    final_list = []
    for t in filtered_list:
        amount = t['Quantity'] * t['UnitPrice']
        if min_amount is not None and amount < min_amount:
            continue
        if max_amount is not None and amount > max_amount:
            continue
        final_list.append(t)

    count_after_amount = len(final_list)
    removed_by_amount = count_after_region - count_after_amount

    # create summary dictionary
    filter_summary = {
        'total_input': total_input,
        'invalid': invalid_count,
        'filtered_by_region': removed_by_region,
        'filtered_by_amount': removed_by_amount,
        'final_count': count_after_amount
    }
    # print EXACT output format required
    print(f"Total records parsed: {total_input}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records after cleaning: {len(valid_transactions)}")

    return final_list, invalid_count, filter_summary

