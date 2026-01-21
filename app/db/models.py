# app/db/models.py
from sqlalchemy import Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Date, Numeric

Base = declarative_base()


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True)

    file_name = Column(String)

    invoice_number = Column(String)

    client_id = Column(String)

    invoice_date = Column(Date)

    subtotal = Column(Numeric)

    tax = Column(Numeric)
    tax_confidence = Column(String)

    total = Column(Numeric)
