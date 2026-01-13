from app.pdf.loader import load_pdfs
from app.pdf.parser import extract_text
from app.processing.extractor import extract_fields
from app.processing.validator import apply_fallbacks


def run_pipeline(input_dir):
    pdfs = load_pdfs(input_dir)
    parsed = extract_text(pdfs)
    extracted = extract_fields(parsed)
    validated = apply_fallbacks(extracted)
    return validated
