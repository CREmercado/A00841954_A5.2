"""Program to compute total sales from catalogue and sales records

This program reads a price catalogue and a sales record from JSON files,
computes the cost for all sales, and generates a detailed report.
It includes error handling for file operations and data validation.


Example:
    Basic usage from command line:
        $ python computeSales.py priceCatalogue.json salesRecord.json

Author: A00841954 Christian Erick Mercado Flores
Date: February 2026
"""

import json
import sys
import time

def load_json_file(filename):
    try:
        # Open file with UTF-8 encoding for international character support
        with open(filename, 'r', encoding='utf-8') as file:
            # Parse JSON data from file
            data = json.load(file)
            return data
    except (FileNotFoundError, json.JSONDecodeError, OSError) as e:
        # Report error to user and return None to indicate failure
        print(f"Error reading '{filename}': {e}")
        return None

def create_price_catalogue(catalogue_data):
    # Initialize empty dictionary for price mappings
    price_map = {}

    # Validate that input is a list
    if not isinstance(catalogue_data, list):
        print("Error: Catalogue data is not a list.")
        return price_map

    # Process each item in the catalogue
    for idx, item in enumerate(catalogue_data):
        # Validate item is a dictionary
        if not isinstance(item, dict):
            print(
                f"Warning: Item {idx} in catalogue is not a dictionary. "
                "Skipping."
            )
            continue

        # Extract title and price fields
        title = item.get('title')
        price = item.get('price')

        # Validate title field exists
        if title is None:
            print(f"Warning: Item {idx} missing 'title' field. Skipping.")
            continue

        # Validate price field exists
        if price is None:
            print(
                f"Warning: Item '{title}' missing 'price' field. Skipping.")
            continue

        # Attempt to convert price to float
        try:
            price = float(price)
            # Add valid entry to price map
            price_map[title] = price
        except (ValueError, TypeError):
            # Report conversion error and skip this item
            print(f"Warning: Invalid price for '{title}'. Skipping.")
            continue

    return price_map

def compute_sales(sales_data, price_catalogue):
    """Compute total sales cost from sales records and price catalogue.

    This function processes all sales records, validates each entry,
    looks up prices from the catalogue, and calculates costs. It handles
    various error conditions gracefully and continues processing valid
    records even when some records are invalid.

    Validation performed on each sale record:
        - Record must be a dictionary
        - Must have 'Product' and 'Quantity' fields
        - Quantity must be convertible to integer
        - Product must exist in price catalogue

    Args:
        sales_data (list): List of sale record dictionaries. Each record
            should contain 'SALE_ID', 'SALE_Date', 'Product', and
            'Quantity' fields.
        price_catalogue (dict): Dictionary mapping product names to prices,
            as created by create_price_catalogue().

    Returns:
        tuple: A 2-tuple containing:
            - total_cost (float): Sum of all valid sales costs
            - sales_details (list): List of dictionaries containing detailed
              information about each valid sale (sale_id, date, product,
              quantity, unit_price, sales_cost)

    Example:
        >>> catalogue = {'Apple': 1.50, 'Orange': 2.00}
        >>> sales = [{'Product': 'Apple', 'Quantity': 3}]
        >>> total, details = compute_sales(sales, catalogue)
        >>> total
        4.5
    """
    # Initialize accumulator for total cost
    total_cost = 0.0
    # Initialize list to store detailed sale information
    sales_details = []

    # Validate that sales data is a list
    if not isinstance(sales_data, list):
        print("Error: Sales data is not a list.")
        return total_cost, sales_details

    # Process each sale record
    for idx, sale in enumerate(sales_data):
        # Validate record is a dictionary
        if not isinstance(sale, dict):
            print(f"Warning: Sale record {idx} is not a dictionary. Skipping.")
            continue

        # Extract required fields from sale record
        product = sale.get('Product')
        quantity = sale.get('Quantity')
        # Extract optional fields with defaults
        sale_id = sale.get('SALE_ID', 'N/A')
        sale_date = sale.get('SALE_Date', 'N/A')

        # Validate product field exists
        if product is None:
            print(
                f"Warning: Sale record {idx} missing 'Product' field. "
                "Skipping."
            )
            continue

        # Validate quantity field exists
        if quantity is None:
            print(
                f"Warning: Sale record {idx} missing 'Quantity' field. "
                "Skipping."
            )
            continue

        # Attempt to convert quantity to integer
        try:
            quantity = int(quantity)
        except (ValueError, TypeError):
            print(
                f"Warning: Invalid quantity for sale {idx}. "
                "Skipping."
            )
            continue

        # Verify product exists in catalogue
        if product not in price_catalogue:
            print(
                f"Warning: Product '{product}' not found in catalogue. "
                "Skipping."
            )
            continue

        # Look up unit price from catalogue
        unit_price = price_catalogue[product]
        # Calculate cost for this sale (price × quantity)
        sales_cost = unit_price * quantity
        # Add to running total
        total_cost += sales_cost

        # Store detailed information about this sale
        sales_details.append({
            'sale_id': sale_id,
            'date': sale_date,
            'product': product,
            'quantity': quantity,
            'unit_price': unit_price,
            'sales_cost': sales_cost
        })

    return total_cost, sales_details

def main():
    # Validate correct number of command line arguments
    if len(sys.argv) != 3:
        print(
            "Usage: python computeSales.py "
            "priceCatalogue.json salesRecord.json"
        )
        sys.exit(1)

    # Store file paths in dictionary for easy access
    files = {}
    files['soruce_file'] = sys.argv[0]  # Program name
    files['catalogue_file'] = sys.argv[1]  # Price catalogue path
    files['sales_file'] = sys.argv[2]  # Sales records path

    # Display startup message
    print("")
    print("Starting sales computation...")
    print("")

    # Record start time for performance measurement
    start_time = time.time()

    # Load price catalogue from JSON file
    catalogue_data = load_json_file(files['catalogue_file'])
    if catalogue_data is None:
        # Critical error: cannot proceed without catalogue
        print("Failed to load price catalogue. Exiting.")
        sys.exit(1)

    # Build price lookup dictionary from catalogue
    price_catalogue = create_price_catalogue(catalogue_data)
    print(f"Loaded {len(price_catalogue)} products from catalogue...")
    print("")

    # Process all sales and compute totals
    total_cost, sales_details = compute_sales(sales_data, price_catalogue)
    print(f"Processed {len(sales_details)} valid sales records...")
    print("")

# Standard Python idiom to execute main() when script is run directly
if __name__ == "__main__":
    main()
