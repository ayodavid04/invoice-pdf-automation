import pandas as pd
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger()


def build_analytics_dataset(records: list[dict]) -> pd.DataFrame:
    """
    Converts validated invoice records into an analytics-ready DataFrame.
    """

    df = pd.DataFrame(records)

    # -------------------------
    # Type casting
    # -------------------------
    money_cols = ["subtotal", "tax", "total"]

    for col in money_cols:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .astype(float)
        )

    # -------------------------
    # Date parsing
    # -------------------------
    df["invoice_date"] = pd.to_datetime(
        df["invoice_date"], errors="coerce"
    )
    df["due_date"] = pd.to_datetime(
        df["due_date"], errors="coerce"
    )

    # -------------------------
    # Derived fields
    # -------------------------
    df["invoice_month"] = df["invoice_date"].dt.to_period("M").astype(str)

    df["days_to_due"] = (
        df["due_date"] - df["invoice_date"]
    ).dt.days

    df["is_overdue"] = df["days_to_due"] < 0

    logger.info("Analytics dataset built")

    return df
