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

        # Check if the request was successful (status code 200)
        response.raise_for_status()

        data = response.json()

        # The API returns a dictionary with a products key containing the list
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

        # Only add if ID exists
        if p_id is not None:
            mapping[p_id] = {
                'title': p.get('title'),
                'category': p.get('category'),
                'brand': p.get('brand'),
                'rating': p.get('rating')
            }

    return mapping


