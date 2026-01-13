import re
from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)


INVOICE_PATTERNS = {
    "invoice_number": [
        r"#\s*(\d{4,})",
        r"Invoice\s*(?:Number|#)[:\s]+(\d+)",
    ],
    "po_number": [
        r"PO\s*Number[:\s]+(\d+)",
        r"\n(\d{5,})\n",
    ],
    "invoice_date": [
        r"Date[:\s]+([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})",
    ],
    "due_date": [
        r"Due\s*Date[:\s]+([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})",
    ],
    "client_name": [
        r"Bill To[:\s]*\n([A-Za-z0-9 .&]+)",
        r"Customer[:\s]+([A-Za-z0-9 .&]+)",
    ],
    "subtotal": [
        r"(?i)subtotal\s*[:\-]?\s*\$?\s*([\d,]+\.\d{2})",
        r"\$?\s*([\d,]+\.\d{2})\s*(?:\n|\s)*subtotal",
    ],
    "tax": [
        r"(?i)tax\s*[:\-]?\s*\$?\s*([\d,]+\.\d{2})",
        r"\$?\s*([\d,]+\.\d{2})\s*(?:\n|\s)*tax",
    ],
    "total": [
        r"(?i)total\s*[:\-]?\s*\$?\s*([\d,]+\.\d{2})",
        r"\$?\s*([\d,]+\.\d{2})\s*(?:\n|\s)*total",
    ],
}


def extract_field(text: str, patterns: list[str]):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return {
                "value": match.group(1).strip(),
                "confidence": "EXACT",
                "pattern": pattern,
            }

    return {
        "value": None,
        "confidence": "MISSING",
        "pattern": None,
    }


def extract_fields(parsed_pdfs):
    results = []

    for pdf in parsed_pdfs:
        full_text = "\n".join(pdf["pages"])

        record = {
            "source_file": pdf["path"].name,
            "full_text": full_text,   # keep for validator
        }

        for field, patterns in INVOICE_PATTERNS.items():
            result = extract_field(full_text, patterns)

            record[field] = result["value"]
            record[f"{field}_confidence"] = result["confidence"]
            record[f"{field}_pattern"] = result["pattern"]

            if result["value"]:
                logger.info(
                    f"{pdf['path'].name} -> {field}: {result['value']}"
                )
            else:
                logger.warning(
                    f"{pdf['path'].name} -> Missing {field}"
                )

        results.append(record)

    return results
