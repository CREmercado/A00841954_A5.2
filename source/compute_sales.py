"""Program to compute total sales from catalogue and sales records

This program reads a price catalogue and a sales record from JSON files,
computes the cost for all sales, and generates a detailed report.
It includes error handling for file operations and data validation.

Features:
    - Loads and parses JSON files for catalogue and sales records
    - Creates a price mapping from the catalogue
    - Computes total sales cost based on the sales records and price mapping
    - Formats the output report with details of each sale and total cost

Example:
    Basic usage from command line:
        $ python compute_sales.py priceCatalogue.json salesRecord.json

Author: A00841954 Christian Erick Mercado Flores
Date: February 2026
"""

import json
import sys
import time
from datetime import datetime


def load_json_file(filename):
    """Load and parse a JSON file with comprehensive error handling.

    This function attempts to open and parse a JSON file, handling common
    errors such as missing files. All errors are caught and reported.

    Args:
        filename (str): Path to the JSON file to be loaded. Can be either
            an absolute or relative path.

    Returns:
        list or dict or None: Parsed JSON data structure (typically a list
            or dictionary), or None if any error occurs during file reading
            or JSON parsing.

    Example:
        >>> data = load_json_file('catalogue.json')
        >>> if data is not None:
        ...     print(f"Loaded {len(data)} items")
    """
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
    """Create a dictionary mapping product titles to their prices.

    This function processes the raw catalogue data and builds an efficient
    lookup dictionary for price queries. It validates each product entry
    and skips invalid items while reporting warnings to the user.

    Args:
        catalogue_data (list): List of product dictionaries from the JSON
            catalogue file. Each dictionary should contain at minimum
            'title' and 'price' keys.

    Returns:
        dict: Dictionary mapping product titles (str) to prices (float).
            Returns empty dict if catalogue_data is invalid or not a list.

    Example:
        >>> catalogue = [{'title': 'Apple', 'price': 1.50}]
        >>> prices = create_price_catalogue(catalogue)
        >>> prices['Apple']
        1.5
    """
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
    looks up prices from the catalogue, and calculates costs.

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


def format_output(sales_details, total_cost, elapsed_time, files):
    """Format the sales report output with headers, data, and summary.

    This function creates a human-readable report containing all sales
    details, metadata about the execution, and summary statistics.

    The report includes:
        - Execution timestamp
        - Source files used
        - Detailed table of all sales
        - Total sales cost
        - Execution time

    Args:
        sales_details (list): List of dictionaries containing sale details
            as returned by compute_sales().
        total_cost (float): Total cost of all sales.
        elapsed_time (float): Time in seconds taken to execute the program.
        files (dict): Dictionary containing file paths with keys:
            'soruce_file', 'catalogue_file', 'sales_file'.

    Returns:
        str: Formatted multi-line string containing the complete report,
            ready to be printed or saved to a file.

    Example:
        >>> details = [{'sale_id': 1, 'product': 'Apple', ...}]
        >>> report = format_output(details, 100.50, 0.025, {...})
        >>> print(report)
    """
    # Generate timestamp for this execution
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Initialize list to store output lines
    lines = []

    # Add report header with decorative separator
    lines.append("=" * 80)
    lines.append("SALES REPORT")
    lines.append("=" * 80)

    # Add metadata section with execution details
    lines.append(f"Timestamp: {timestamp}")
    lines.append(f"Source File: {files['soruce_file']}")
    lines.append(f"Price Catalogue File: {files['catalogue_file']}")
    lines.append(f"Sales Record File: {files['sales_file']}")
    lines.append("=" * 80)

    # Check if there are any valid sales to display
    if not sales_details:
        lines.append("No valid sales records found.")
    else:
        # Add table header with column names
        lines.append(
            f"{'Sales ID':<10} {'Date':<10} {'Product':<30} "
            f"{'Qty':<4} {'Price':<10} {'Sale Cost':<10}"
        )
        # Add separator line under header
        lines.append("-" * 80)

        # Add a row for each sale with aligned columns
        for detail in sales_details:
            lines.append(
                f"{str(detail['sale_id']):<10} "
                f"{detail['date']:<10} "
                f"{detail['product']:<30} "
                f"{detail['quantity']:<4} "
                f"${detail['unit_price']:<9.2f} "
                f"${detail['sales_cost']:<9.2f}"
            )

    # Add report footer with summary statistics
    lines.append("=" * 80)
    lines.append(f"TOTAL SALES COST: ${total_cost:.2f}")
    lines.append(f"Execution time: {elapsed_time:.4f} seconds")
    lines.append("=" * 80 + "\n")

    # Join all lines with newlines and return complete report
    return "\n".join(lines)


def save_results(output_text, filename):
    """Save the formatted results to a text file.

    This function appends the results to a file, creating the file if it
    doesn't exist.

    Args:
        output_text (str): The formatted report text to save.
        filename (str): Path to the output file. Parent directories must
            already exist.

    Returns:
        None

    Example:
        >>> save_results("Report content...", "results/output.txt")
        Results saved to 'results/output.txt'
    """
    try:
        # Open file in append mode with UTF-8 encoding
        with open(filename, 'a', encoding='utf-8') as file:
            # Write the complete report to file
            file.write(output_text)
        # Confirm successful save to user
        print(f"\nResults saved to '{filename}'")
    except OSError as e:
        # Report any I/O errors to user
        print(f"Error saving results to file: {e}")


def main():
    """Execute the main sales computation workflow.

    This is the main entry point for the program. It orchestrates all
    operations in the correct sequence:
        1. Validate command line arguments
        2. Load input files
        3. Process catalogue and sales data
        4. Compute results
        5. Format and display output
        6. Save results to file

    The function handles errors at each step and exits gracefully if
    critical errors occur (e.g., missing input files).

    Command Line Arguments:
        argv[1]: Path to price catalogue JSON file
        argv[2]: Path to sales record JSON file

    Returns:
        None (exits with sys.exit() on error)

    Exit Codes:
        0: Successful execution
        1: Invalid arguments or critical error

    Example:
        $ python computeSales.py catalogue.json sales.json
    """
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

    # Load sales records from JSON file
    sales_data = load_json_file(files['sales_file'])
    if sales_data is None:
        # Critical error: cannot proceed without sales data
        print("Failed to load sales records. Exiting.")
        sys.exit(1)

    # Build price lookup dictionary from catalogue
    price_catalogue = create_price_catalogue(catalogue_data)
    print(f"Loaded {len(price_catalogue)} products from catalogue...")
    print("")

    # Process all sales and compute totals
    total_cost, sales_details = compute_sales(sales_data, price_catalogue)
    print(f"Processed {len(sales_details)} valid sales records...")
    print("")

    # Record end time and calculate elapsed time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Generate formatted report
    output_text = format_output(sales_details, total_cost, elapsed_time, files)
    # Display report to console
    print(output_text)

    # Save report to file for record keeping
    output_filename = "results/SalesResults.txt"
    save_results(output_text, output_filename)


# Standard Python idiom to execute main() when script is run directly
if __name__ == "__main__":
    main()
