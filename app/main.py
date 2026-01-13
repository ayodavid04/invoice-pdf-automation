from pathlib import Path
from app.core.pipeline import run_pipeline


if __name__ == "__main__":
    input_dir = Path("invoices")   # folder with PDFs
    results = run_pipeline(input_dir)

    for record in results:
        print(record)
