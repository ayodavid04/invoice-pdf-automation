from app.utils.logger import setup_logger
from app.config.settings import Settings

logger = setup_logger(Settings.LOG_LEVEL)


def extract_text(loaded_pdfs):
    extracted = []

    for pdf in loaded_pdfs:
        text_pages = []

        for idx, page in enumerate(pdf["reader"].pages):
            try:
                text = page.extract_text() or ""
                logger.info(f"Extracted text from {pdf['path'].name} page {idx+1}")
                text_pages.append(text)

            except Exception as e:
                logger.error(
                    f"Failed extracting page {idx+1} from {pdf['path'].name}: {e}"
                )

        extracted.append({
            "path": pdf["path"],
            "pages": text_pages
        })

    return extracted
