import re
from app.utils.logger import get_logger

logger = get_logger()

CURRENCY_REGEX = r"\$?([\d,]+\.\d{2})"


def _to_float(value):
    try:
        return float(value.replace(",", ""))
    except Exception:
        return None


def apply_fallbacks(records: list[dict]) -> list[dict]:
    validated = []

    for record in records:
        text = record.get("full_text", "")

        # -------- Subtotal --------
        if not record.get("subtotal"):
            m = re.search(r"subtotal\s*[:\-]?\s*\$?([\d,]+\.\d{2})", text, re.I)
            if m:
                record["subtotal"] = m.group(1)

        # -------- Tax --------
        if not record.get("tax"):
            m = re.search(r"tax\s*[:\-]?\s*\$?([\d,]+\.\d{2})", text, re.I)
            if m:
                record["tax"] = m.group(1)

        # -------- Total (extract ONLY) --------
        if not record.get("total"):
            m = re.search(r"total\s*[:\-]?\s*\$?([\d,]+\.\d{2})", text, re.I)
            if m:
                record["total"] = m.group(1)

        # -------- Currency inference (last resort) --------
        missing = any(not record.get(k) for k in ("subtotal", "tax", "total"))
        if missing:
            values = re.findall(CURRENCY_REGEX, text)
            if len(values) >= 3:
                record.setdefault("subtotal", values[-3])
                record.setdefault("tax", values[-2])
                record.setdefault("total", values[-1])
                logger.info(f"{record.get('source_file')} -> inferred monetary values")

        # -------- Correct total ONLY if missing --------
        subtotal = _to_float(record.get("subtotal"))
        tax = _to_float(record.get("tax"))

        if record.get("total") is None and subtotal is not None and tax is not None:
            calculated = round(subtotal + tax, 2)
            record["total"] = f"{calculated:.2f}"
            logger.info(
                f"{record.get('source_file')} -> total computed "
                f"({record['subtotal']} + {record['tax']} = {record['total']})"
            )

        # -------- Cleanup --------
        record.pop("full_text", None)
        validated.append(record)

    return validated
