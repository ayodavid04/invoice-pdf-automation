import re

from numpy import record
from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)

DATE_FALLBACK_REGEX = r"([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})"
CURRENCY_REGEX = r"\$?([\d,]+\.\d{2})"


def apply_fallbacks(records):
    validated = []

    for record in records:
        text = record["full_text"]

        # ---- Date fallback ----
        
        if not record.get("subtotal"):
            m = re.search(r"subtotal\s*[:\-]?\s*\$?([\d,]+\.\d{2})", text, re.I)
        if m:
            record["subtotal"] = m.group(1)
            record["subtotal_confidence"] = "FALLBACK"

        if not record.get("tax"):
            m = re.search(r"tax\s*[:\-]?\s*\$?([\d,]+\.\d{2})", text, re.I)
            if m:
                record["tax"] = m.group(1)
                record["tax_confidence"] = "FALLBACK"
        if not record.get("total"):
            m = re.search(r"total\s*[:\-]?\s*\$?([\d,]+\.\d{2})", text, re.I)
            if m:
                record["total"] = m.group(1)
                record["total_confidence"] = "FALLBACK"
                
        # ---- Currency fallback ----
        missing_money = any(
            not record.get(k) for k in ("subtotal", "tax", "total")
        )

        if missing_money:
            values = re.findall(CURRENCY_REGEX, text)

            if len(values) >= 3:
                record.setdefault("subtotal", values[-3])
                record.setdefault("tax", values[-2])
                record.setdefault("total", values[-1])

                logger.info(f"{record['source_file']} -> inferred monetary values")

        # cleanup
        record.pop("full_text", None)

        validated.append(record)

    return validated
