from pathlib import Path
from PyPDF2 import PdfReader
from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)


def load_pdfs(input_dir: Path):
    pdfs = []

    for pdf_path in input_dir.glob("*.pdf"):
        try:
            reader = PdfReader(pdf_path)
            pdfs.append({
                "path": pdf_path,
                "reader": reader
            })
            logger.info(f"Loaded PDF: {pdf_path.name}")

        except Exception as e:
            logger.error(f"Failed loading {pdf_path.name}: {e}")

    return pdfs
