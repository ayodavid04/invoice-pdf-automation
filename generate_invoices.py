import random
from pathlib import Path
from datetime import datetime, timedelta
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

OUTPUT_DIR = Path("input")
OUTPUT_DIR.mkdir(exist_ok=True)

COMPANIES = ["ACME LTD", "SYM LTD", "NOVA TECH", "ORBIT GROUP", "ZENITH INC"]
ITEMS = ["Hoodie", "Jeans", "Shoes", "Jacket", "Bag"]

def random_date():
    start = datetime(2025, 1, 1)
    return start + timedelta(days=random.randint(1, 365))

def generate_invoice_pdf(i: int):
    invoice_no = random.randint(100000, 999999)
    po_no = random.randint(500000, 999999)
    client = random.choice(COMPANIES)

    issue_date = random_date()
    due_date = issue_date + timedelta(days=random.randint(7, 30))

    subtotal = round(random.uniform(20, 500), 2)
    tax = round(subtotal * 0.2, 2)
    total = round(subtotal + tax, 2)

    filename = OUTPUT_DIR / f"invoice_{i}.pdf"
    c = canvas.Canvas(str(filename), pagesize=A4)

    y = 800

    # ----- Random layout selection -----
    layout = random.choice([1, 2, 3])

    if layout == 1:
        c.drawString(50, y, f"# {invoice_no}")
        y -= 30
        c.drawString(50, y, f"Bill To:")
        y -= 20
        c.drawString(50, y, client)
        y -= 30
        c.drawString(50, y, f"Date: {issue_date.strftime('%b %d, %Y')}")
        y -= 20
        c.drawString(50, y, f"Due Date: {due_date.strftime('%b %d, %Y')}")
        y -= 30
        c.drawString(50, y, f"PO Number: {po_no}")
        y -= 40
        c.drawString(50, y, f"Subtotal: ${subtotal}")
        y -= 20
        c.drawString(50, y, f"Tax: ${tax}")
        y -= 20
        c.drawString(50, y, f"Total: ${total}")

    elif layout == 2:
        c.drawString(50, y, f"Invoice Number: {invoice_no}")
        y -= 25
        c.drawString(50, y, f"Customer: {client}")
        y -= 25
        c.drawString(50, y, f"{issue_date.strftime('%b %d, %Y')}")
        y -= 20
        c.drawString(50, y, f"{due_date.strftime('%b %d, %Y')}")
        y -= 25
        c.drawString(50, y, f"{po_no}")
        y -= 40
        c.drawString(50, y, f"${subtotal} Subtotal")
        y -= 20
        c.drawString(50, y, f"${tax} Tax")
        y -= 20
        c.drawString(50, y, f"${total} Total")

    else:
        # messy layout on purpose
        c.drawString(300, y, f"# {invoice_no}")
        y -= 20
        c.drawString(50, y, f"{client}")
        y -= 20
        c.drawString(300, y, f"PO Number {po_no}")
        y -= 20
        c.drawString(50, y, f"Issued {issue_date.strftime('%b %d, %Y')}")
        y -= 20
        c.drawString(50, y, f"Pay By {due_date.strftime('%b %d, %Y')}")
        y -= 40
        c.drawString(50, y, f"Subtotal ${subtotal}")
        y -= 20
        c.drawString(50, y, f"Tax ${tax}")
        y -= 20
        c.drawString(50, y, f"Total ${total}")

    c.save()
    print(f"Generated {filename.name}")

if __name__ == "__main__":
    for i in range(1, 51):
        generate_invoice_pdf(i)
