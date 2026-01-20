import requests

def fetch_all_products():
    """
    Fetches all products from DummyJSON API

    Returns: list of product dictionaries
    """
    url = "https://dummyjson.com/products?limit=100"

    try:
        print(f"   > Connecting to {url}...")
        response = requests.get(url, timeout=10)

        # check if the request was successful (status code 200)
        response.raise_for_status()

        data = response.json()

        # the API returns a dictionary with a products key containing the list
        if 'products' in data:
            products = data['products']
            print(f"   ✓ Successfully fetched {len(products)} products from API")

            return products
        else:
            print("   - API returned data but no 'products' key found.")
            return []

    except requests.exceptions.ConnectionError:
        print("Network Error: Could not connect to the API. Check your internet.")
        return []
    except requests.exceptions.Timeout:
        print("Timeout Error: The API took too long to respond.")
        return []
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return []

def create_product_mapping(api_products):
    """
    Creates a mapping of product IDs to product info

    Parameters: api_products from fetch_all_products()

    Returns: dictionary mapping product IDs to info
    """
    mapping = {}

    for p in api_products:
        p_id = p.get('id')

        # only add if ID exists
        if p_id is not None:
            mapping[p_id] = {
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'rating': p.get('rating')
            }

    return mapping

import re

def enrich_sales_data(transactions, product_mapping):
    """
    Enriches transaction data with API product information
    """
    enriched_data = []

    for t in transactions:
        # create a copy so we don't mess up original data
        new_t = t.copy()

        # safely get ProductID (default to empty string if missing)
        p_id_str = new_t.get('ProductID', '')

        # extract numeric ID using regex
        match = re.search(r'\d+', str(p_id_str))

        api_match = False
        if match:
            numeric_id = int(match.group())

            # check if this ID exists in our API data
            if numeric_id in product_mapping:
                api_info = product_mapping[numeric_id]

                new_t['API_Category'] = api_info['category']
                new_t['API_Brand'] = api_info['brand']
                new_t['API_Rating'] = api_info['rating']
                api_match = True

        # if no match found, fill with None/False
        if not api_match:
            new_t['API_Category'] = None
            new_t['API_Brand'] = None
            new_t['API_Rating'] = None

        new_t['API_Match'] = api_match
        enriched_data.append(new_t)

    return enriched_data

def save_enriched_data(enriched_transactions, filename='data/enriched_sales_data.txt'):
    """
    Saves enriched transactions back to file with pipe delimiter
    """
    if not enriched_transactions:
        print("- No enriched data to save.")
        return

    # define the exact column order required
    headers = [
        'TransactionID', 'Date', 'ProductID', 'ProductName',
        'Quantity', 'UnitPrice', 'CustomerID', 'Region',
        'API_Category', 'API_Brand', 'API_Rating', 'API_Match'
    ]

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            # 1. Write Header (Pipe delimited)
            f.write("|".join(headers) + "\n")

            # 2. write Rows
            for t in enriched_transactions:
                row_values = []
                for field in headers:
                    val = t.get(field)

                    # handle None values (convert to string 'None' or empty)
                    if val is None:
                        row_values.append('None')
                    else:
                        row_values.append(str(val))

                f.write("|".join(row_values) + "\n")

        print(f"✓ Enriched data saved to: {filename}")

    except Exception as e:
        print(f"- Error saving enriched data: {e}")
