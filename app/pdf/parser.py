import re
from pathlib import Path
from app.utils.logger import setup_logger
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

logger = setup_logger(Settings.LOG_LEVEL)


def extract_text(loaded_pdfs):
    """
    Takes loaded PDFs and extracts text from each page.
    Returns:
        [
            {
                "path": Path,
                "pages": [str, str, ...]
            }
        ]
    """
    extracted = []

    for pdf in loaded_pdfs:
        text_pages = []

        for idx, page in enumerate(pdf["reader"].pages):
            try:
                text = page.extract_text() or ""
                logger.info(
                    f"Extracted text from {pdf['path'].name} page {idx + 1}"
                )
                text_pages.append(text)

            except Exception as e:
                logger.error(
                    f"Failed extracting page {idx + 1} from {pdf['path'].name}: {e}"
                )

        extracted.append({
            "path": pdf["path"],
            "pages": text_pages,
        })

        logger.info(
            f"{pdf['path'].name} extracted {len(text_pages)} pages of text"
        )

    return extracted