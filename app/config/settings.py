import os
from pathlib import Path
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class Settings:
    INPUT_PDF_DIR = Path(os.getenv("INPUT_PDF_DIR", BASE_DIR / "data/input_pdfs"))
    OUTPUT_DIR = Path(os.getenv("OUTPUT_DIR", BASE_DIR / "data/output"))
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    SMTP_HOST = os.getenv("SMTP_HOST")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "0")) if os.getenv("SMTP_PORT") else None
    SMTP_USER = os.getenv("SMTP_USER")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    EMAIL_FROM = os.getenv("EMAIL_FROM")
    EMAIL_SUBJECT_OVERDUE = os.getenv(
        "EMAIL_SUBJECT_OVERDUE", "Invoice {invoice_number} Reminder"
    )

    @classmethod
    def smtp_enabled(cls) -> bool:
        return all(
            [
                cls.SMTP_HOST,
                cls.SMTP_PORT,
                cls.SMTP_USER,
                cls.SMTP_PASSWORD,
                cls.EMAIL_FROM,
            ]
        )
