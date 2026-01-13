from pathlib import Path
from app.pdf.loader import load_pdfs
from app.pdf.parser import extract_text
from app.processing.extractor import extract_fields
from app.processing.normalizer import normalize_records
import pandas as pd

from app.output.csv_writer import write_csv
from app.output.excel_writer import write_excel

from app.utils.logger import setup_logger
from app.config.settings import Settings


def main():
    logger = setup_logger(Settings.LOG_LEVEL)
    logger.info("Application starting")

    input_dir = Path(Settings.INPUT_PDF_DIR)

    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        return

    pdf_files = list(input_dir.glob("*.pdf"))

    logger.info(f"Found {len(pdf_files)} PDF files")

    for pdf in pdf_files:
        logger.info(f"Detected file: {pdf.name}")

    logger.info("Startup validation complete")
    
    loaded_pdfs = load_pdfs(Settings.INPUT_PDF_DIR)
    logger.info(f"Successfully loaded {len(loaded_pdfs)} PDFs")
    
    parsed_pdfs = extract_text(loaded_pdfs)

    for pdf in parsed_pdfs:
        logger.info(
            f"{pdf['path'].name} extracted {len(pdf['pages'])} pages of text"
        )

    extracted_records = extract_fields(parsed_pdfs)

    logger.info(f"Extracted structured data for {len(extracted_records)} invoices")

    normalized_records = normalize_records(extracted_records)
    df = pd.DataFrame(normalized_records)
    logger.info(f"DataFrame created with {len(df)} rows")
    logger.info(f"\n{df.head()}")



if __name__ == "__main__":
    main()
