import re
from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)

DATE_FALLBACK_REGEX = r"([A-Za-z]{3,9}\s+\d{1,2},\s+\d{4})"
CURRENCY_REGEX = r"\$([\d,]+\.\d{2})"


def apply_fallbacks(records: list[dict]) -> list[dict]:
    """
    Applies fallback extraction logic when primary extraction failed.
    Safe against missing keys and undefined variables.
    """

    for record in records:
        text = record.get("full_text", "")

        if not text:
            logger.warning(
                f"{record.get('source_file')} -> No full_text available for fallback"
            )
            continue

        # -----------------------
        # DATE FALLBACK
        # -----------------------
        if not record.get("invoice_date") or not record.get("due_date"):
            dates = re.findall(DATE_FALLBACK_REGEX, text)

            if len(dates) >= 1 and not record.get("invoice_date"):
                record["invoice_date"] = dates[0]
                record["invoice_date_confidence"] = "FALLBACK"
                logger.info(
                    f"{record['source_file']} -> inferred invoice_date: {dates[0]}"
                )

            if len(dates) >= 2 and not record.get("due_date"):
                record["due_date"] = dates[1]
                record["due_date_confidence"] = "FALLBACK"
                logger.info(
                    f"{record['source_file']} -> inferred due_date: {dates[1]}"
                )

        # -----------------------
        # MONEY FALLBACK
        # -----------------------
        missing_money = any(
            not record.get(k) for k in ("subtotal", "tax", "total")
        )

        if missing_money:
            values = re.findall(CURRENCY_REGEX, text)
            values = [float(v.replace(",", "")) for v in values]

            if len(values) >= 3:
                # Heuristic: last 3 money values usually subtotal / tax / total
                subtotal, tax, total = values[-3], values[-2], values[-1]

                record.setdefault("subtotal", f"{subtotal:.2f}")
                record.setdefault("tax", f"{tax:.2f}")
                record.setdefault("total", f"{total:.2f}")

                record.setdefault("subtotal_confidence", "FALLBACK")
                record.setdefault("tax_confidence", "FALLBACK")
                record.setdefault("total_confidence", "FALLBACK")

                logger.info(
                    f"{record['source_file']} -> inferred monetary values"
                )

        # -----------------------
        # CLEANUP
        # -----------------------
        record.pop("full_text", None)

    return records
