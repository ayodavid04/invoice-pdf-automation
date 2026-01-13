from pathlib import Path
import pandas as pd

from app.core.pipeline import run_pipeline
from app.processing.normalizer import normalize_records
from app.utils.logger import setup_logger
from app.config.settings import Settings


def main():
    logger = setup_logger(Settings.LOG_LEVEL)
    logger.info("Application starting")

    input_dir = Path(Settings.INPUT_PDF_DIR)

    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        return

    logger.info(f"Input directory: {input_dir}")

    # -------- Run pipeline --------
    extracted_records = run_pipeline(input_dir)

    logger.info(f"Extracted structured data for {len(extracted_records)} invoices")

    # -------- Normalize --------
    normalized_records = normalize_records(extracted_records)

    df = pd.DataFrame(normalized_records)
    logger.info(f"DataFrame created with {len(df)} rows")
    logger.info(f"\n{df.head()}")

    # Optional exports (enable when ready)
    # from app.output.csv_writer import write_csv
    # from app.output.excel_writer import write_excel
    # write_csv(df)
    # write_excel(df)


if __name__ == "__main__":
    main()
