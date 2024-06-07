import pytest
from src.data_repository import DataRepository


@pytest.fixture
def mock_data_repository(monkeypatch):
    """
    Fixture to mock the DataRepository
    """

    class MockDataRepository:
        def get_all_companies(self):
            return ["HealthInc", "RetailCo", "FinanceLLC"]

        def get_company_data(self):
            return {"data": "from db"}

    def mock_get_all_companies(*args, **kwargs):
        return MockDataRepository().get_all_companies()

    def mock_get_company_data(*args, **kwargs):
        return MockDataRepository().get_company_data()

    monkeypatch.setattr(DataRepository, "get_all_companies", mock_get_all_companies)
    monkeypatch.setattr(DataRepository, "get_company_data", mock_get_company_data)
