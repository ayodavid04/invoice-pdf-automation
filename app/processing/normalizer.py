from datetime import datetime
from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)


DATE_FORMATS = [
    "%d/%m/%Y",
    "%Y-%m-%d",
    "%m/%d/%Y",
    "%b %d, %Y",
    "%B %d, %Y",
]


def parse_float(value):
    if value is None:
        return None
    try:
        return float(value.replace(",", "").replace("$", "").strip())
    except Exception:
        logger.warning(f"Failed to parse float: {value}")
        return None


def parse_date(value):
    if value is None:
        return None

    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue

    logger.warning(f"Failed to parse date: {value}")
    return None


def normalize_records(records):
    normalized = []

    for record in records:
        clean = {
            "source_file": record.get("source_file"),

            "invoice_number": record.get("invoice_number"),
            "invoice_number_confidence": record.get("invoice_number_confidence"),

            "po_number": record.get("po_number"),
            "po_number_confidence": record.get("po_number_confidence"),

            "invoice_date": parse_date(record.get("invoice_date")),
            "invoice_date_confidence": record.get("invoice_date_confidence"),

            "due_date": parse_date(record.get("due_date")),
            "due_date_confidence": record.get("due_date_confidence"),

            "client_name": record.get("client_name"),
            "client_name_confidence": record.get("client_name_confidence"),

            "subtotal": parse_float(record.get("subtotal")),
            "subtotal_confidence": record.get("subtotal_confidence"),

            "tax": parse_float(record.get("tax")),
            "tax_confidence": record.get("tax_confidence"),

            "total": parse_float(record.get("total")),
            "total_confidence": record.get("total_confidence"),
        }

        normalized.append(clean)

    logger.info(f"Normalized {len(normalized)} records")
    return normalized
