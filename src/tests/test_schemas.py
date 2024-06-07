import pytest
from pydantic import ValidationError
from src.schemas import (
    DataComparisonRequest,
    DataComparisonResponse,
)
from src.tests.mocks import mock_data_repository


def test_valid_data_comparison_request(mock_data_repository):
    """
    Test that a valid DataComparisonRequest passes without errors.
    """
    valid_request = DataComparisonRequest(
        filepath="assets/healthinc.pdf", company_name="HealthInc"
    )
    assert valid_request.filepath == "assets/healthinc.pdf"
    assert valid_request.company_name == "HealthInc"


def test_invalid_filepath_in_request(mock_data_repository):
    """
    Test that an invalid filepath in DataComparisonRequest raises a ValueError.
    """
    with pytest.raises(ValidationError) as exc_info:
        DataComparisonRequest(filepath="assets/unknown.pdf", company_name="HealthInc")
    assert "Filepath is not valid" in str(exc_info.value)


def test_invalid_company_name_in_request(mock_data_repository):
    """
    Test that an invalid company name in DataComparisonRequest raises a ValueError.
    """
    with pytest.raises(ValidationError) as exc_info:
        DataComparisonRequest(
            filepath="assets/healthinc.pdf", company_name="UnknownCompany"
        )
    assert "Company name is not valid" in str(exc_info.value)


def test_valid_data_comparison_response():
    """
    Test that a valid DataComparisonResponse is created correctly.
    """
    response = DataComparisonResponse(
        company_name="HealthInc",
        file_data={"key1": "value1"},
        db_data={"key1": "value2"},
        differences={"key1": {"file": "value1", "db": "value2"}},
    )
    assert response.company_name == "HealthInc"
    assert response.file_data == {"key1": "value1"}
    assert response.db_data == {"key1": "value2"}
    assert response.differences == {"key1": {"file": "value1", "db": "value2"}}


def test_data_comparison_response_missing_fields():
    """
    Test that missing required fields in DataComparisonResponse raise ValidationError.
    """
    with pytest.raises(ValidationError):
        DataComparisonResponse(
            company_name="HealthInc",
            file_data={"key1": "value1"},
        )


def test_data_comparison_response_invalid_field_type():
    """
    Test that invalid field types in DataComparisonResponse raise ValidationError.
    """
    with pytest.raises(ValidationError):
        DataComparisonResponse(
            company_name="HealthInc",
            file_data="This should be a dictionary",
            db_data={"key1": "value2"},
            differences={"key1": {"file": "value1", "db": "value2"}},
        )
