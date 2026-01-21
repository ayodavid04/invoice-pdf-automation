from app.db.session import SessionLocal
from app.db.models import Invoice

def insert_invoices(records: list[dict]):
    db = SessionLocal()

    try:
        for r in records:
            # Rename source_file → file_name to match model
            if "source_file" in r:
                r["file_name"] = r.pop("source_file")

            # Keep only canonical fields to match your model
            canonical_keys = [
                "file_name",
                "invoice_number",
                "client_id",
                "invoice_date",
                "subtotal",
                "tax",
                "total"
            ]
            clean_r = {k: r[k] for k in canonical_keys if k in r}

            db.add(Invoice(**clean_r))
        db.commit()
    finally:
        db.close()
