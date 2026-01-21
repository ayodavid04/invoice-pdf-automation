import re
from pathlib import Path
from app.utils.logger import get_logger
from app.config.settings import Settings

CURRENCY_REGEX = r"\$([\d,]+\.\d{2})"

PATTERNS = {
    "subtotal": [
        r"Subtotal\s*[:\-]?\s*\$([\d,]+\.\d{2})",
        r"\$([\d,]+\.\d{2})\s*\n*\s*Subtotal",
    ],
    "tax": [
        r"Tax\s*[:\-]?\s*\$([\d,]+\.\d{2})",
        r"\$([\d,]+\.\d{2})\s*\n*\s*Tax",
    ],
    "total": [
        r"Total\s*[:\-]?\s*\$([\d,]+\.\d{2})",
        r"\$([\d,]+\.\d{2})\s*\n*\s*Total",
    ],
    "invoice_date": [
        r"Invoice Date\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})",
    ],
    "due_date": [
        r"Due Date\s*[:\-]?\s*(\d{4}-\d{2}-\d{2})",
    ],
}


def validate_money(record: dict) -> bool:
    try:
        s = float(record.get("subtotal", 0))
        t = float(record.get("tax", 0))
        total = float(record.get("total", 0))
        return abs((s + t) - total) < 0.05
    except:
        return False


def extract_fields(text: str) -> dict:
    record = {}

    for field, patterns in PATTERNS.items():
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                record[field] = match.group(1)
                break

    # Fallback monetary recovery ONLY if validation fails
    if not validate_money(record):
        values = [
            float(v.replace(",", ""))
            for v in re.findall(CURRENCY_REGEX, text)
        ]

        if len(values) >= 3:
            values.sort()
            subtotal = values[-3]
            tax = values[-2]
            total = values[-1]

            if abs((subtotal + tax) - total) < 0.05:
                record["subtotal"] = f"{subtotal:.2f}"
                record["tax"] = f"{tax:.2f}"
                record["total"] = f"{total:.2f}"

    return record

from app.utils.logger import get_logger

logger = get_logger()


def extract_text(loaded_pdfs):
    extracted = []

    for pdf in loaded_pdfs:
        pages = []

        for page in pdf["reader"].pages:
            pages.append(page.extract_text() or "")

        extracted.append({
            "path": pdf["path"],
            "pages": pages,
        })

    return extracted
