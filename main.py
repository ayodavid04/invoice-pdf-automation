from pathlib import Path
import pandas as pd

from app.core.pipeline import run_pipeline
from app.processing.normalizer import normalize_records
from app.utils.logger import get_logger
from app.config.settings import Settings
from app.db.writer import insert_invoices

logger = get_logger()


def main():
    logger.info("Application starting")

    # ✅ SINGLE SOURCE OF TRUTH
    input_dir = Path(Settings.INPUT_PDF_DIR)

    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")

    logger.info(f"Input directory: {input_dir}")

    # -------- Run pipeline --------
    extracted_records = run_pipeline(input_dir)
    logger.info(f"Extracted {len(extracted_records)} invoices")

    # -------- Normalize --------
    normalized_records = normalize_records(extracted_records)
    df = pd.DataFrame(normalized_records)

    logger.info(f"Normalized DataFrame rows: {len(df)}")
    logger.info(f"\n{df.head()}")

    # -------- INSERT INTO POSTGRES --------
    insert_invoices(normalized_records)
    logger.info("✅ Data inserted into Postgres")

    # -------- Save CSV (LOCKED DATASET) --------
    output_dir = Path("data/output")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_csv = output_dir / "locked_invoices.csv"
    df.to_csv(output_csv, index=False)

    logger.info(f"✅ Locked dataset written to {output_csv}")


if __name__ == "__main__":
    main()
