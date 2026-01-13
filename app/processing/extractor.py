import re
from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)

MONEY = r"\$?\s*([\d,]+\.\d{2})"

INVOICE_PATTERNS = {
    "invoice_number": [
        r"#\s*(\d{5,})",
        r"Invoice\s*(?:Number)?\s*(\d{5,})",
    ],
    "po_number": [
        r"PO\s*(?:Number)?[:\s]*(\d{5,})",
    ],
    "client_name": [
        r"Client[:\s]+([A-Za-z0-9 .&]+)",
        r"BILL TO[:\s]+([A-Za-z0-9 .&]+)",
        r"^([A-Z][A-Za-z0-9 .&]+)\n",   # top header fallback
    ],
    "invoice_date": [
        r"Invoice Date[:\s]*([A-Za-z0-9 ,\-]+)",
    ],
    "due_date": [
        r"Due Date[:\s]*([A-Za-z0-9 ,\-]+)",
    ],
    "subtotal": [
        rf"Subtotal[:\s]*{MONEY}",
        rf"{MONEY}\s*Subtotal",
    ],
    "tax": [
        rf"Tax[:\s]*{MONEY}",
        rf"{MONEY}\s*Tax",
    ],
    "total": [
        rf"Total[:\s]*{MONEY}",
        rf"{MONEY}\s*Total",
    ],
}

DATE_FALLBACK_REGEX = r"([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4}|\d{4}-\d{2}-\d{2})"
CURRENCY_FALLBACK = r"\$?\s*([\d,]+\.\d{2})"


def extract_field(text: str, patterns: list[str]):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip(), "EXACT"
    return None, "MISSING"


def extract_fields(parsed_pdfs):
    results = []

    for pdf in parsed_pdfs:
        full_text = "\n".join(pdf["pages"])

        record = {
            "source_file": pdf["path"].name,
            "full_text": full_text,
        }

        # ---------- Primary Extraction ----------
        for field, patterns in INVOICE_PATTERNS.items():
            value, confidence = extract_field(full_text, patterns)
            record[field] = value
            record[f"{field}_confidence"] = confidence

            if value:
                logger.info(f"{pdf['path'].name} -> {field}: {value}")
            else:
                logger.warning(f"{pdf['path'].name} -> Missing {field}")

        # ---------- Date Fallback ----------
        dates = re.findall(DATE_FALLBACK_REGEX, full_text)

        if not record["invoice_date"] and len(dates) >= 1:
            record["invoice_date"] = dates[0]
            record["invoice_date_confidence"] = "FALLBACK"

        if not record["due_date"] and len(dates) >= 2:
            record["due_date"] = dates[1]
            record["due_date_confidence"] = "FALLBACK"

        # ---------- Money Fallback ----------
        if not (record["subtotal"] and record["tax"] and record["total"]):
            values = re.findall(CURRENCY_FALLBACK, full_text)

            if len(values) >= 3:
                record.setdefault("subtotal", values[-3])
                record.setdefault("tax", values[-2])
                record.setdefault("total", values[-1])

                record.setdefault("subtotal_confidence", "FALLBACK")
                record.setdefault("tax_confidence", "FALLBACK")
                record.setdefault("total_confidence", "FALLBACK")

                logger.info(f"{pdf['path'].name} -> inferred monetary values")

        results.append(record)

    return results
