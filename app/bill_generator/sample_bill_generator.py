from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image

bill_data = {
    'bill_number': '123456',
    'date': '2024-05-29',
    'buyer': {
        'name': 'Buyer Name',
        'address': 'Buyer Address Line',
        'contact': 'Buyer Contact Info'
    },
    'supplier': {
        'name': 'Supplier Name',
        'address': 'Supplier Address Line',
        'contact': 'Supplier Contact Info'
    },
    'items': [
        {'name': 'Item 1', 'quantity': 2, 'price': 10},
        {'name': 'Item 2', 'quantity': 1, 'price': 20},
        # Add more items to test multiple pages
        {'name': 'Item 3', 'quantity': 5, 'price': 30},
        {'name': 'Item 4', 'quantity': 3, 'price': 15},
        {'name': 'Item 5', 'quantity': 4, 'price': 25},
        {'name': 'Item 6', 'quantity': 2, 'price': 18},
        {'name': 'Item 7', 'quantity': 1, 'price': 50},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        {'name': 'Item 8', 'quantity': 6, 'price': 60},
        # ... more items
    ],
    'total_amount': 228  # Update this according to the items
}


def generate_invoice(bill, file_name):
    canvas_a4 = canvas.Canvas(file_name, pagesize=A4)

    def draw_header(canvas_object):
        # Company details
        canvas_object.setFont("Helvetica-Bold", 14)
        canvas_object.drawString(1 * inch, 10.75 * inch, "Company Name")
        canvas_object.setFont("Helvetica", 12)
        canvas_object.drawString(1 * inch, 10.5 * inch, "Company Address Line 1")
        canvas_object.drawString(1 * inch, 10.3 * inch, "Company Address Line 2")
        canvas_object.drawString(1 * inch, 10.1 * inch, "Company City, State, ZIP")
        canvas_object.drawString(1 * inch, 9.9 * inch, "Company Contact Info")

        # Company Logo
        try:
            logo = Image.open("Muskan_Engineers_Logo.png")
            canvas_object.drawInlineImage(logo, 6 * inch, 10.25 * inch, 1 * inch, 1 * inch)
        except IOError:
            print("Logo not found.")

        # Bill details
        canvas_object.setFont("Helvetica-Bold", 12)
        canvas_object.drawString(1 * inch, 9.5 * inch, f"Bill Number: {bill['bill_number']}")
        canvas_object.drawString(1 * inch, 9.3 * inch, f"Date: {bill['date']}")

        # Buyer details
        canvas_object.setFont("Helvetica-Bold", 12)
        canvas_object.drawString(1 * inch, 8.9 * inch, "Buyer Details:")
        canvas_object.setFont("Helvetica", 12)
        canvas_object.drawString(1 * inch, 8.7 * inch, f"Name: {bill['buyer']['name']}")
        canvas_object.drawString(1 * inch, 8.5 * inch, f"Address: {bill['buyer']['address']}")
        canvas_object.drawString(1 * inch, 8.3 * inch, f"Contact: {bill['buyer']['contact']}")

        # Supplier details
        canvas_object.setFont("Helvetica-Bold", 12)
        canvas_object.drawString(1 * inch, 7.9 * inch, "Supplier Details:")
        canvas_object.setFont("Helvetica", 12)
        canvas_object.drawString(1 * inch, 7.7 * inch, f"Name: {bill['supplier']['name']}")
        canvas_object.drawString(1 * inch, 7.5 * inch, f"Address: {bill['supplier']['address']}")
        canvas_object.drawString(1 * inch, 7.3 * inch, f"Contact: {bill['supplier']['contact']}")

    def draw_footer(canvas_object):
        canvas_object.setFont("Helvetica", 10)
        canvas_object.drawString(1 * inch, 0.5 * inch, "Thank you for your business!")
        canvas_object.drawString(1 * inch, 0.3 * inch, "Page %d" % canvas_object.getPageNumber())

    # page_pointer -> pointer of the cursor on the current page
    def draw_items(canvas_object, page_pointer, items):
        canvas_object.setFont("Helvetica", 10)
        for item in items:
            if page_pointer < 1.5 * inch:  # Adjusted to leave space for footer
                canvas_object.showPage()
                draw_header(canvas_object)
                draw_footer(canvas_object)
                page_pointer = 7 * inch  # Start drawing items below the details on the new page
            canvas_object.drawString(1 * inch, page_pointer, f"{item['name']} - {item['quantity']} x ${item['price']}")
            page_pointer -= 0.2 * inch
        return page_pointer

    # Start generating the PDF
    draw_header(canvas_a4)
    cursor_pointer = 7 * inch  # Start items below the details section

    # Add items to the invoice, handle multiple pages
    cursor_pointer = draw_items(canvas_a4, cursor_pointer, bill['items'])

    # Add total amount at the bottom of the last page
    if cursor_pointer < 1.5 * inch:
        canvas_a4.showPage()
        draw_header(canvas_a4)
        draw_footer(canvas_a4)
        cursor_pointer = 7 * inch  # Start below details section on the new page
    canvas_a4.drawString(1 * inch, cursor_pointer, f"Total Amount: ${bill['total_amount']}")

    draw_footer(canvas_a4)
    canvas_a4.save()


filename = f"bill_{bill_data['bill_number']}.pdf"

if __name__ == "__main__":
    generate_invoice(bill_data, filename)
