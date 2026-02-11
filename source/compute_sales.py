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

# Standard Python idiom to execute main() when script is run directly
if __name__ == "__main__":
    main()
