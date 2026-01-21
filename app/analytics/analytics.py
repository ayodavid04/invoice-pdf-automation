import pandas as pd
from pathlib import Path
from app.utils.logger import get_logger

logger = get_logger()

OUTPUT_DIR = Path("data/analytics")
OUTPUT_FILE = OUTPUT_DIR / "invoices_locked.csv"


def build_analytics_dataset(records: list[dict]) -> pd.DataFrame:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.DataFrame(records)

    # ---- Type coercion ----
    money_cols = ["subtotal", "tax", "total"]
    for col in money_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
    df["due_date"] = pd.to_datetime(df["due_date"], errors="coerce")

    # ---- Analytics flags ----
    df["computed_total"] = df["subtotal"] + df["tax"]
    df["total_mismatch"] = (df["computed_total"] - df["total"]).abs() > 0.01

    df["has_all_required_fields"] = (
        df["invoice_number"].notna()
        & df["client_name"].notna()
        & df["invoice_date"].notna()
        & df["total"].notna()
    )

    # ---- Persist LOCKED dataset ----
    df.to_csv(OUTPUT_FILE, index=False)

    logger.info(f"Locked analytics dataset written to {OUTPUT_FILE}")
    logger.info(f"Rows: {len(df)} | Mismatches: {df['total_mismatch'].sum()}")

    return df

