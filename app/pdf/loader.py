from pathlib import Path
from pypdf import PdfReader
from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)


def load_pdfs(pdf_dir: Path):
    pdf_files = list(pdf_dir.glob("*.pdf"))
    loaded = []

    for pdf_path in pdf_files:
        try:
            reader = PdfReader(pdf_path)
            page_count = len(reader.pages)

            logger.info(f"Loaded {pdf_path.name} ({page_count} pages)")
            loaded.append({
                "path": pdf_path,
                "reader": reader,
                "pages": page_count
            })

        except Exception as e:
            logger.error(f"Failed to load {pdf_path.name}: {e}")

    return loaded
