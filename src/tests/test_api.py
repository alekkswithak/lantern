import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.pdf_service import PdfService
from src.tests.mocks import mock_data_repository

client = TestClient(app)


class TestAPI:
    """
    Tests for the / endpoint.
    """

    @pytest.fixture
    def mock_pdf_service(self, monkeypatch):
        """
        Fixture to mock PdfService dependency using monkeypatch.

        This fixture patches the extract method of PdfService to return a sample file data dictionary.
        """

        def mock_extract(*args, **kwargs):
            return {"data": "from file"}

        monkeypatch.setattr(PdfService, "extract", mock_extract)

    def test_post_data_comparison_success(
        self,
        mock_pdf_service,
        mock_data_repository,
    ):
        """
        Test the / endpoint with valid inputs for a successful data comparison.

        This test verifies that the endpoint correctly processes the request and returns the
        expected data structure when provided with a valid file path and company name.
        """
        response = client.post(
            "/", json={"filepath": "assets/healthinc.pdf", "company_name": "HealthInc"}
        )

        assert response.status_code == 200
        response_data = response.json()
        assert response_data["company_name"] == "HealthInc"
        assert response_data["file_data"] == {"data": "from file"}
        assert response_data["db_data"] == {"data": "from db"}
        assert response_data["differences"] == {
            "data": {"db": "from db", "file": "from file"}
        }

    def test_post_data_comparison_invalid_filepath(self):
        """
        Test the / endpoint with an invalid file path input.

        This test verifies that the endpoint returns a 422 Unprocessable Entity status and
        appropriate error message when the file path does not end with '.pdf'.

        """
        response = client.post(
            "/", json={"filepath": "/invalid.txt", "company_name": "HealthInc"}
        )

        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"] == "Value error, Filepath is not valid."
        )
        assert response.json()["detail"][0]["type"] == "value_error"

    def test_post_data_comparison_empty_company_name(self):
        """
        Test the / endpoint with an empty company name input.

        This test verifies that the endpoint returns a 422 Unprocessable Entity status and
        appropriate error message when the company name is empty or contains only whitespace.

        """
        response = client.post(
            "/",
            json={
                "filepath": "assets/healthinc.pdf",
                "company_name": "   ",
            },
        )

        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Company name is not valid."
        )
        assert response.json()["detail"][0]["type"] == "value_error"
