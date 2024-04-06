from num2words import num2words
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image


def add_signature(story):
    """Add a note about the digital signature to the PDF."""
    styles = getSampleStyleSheet()
    signature_note = Paragraph(f"Signature __________________________", styles['Normal'])
    story.append(signature_note)


def generate_invoice(buyer_details, seller_details, items):
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
    styles.add(ParagraphStyle(name='Normal_CENTER3',
                              alignment=TA_CENTER,
                              leading=15
                              ))
    styles.add(ParagraphStyle(name='Seller_Details',
                              fontSize=8
                              ))

    # Adjust table column widths here
    colWidths = [0.4 * inch, 3.4 * inch, 0.6 * inch, 0.6 * inch, 0.7 * inch, 0.8 * inch, 0.5 * inch]
    colWidths2 = [0.4 * inch, 3.4 * inch, 0.6 * inch, 0.6 * inch, 0.7 * inch, 1.3 * inch]

    header2_data = [

        [[Paragraph(f"<b>REG NO. : 06EGAPK9506B1ZQ</b>", styles['Normal_LEFT'])],
         [Paragraph(f"<b><u>TAX INVOICE</u></b>", styles['Normal_CENTER2'])],
         [Paragraph(f"<b>Mob.: +91 858837212</b>", styles['Normal_RIGHT'])],
         ]

    ]
    header2_table = Table(header2_data, colWidths=[7 * inch / 3, 7 * inch / 3, 7 * inch / 3])
    header2_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(header2_table)

    header1_data = [
        [Paragraph(f"<b>MUSKAN ENGINEERS</b>", styles['Normal_CENTER'])],
        [Paragraph(f"<font size=8>Address. H.No.-458,Gali No.-1/13B, Basai Enclave, Gurgaon Haryana 122001</font>",
                   styles['Normal_CENTER2'])],

    ]
    header1_table = Table(header1_data, colWidths=[7 * inch])
    header1_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
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
        ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
    ]))
    story.append(header_table)

    # Items table
    item_data2 = [

        [[Paragraph(f"<b>Sr.No.</b>", styles['Normal_CENTER2'])],
         [Paragraph(f"<b>Description Of Goods</b>", styles['Normal_CENTER2'])],
         [Paragraph(f"<b>HSN Code</b>", styles['Normal_CENTER2'])],
         [Paragraph(f"<b>Qty.</b>", styles['Normal_CENTER2'])],
         [Paragraph(f"<b>Rate</b><br/><font size=8>(Rs.)</font>", styles['Normal_CENTER2'])],
         [Paragraph(f"<b>Amount</b><br/><font size=8>Rs._____________P.</font>", styles['Normal_CENTER2'])]

         ]

    ]

    items_table = Table(item_data2, colWidths=colWidths2)
    items_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('VALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    story.append(items_table)

    total_before_tax = 0
    total_sgst = total_cgst = 0
    c = 1

    for item in items:
        price = item['price']
        qty = item['quantity']
        hsn = item['hsn']
        amt_before_tax = price * qty
        sgst = cgst = amt_before_tax * 0.09  # SGST and CGST at 9%
        total_after_gst = amt_before_tax + sgst + cgst

        total_before_tax += amt_before_tax
        total_sgst += sgst
        total_cgst += cgst

        item_data = ([

            [[Paragraph(f"{c}", styles['Normal_CENTER2'])],
             [Paragraph(f"{item['name']}", styles['Normal_CENTER2'])],
             [Paragraph(f"{hsn}", styles['Normal_CENTER2'])],
             [Paragraph(f"{qty}", styles['Normal_CENTER2'])],
             [Paragraph(f"{price}", styles['Normal_CENTER2'])],
             [Paragraph(f"{amt_before_tax}", styles['Normal_CENTER2'])],
             [Paragraph(f"{"{:.2f}".format(amt_before_tax - int(amt_before_tax))}", styles['Normal_CENTER2'])]

             ],

        ])
        items_table = Table(item_data, colWidths=colWidths)
        items_table.setStyle(TableStyle([
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER')
        ]))
        story.append(items_table)
        c = c + 1

    total_tax = total_sgst + total_cgst
    grand_total = total_before_tax + total_sgst + total_cgst

    # Total in words
    total_in_words = num2words(grand_total, to='currency', lang='en')

    item_data = (

        [[Paragraph(f"Total (in words): {total_in_words.capitalize()}.", styles['Normal_CENTER3'])],
         [[Paragraph(f"Total", styles['Normal_CENTER3'])],
          [[Paragraph(f"CGST____9%", styles['Normal_CENTER3'])],
           [[Paragraph(f"SGST____9%", styles['Normal_CENTER3'])],
            [[Paragraph(f"IGST____N/A", styles['Normal_CENTER3'])],
             [[Paragraph(f"Total Tax", styles['Normal_CENTER3'])],
              [Paragraph(f"Grand Total", styles['Normal_CENTER3'])], ]]]]],
         [[Paragraph(f"{total_before_tax}", styles['Normal_CENTER3'])],
          [[Paragraph(f"{total_cgst}", styles['Normal_CENTER3'])],
           [[Paragraph(f"{total_sgst}", styles['Normal_CENTER3'])],
            [[Paragraph(f"---", styles['Normal_CENTER3'])],
             [[Paragraph(f"{total_tax}", styles['Normal_CENTER3'])],
              [Paragraph(f"{grand_total}", styles['Normal_CENTER3'])]]]]]],
         [[Paragraph(f"{"{:.2f}".format(total_before_tax - int(total_before_tax))}", styles['Normal_CENTER3'])],
          [[Paragraph(f"{"{:.2f}".format(total_cgst - int(total_cgst))}", styles['Normal_CENTER3'])],
           [[Paragraph(f"{"{:.2f}".format(total_sgst - int(total_sgst))}", styles['Normal_CENTER3'])],
            [[Paragraph(f"---", styles['Normal_CENTER3'])],
             [[Paragraph(f"{"{:.2f}".format(total_tax - int(total_tax))}", styles['Normal_CENTER3'])],
              [[Paragraph(f"{"{:.2f}".format(grand_total - int(grand_total))}",
                          styles['Normal_CENTER3'])]]]]]]],

         ],

    )

    items_table = Table(item_data, colWidths=[4.4 * inch, 1.3 * inch, 0.8 * inch, 0.5 * inch])
    items_table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'CENTER')
    ]))
    story.append(items_table)
    story.append(Spacer(1, 12))

    # Digital Signature
    add_signature(story)

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
    {"name": "Item 1", "price": 1000.0, "quantity": 2, "hsn": 24},
    {"name": "Item 2", "price": 500.0, "quantity": 3, "hsn": 87},
    {"name": "Item 3", "price": 500.0, "quantity": 4, "hsn": 20},
    {"name": "Item 4", "price": 900.0, "quantity": 1, "hsn": 8},
    {"name": "Item 5", "price": 700.0, "quantity": 2, "hsn": 23},
    {"name": "Item 6", "price": 1200.0, "quantity": 3, "hsn": 42}
]

generate_invoice(buyer_details, seller_details, items)
