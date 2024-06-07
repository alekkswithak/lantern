from src.pdf_service import PdfService
from src.data_repository import DataRepository
import os

TEST_KEY = os.environ.get("TEST_KEY")


def get_pdf_service() -> PdfService:
    return PdfService(key=TEST_KEY)


def get_data_repository() -> DataRepository:
    return DataRepository()
