from num2words import num2words
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer


def add_signature(story, signature_name):
    """Add a note about the digital signature to the PDF."""
    styles = getSampleStyleSheet()
    signature_note = Paragraph(f"This document is digitally signed by {signature_name}.", styles['Normal'])
    story.append(signature_note)


def generate_invoice(buyer_details, seller_details, items, bill_no, bill_date, signature_name):
    doc = SimpleDocTemplate("invoice.pdf", pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(name='Normal_LEFT',
                              alignment=TA_LEFT,
                              ))
    styles.add(ParagraphStyle(name='Normal_RIGHT',
                              alignment=TA_RIGHT,
                              ))
    styles.add(ParagraphStyle(name='Normal_CENTER',
                              alignment=TA_CENTER,
                              fontSize=20,
                              leading=15
                              ))
    styles.add(ParagraphStyle(name='Normal_CENTER2',
                              alignment=TA_CENTER,
                              ))
    styles.add(ParagraphStyle(name='Seller_Details',
                              fontSize=8
                              ))

    # Adjust table column widths here
    colWidths = [1.45 * inch, 0.75 * inch, 0.6 * inch, 1.2 * inch, 0.9 * inch, 0.9 * inch, 1.2 * inch]

    header1_data = [
        [Paragraph(f"<b>REG NO. : 06EGAPK9506B1ZQ</b>")],
        [Paragraph(f"<b>MUSKAN ENGINEERS</b>", styles['Normal_CENTER'])],
        [Paragraph(f"<font size=8>Address. H.No.-458,Gali No.-1/13B, Basai Enclave, Gurgaon Haryana 122001</font>",
                   styles['Normal_CENTER2'])]

    ]
    header1_table = Table(header1_data, colWidths=[7 * inch, 1 * inch])
    header1_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(header1_table)

    # Header
    header_data = [

        [[Paragraph(
            f"<b>Buyer:</b><br/>{buyer_details['company_name']}<br/>GST: {buyer_details['gst_no']}<br/>{buyer_details['address']}",
            styles['Normal_LEFT'])],
            [Paragraph(
                f"<b>Sr.No.: </b><u>{seller_details['sr_no']}</u><br/><b>Date: </b><u>{seller_details['date']}</u><br/><b>P.O. No.: </b><u>{seller_details['po_no']}</u><br/><b>P.O. Date: </b><u>{seller_details['po_date']}</u>",
                styles['Seller_Details'])]
        ],

    ]
    header_table = Table(header_data, colWidths=[5.5 * inch, 1.5 * inch])
    header_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(header_table)

    # Items table
    item_data = [['Item', 'Price', 'Qty', 'Amt Before Tax', 'SGST (9%)', 'CGST (9%)', 'Total After GST']]
    total_before_tax = 0
    total_sgst = total_cgst = 0

    for item in items:
        price = item['price']
        qty = item['quantity']
        amt_before_tax = price * qty
        sgst = cgst = amt_before_tax * 0.09  # SGST and CGST at 9%
        total_after_gst = amt_before_tax + sgst + cgst

        total_before_tax += amt_before_tax
        total_sgst += sgst
        total_cgst += cgst

        item_data.append([item['name'], f"{price:.2f}", qty, f"{amt_before_tax:.2f}", f"{sgst:.2f}", f"{cgst:.2f}",
                          f"{total_after_gst:.2f}"])

    grand_total = total_before_tax + total_sgst + total_cgst
    item_data.append(["", "", "", "", "", "Grand Total", f"{grand_total:.2f}"])

    items_table = Table(item_data, colWidths=colWidths)
    items_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
    ]))
    story.append(items_table)
    story.append(Spacer(1, 12))

    # Total in words
    total_in_words = num2words(grand_total, to='currency', lang='en')
    story.append(Paragraph(f"Total (in words): {total_in_words.capitalize()}.", styles['Normal']))
    story.append(Spacer(1, 12))

    # Digital Signature
    add_signature(story, signature_name)

    doc.build(story)


# Example usage
buyer_details = {
    "gst_no": "27AAACI1122G1Z6",
    "address": "Buyer Address, City, State, Zip",
    "company_name": "Buyer Company Pvt Ltd"
}

seller_details = {
    "sr_no": 23,
    "date": "04-04-2024",
    "po_no": 4200412,
    "po_date": "14-04-2024"
}

items = [
    {"name": "Item 1", "price": 1000.0, "quantity": 2},
    {"name": "Item 2", "price": 500.0, "quantity": 3},
    {"name": "Item 3", "price": 500.0, "quantity": 4},
    {"name": "Item 4", "price": 900.0, "quantity": 1},
    {"name": "Item 5", "price": 700.0, "quantity": 2},
    {"name": "Item 6", "price": 1200.0, "quantity": 3}
]

generate_invoice(buyer_details, seller_details, items, "123456", "2024-04-03", "User XYZ")
