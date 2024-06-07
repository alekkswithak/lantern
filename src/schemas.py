from pydantic import BaseModel, validator
from typing import Any, Dict
from src.data_repository import DataRepository


class DataComparisonRequest(BaseModel):
    """
    Model representing a request for comparing data between a file and a database entry.

    Attributes:
        filepath (str): The path to the file to be compared.
                        Must be one of the predefined valid file paths.
        company_name (str): The name of the company whose data is being compared.
                            Must be a valid company name listed in the data repository.
    """

    filepath: str
    company_name: str

    @validator("filepath")
    def validate_filepath(cls, v: str) -> str:
        """
        Hacky validation to check provided filepath is one of
        the allowed file paths.

        Args:
            v (str): The file path provided in the request.

        Raises:
            ValueError: If the file path is not in the list of valid file paths.

        Returns:
            str: The validated file path.
        """
        valid_filepaths = (
            "assets/healthinc.pdf",
            "assets/retailco.pdf",
            "assets/financellc.pdf",
        )
        if v not in valid_filepaths:
            raise ValueError("Filepath is not valid.")
        return v

    @validator("company_name")
    def validate_company_name(cls, v: str) -> str:
        """
        Validates that the provided company name exists in the data repository.

        Args:
            v (str): The company name provided in the request.

        Raises:
            ValueError: If the company name is not found in the data repository.

        Returns:
            str: The validated company name.
        """
        data_repository = DataRepository()
        if v not in data_repository.get_all_companies():
            raise ValueError("Company name is not valid.")
        return v


class DataComparisonResponse(BaseModel):
    """
    Model representing the response of a data comparison operation.

    Attributes:
        company_name (str): The name of the company whose data was compared.
        file_data (Dict[str, Any]): The data extracted from the provided file.
        db_data (Dict[str, Any]): The data fetched from the database for the specified company.
        differences (Dict[str, Dict[str, Any]]): A dictionary highlighting the differences
                                                 between the file data and the database data.
    """

    company_name: str
    file_data: Dict[str, Any]
    db_data: Dict[str, Any]
    differences: Dict[str, Dict[str, Any]]
