from pathlib import Path
import pandas as pd

from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)


def ensure_output_dir():
    output_dir = Path(Settings.OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir


def write_csv(df: pd.DataFrame):
    output_dir = ensure_output_dir()
    csv_path = output_dir / "invoices.csv"

    df.to_csv(csv_path, index=False)

    logger.info(f"CSV written to {csv_path}")
    return csv_path
