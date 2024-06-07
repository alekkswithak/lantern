import csv
import os
from typing import Dict, Any, Optional, List


class DataRepository:
    _cached_data: Dict[str, Dict[str, Any]] = {}

    def __init__(self, file_path: Optional[str] = None) -> None:
        """
        Initialize the DataRepository instance.

        Args:
            file_path (str, optional): The path to the CSV file containing the data.
                If not provided, the default path will be used.
        """
        if file_path is None:
            current_file_path = os.path.abspath(__file__)
            project_root = os.path.dirname(os.path.dirname(current_file_path))
            file_path = os.path.join(project_root, "data/database.csv")
        self.file_path = file_path
        if file_path not in DataRepository._cached_data:
            DataRepository._cached_data[file_path] = self.read_csv_to_dict()

    def read_csv_to_dict(self) -> Dict[str, Dict[str, Any]]:
        """
        Read the CSV file and convert its contents into a nested dictionary.

        Returns:
            Dict[str, Dict[str, Any]]: A nested dictionary where keys are company names
                and values are dictionaries containing data for each company.
        """
        data_dict: Dict[str, Dict[str, Any]] = {}
        with open(self.file_path, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                row = {k: DataRepository._convert_value(v) for k, v in row.items()}
                data_dict.setdefault(row["Company Name"], {}).update(row)
        return data_dict

    def get_data(self) -> Dict[str, Dict[str, Any]]:
        """
        Get the entire data dictionary.

        Returns:
            Dict[str, Dict[str, Any]]: The entire data dictionary.
        """
        return DataRepository._cached_data[self.file_path]

    def get_all_companies(self) -> List[str]:
        """
        Get a list of all company names in the data.

        Returns:
            List[str]: A list containing the names of all companies in the data.
        """
        return list(self.get_data().keys())

    def get_company_data(self, company_name: str) -> Dict[str, Any]:
        """
        Get data for a specific company.

        Args:
            company_name (str): The name of the company.

        Returns:
            Dict[str, Any]: A dictionary containing data for the specified company.
                Returns an empty dictionary if the company name is not found.
        """
        return self.get_data().get(company_name, {})

    @staticmethod
    def _convert_value(value: str) -> Any:
        """
        Convert a string value to an appropriate data type.

        Args:
            value (str): The string value to be converted.

        Returns:
            Any: The converted value. If the value represents an integer, it is returned as int.
                If it represents a float, it is returned as float. Otherwise, the original string
                value is returned.
        """
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value
