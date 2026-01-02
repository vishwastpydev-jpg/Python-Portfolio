from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

# 1. Collect User Details
print("--- PDF Receipt Generator ---")
name = input("Enter Customer Name: ")
date = input("Enter Date (DD/MM/YYYY): ")
product_name = input("Enter Product/Course Name: ")
sub_duration = input("Enter Subscription (e.g., Lifetime, 6 Months): ")
price = float(input("Enter Price (Numeric only, e.g., 10999): "))
discount = float(input("Enter Discount (Numeric only, e.g., 3000): "))

total = price - discount

# 2. Prepare the Data Array
DATA = [
    ["Date", "Name", "Subscription", "Price (Rs.)"],
    [date, product_name, sub_duration, f"{price:,.2f}"],
    ["Sub Total", "", "", f"{price:,.2f}"],
    ["Discount", "", "", f"-{discount:,.2f}"],
    ["Total", "", "", f"{total:,.2f}"],
]

# 3. Setup PDF Basics
pdf = SimpleDocTemplate("receipt.pdf", pagesize=A4)
styles = getSampleStyleSheet()
title_style = styles["Heading1"]
title_style.alignment = 1  # Center
title = Paragraph(f"Receipt for {name}", title_style)

# 4. Create Advanced Table Style
# We use SPAN to merge the "Total" label across the first 3 columns
style = TableStyle([
    ("BOX", (0, 0), (-1, -1), 1, colors.black),
    ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ("BACKGROUND", (0, 0), (-1, 0), colors.cadetblue), # Header color
    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
    ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
    
    # Merge cells for the Sub-Total, Discount, and Total rows
    ("SPAN", (0, 2), (2, 2)),
    ("SPAN", (0, 3), (2, 3)),
    ("SPAN", (0, 4), (2, 4)),
    
    # Align the "Total" labels to the right for a professional look
    ("ALIGN", (0, 2), (0, 4), "RIGHT"),
    ("FONTNAME", (0, 4), (-1, 4), "Helvetica-Bold"), # Make Total Row Bold
])

# 5. Build the PDF
# colWidths helps ensure the "Name" column doesn't wrap awkwardly
table = Table(DATA, style=style, colWidths=[80, 220, 100, 100])
pdf.build([title, table])

print("\nSuccess! 'receipt.pdf' has been generated.")