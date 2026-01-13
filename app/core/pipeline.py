from app.pdf.loader import load_pdfs
from app.pdf.parser import extract_text
from app.processing.extractor import extract_fields
from app.processing.validator import apply_fallbacks


def run_pipeline(input_dir):
    # Step 1 — Load PDFs
    pdfs = load_pdfs(input_dir)

    # Step 2 — Extract raw text from PDFs
    parsed_pdfs = extract_text(pdfs)

    # Step 3 — Extract structured fields
    extracted_records = extract_fields(parsed_pdfs)

    # Step 4 — Apply fallback validation rules
    validated_records = apply_fallbacks(extracted_records)

    return validated_records
