from pathlib import Path
from fpdf import FPDF
import random
from datetime import datetime, timedelta

OUTPUT_DIR = Path("data/input_pdfs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

CLIENTS = ["ACME LTD", "Blue Systems", "NorthTech", "Delta Group", "Sigma Retail"]
ITEMS = ["Keyboard", "Monitor", "Chair", "Desk", "Laptop", "Mouse"]

LAYOUTS = ["A", "B", "C"]

def random_date():
    start = datetime(2025, 1, 1)
    return start + timedelta(days=random.randint(1, 365))

def generate_invoice(idx: int):
    invoice_number = random.randint(100000, 999999)
    po_number = random.randint(100000, 999999)
    client = random.choice(CLIENTS)

    qty1 = random.randint(1, 5)
    qty2 = random.randint(1, 5)
    price1 = random.randint(50, 500)
    price2 = random.randint(50, 500)

    subtotal = qty1 * price1 + qty2 * price2
    tax = round(subtotal * 0.2, 2)
    total = round(subtotal + tax, 2)

    invoice_date = random_date()
    due_date = invoice_date + timedelta(days=14)

    layout = random.choice(LAYOUTS)
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    if layout == "A":
        pdf.multi_cell(0, 8, f"""
INVOICE #{invoice_number}
Client: {client}
Invoice Date: {invoice_date.strftime('%b %d, %Y')}
Due Date: {due_date.strftime('%b %d, %Y')}
PO Number: {po_number}

Item 1: {qty1} x ${price1}
Item 2: {qty2} x ${price2}

Subtotal: ${subtotal:.2f}
Tax: ${tax:.2f}
Total: ${total:.2f}
""")

    elif layout == "B":
        pdf.multi_cell(0, 8, f"""
{client}

Invoice Number {invoice_number}
PO {po_number}

{subtotal:.2f} Subtotal
{tax:.2f} Tax
{total:.2f} Total

Dates:
{invoice_date.strftime('%B %d, %Y')}
{due_date.strftime('%B %d, %Y')}
""")

    else:
        pdf.multi_cell(0, 8, f"""
BILL TO: {client}

#{invoice_number}
PO Number: {po_number}

Invoice Date : {invoice_date.strftime('%Y-%m-%d')}
Due Date : {due_date.strftime('%Y-%m-%d')}

TOTALS
Subtotal ${subtotal:.2f}
Tax ${tax:.2f}
Total ${total:.2f}
""")

    path = OUTPUT_DIR / f"invoice_{idx}.pdf"
    pdf.output(str(path))


if __name__ == "__main__":
    for i in range(1, 51):
        generate_invoice(i)

    print("✅ Generated 50 invoices")
