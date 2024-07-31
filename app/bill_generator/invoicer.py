from prettytable import PrettyTable


# Define a function to create a bill with custom parameters
def generate_bill(company_info, client_info, items, terms_conditions):
    # Create the header table
    header = PrettyTable()
    header.field_names = ["Logo", company_info['name']]
    header.add_row(["", f"Address: {company_info['address']}"])
    header.add_row(["", f"Mob: {company_info['phone']}"])
    header.align = "l"

    # Create the client info table
    client = PrettyTable()
    client.field_names = [client_info['name'], f"Sr. No.: {client_info['sr_no']}"]
    client.add_row([client_info['address'], f"Date: {client_info['date']}"])
    client.add_row([f"Party GSTIN No.: {client_info['gstin']}", f"P.O. No.: {client_info['po_no']}"])
    client.add_row([f"State: {client_info['state']}", f"P.O. Date: {client_info['po_date']}"])
    client.add_row([f"State Code: {client_info['state_code']}", ""])
    client.align = "l"

    # Create the items table
    items_table = PrettyTable()
    items_table.field_names = ["DESCRIPTION OF GOODS", "HSN CODE", "QTY.", "RATE (Rs.)", "AMOUNT"]
    total_amount = 0
    for item in items:
        items_table.add_row(
            [item['description'], item['hsn_code'], item['qty'], f"{item['rate']:.2f}", f"{item['amount']:.2f}"])
        total_amount += item['amount']

    # Calculate taxes and total
    cgst = sgst = total_amount * 0.09
    total_tax = cgst + sgst
    grand_total = total_amount + total_tax

    items_table.add_row(["", "", "", "TOTAL", f"{total_amount:.2f}"])
    items_table.add_row(["", "", "", "CGST 9%", f"{cgst:.2f}"])
    items_table.add_row(["", "", "", "SGST 9%", f"{sgst:.2f}"])
    items_table.add_row(["", "", "", "TOTAL TAX", f"{total_tax:.2f}"])
    items_table.add_row(["", "", "", "Grand Total", f"{grand_total:.2f}"])
    items_table.align = "l"

    # Convert total to words
    total_in_words = "Ten thousand two hundred fifty one only."  # Placeholder for conversion function

    # Print the bill
    print(header)
    print(client)
    print(items_table)
    print(f"\nRupees In Words: {total_in_words}\n")

    # Print terms and conditions
    print("Terms and Conditions:")
    for i, term in enumerate(terms_conditions, 1):
        print(f"{i}. {term}")

    print("\nFor: MUSKAN ENGINEERS")
    print("\nAuth. Signature")


# Custom parameters
company_info = {
    'name': 'MUSKAN ENGINEERS',
    'address': 'H.No-458, Gali No-1/13B, Basai Enclave, Gurgaon Haryana 122001',
    'phone': '+91 8588837212'
}

client_info = {
    'name': 'M/s. Rohini van Merchandania Ltd.',
    'address': 'Gurgaon',
    'gstin': '06AAACR0000R1Z2',
    'state': 'Haryana',
    'state_code': '06',
    'sr_no': '201',
    'date': '15/06/2023',
    'po_no': '1010000032',
    'po_date': ''
}

items = [
    {'description': 'PSV Toyota', 'hsn_code': '9988', 'qty': 1, 'rate': 4069.00, 'amount': 4069.00},
    {'description': 'JMB', 'hsn_code': '8410', 'qty': 1, 'rate': 4620.00, 'amount': 4620.00}
]

terms_conditions = [
    "Goods once sold will not be taken back.",
    "Interest @24% per annum will be charged on bill paid after 15 days.",
    "We are not responsible for any shortage, breakage, damage, and pilferage.",
    "All disputes subject to Gurgaon courts only."
]

# Generate the bill
generate_bill(company_info, client_info, items, terms_conditions)
