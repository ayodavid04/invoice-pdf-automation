# app/db/insert.py
from app.db.session import SessionLocal
from app.db.models import Invoice

def insert_invoices(records):
    session = SessionLocal()

    for r in records:
        session.add(Invoice(**r))

    session.commit()
    session.close()
