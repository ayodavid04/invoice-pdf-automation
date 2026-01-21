from pathlib import Path
from app.pdf.loader import load_pdfs
from app.pdf.parser import extract_text
from app.processing.extractor import extract_fields
from app.processing.validator import apply_fallbacks
from app.utils.logger import get_logger
from app.analytics.analytics import build_analytics_dataset

logger = get_logger()


def run_pipeline(input_dir: Path):
    
    loaded_pdfs = load_pdfs(input_dir)
    logger.info(f"Loaded {len(loaded_pdfs)} PDFs")

    parsed_pdfs = extract_text(loaded_pdfs)
    logger.info("Text extraction complete")

    extracted_records = extract_fields(parsed_pdfs)
    logger.info("Field extraction complete")

    validated_records = apply_fallbacks(extracted_records)
    logger.info("Validation complete")
    build_analytics_dataset(validated_records)


    return validated_records
