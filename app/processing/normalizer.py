from datetime import datetime
from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)


def parse_float(value):
    if value is None:
        return None
    try:
        return float(value.replace(",", ""))
    except Exception:
        logger.warning(f"Failed to parse float: {value}")
        return None


def parse_date(value):
    if value is None:
        return None

    for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%m/%d/%Y"):
        try:
            return datetime.strptime(value, fmt).date()
        except ValueError:
            continue

    logger.warning(f"Failed to parse date: {value}")
    return None


def normalize_records(records):
    normalized = []

    for record in records:
        clean = {
            "source_file": record["source_file"],
            "invoice_number": record["invoice_number"],
            "invoice_date": parse_date(record["invoice_date"]),
            "client_name": record["client_name"],
            "subtotal": parse_float(record["subtotal"]),
            "tax": parse_float(record["tax"]),
            "total": parse_float(record["total"]),
        }

        normalized.append(clean)

    logger.info(f"Normalized {len(normalized)} records")
    return normalized
