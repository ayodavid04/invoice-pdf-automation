from pathlib import Path
from app.pdf.loader import load_pdfs

from app.utils import logger
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



if __name__ == "__main__":
    main()
