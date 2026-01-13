from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime, timedelta
import random

OUTPUT_DIR = Path("data/input_pdfs")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

NUM_INVOICES = 50
TAX_RATE = 0.20


def random_date():
    start = datetime(2025, 1, 1)
    end = datetime(2025, 12, 1)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))


def generate_invoice(index: int):
    invoice_date = random_date()
    due_date = invoice_date + timedelta(days=14)

    subtotal = round(random.uniform(100, 5000), 2)
    tax = round(subtotal * TAX_RATE, 2)
    total = round(subtotal + tax, 2)

    filename = OUTPUT_DIR / f"invoice_{index:03}.pdf"
    c = canvas.Canvas(str(filename), pagesize=A4)

    y = 800
    line_height = 22

    def write(text):
        nonlocal y
        c.drawString(50, y, text)
        y -= line_height

    write("INVOICE")
    write("-----------------------------")
    write(f"Invoice Number: INV-{index:05}")
    write(f"Invoice Date: {invoice_date.strftime('%Y-%m-%d')}")
    write(f"Due Date: {due_date.strftime('%Y-%m-%d')}")
    write("")
    write("Bill To: Example Company Ltd")
    write("")
    write(f"Subtotal: ${subtotal:.2f}")
    write(f"Tax: ${tax:.2f}")
    write(f"Total: ${total:.2f}")

    c.save()
    print(f"Generated -> {filename}")


if __name__ == "__main__":
    for i in range(1, NUM_INVOICES + 1):
        generate_invoice(i)

    print("Invoice generation complete.")
