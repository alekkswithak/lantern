import unittest
import os
from src.data_repository import DataRepository
from unittest.mock import patch


class TestDataRepository(unittest.TestCase):
    """
    Test class for the DataRepository class.
    """

    @classmethod
    def setUpClass(cls):
        cls.current_directory = os.path.dirname(os.path.abspath(__file__))
        cls.file_path = os.path.join(cls.current_directory, "example_data.csv")
        cls.repo = DataRepository(cls.file_path)

    def test_get_data(self):
        """
        Test if the returned data is a dictionary, and not empty.
        """
        self.assertIsInstance(self.repo.get_data(), dict)
        self.assertTrue(len(self.repo.get_data()) > 0)

    def test_get_company_data_existing(self):
        """
        Test if data for an existing company is returned correctly.
        """
        company_data = self.repo.get_company_data("HealthInc")
        self.assertIsInstance(company_data, dict)
        self.assertEqual(company_data["Location"], "New York")
        self.assertEqual(company_data["Industry"], "Healthcare")

    def test_get_company_data_non_existing(self):
        """
        Test if data for a non-existing company returns an empty dictionary.
        """
        company_data = self.repo.get_company_data("Non-existent Company")
        self.assertEqual(company_data, {})

    def test_same_data_source(self):
        """
        Test if separate instances use the same source of data
        """
        repo2 = DataRepository(self.file_path)

        self.assertIs(self.repo.get_data(), repo2.get_data())

    @patch(
        "src.data_repository.DataRepository.get_data",
        return_value={"Company A": {}, "Company B": {}},
    )
    def test_get_all_companies(self, mock_get_data):
        """
        Test if all company names are returned.
        """
        expected_result = ["Company A", "Company B"]
        self.assertEqual(self.repo.get_all_companies(), expected_result)
