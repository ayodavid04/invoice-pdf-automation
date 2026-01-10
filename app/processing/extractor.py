import re
from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)


INVOICE_PATTERNS = {
    "invoice_number": r"Invoice\s*#?:?\s*([A-Z0-9\-]+)",
    "invoice_date": r"Date\s*:?[\s]*([0-9\/\-\.]+)",
    "client_name": r"Bill\s*To\s*:?\s*(.+)",
    "subtotal": r"Subtotal\s*\$?([0-9\.,]+)",
    "tax": r"Tax\s*\$?([0-9\.,]+)",
    "total": r"Total\s*\$?([0-9\.,]+)",
}


def extract_fields(parsed_pdfs):
    results = []

    for pdf in parsed_pdfs:
        full_text = "\n".join(pdf["pages"])

        record = {
            "source_file": pdf["path"].name,
        }

        for field, pattern in INVOICE_PATTERNS.items():
            match = re.search(pattern, full_text, re.IGNORECASE)

            if match:
                record[field] = match.group(1).strip()
                logger.info(f"{pdf['path'].name} -> {field}: {record[field]}")
            else:
                record[field] = None
                logger.warning(f"{pdf['path'].name} -> Missing {field}")

        results.append(record)

    return results
