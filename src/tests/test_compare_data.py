import unittest
from src.helpers import compare_data


class TestCompareData(unittest.TestCase):
    def test_compare_data(self):
        file_data = {"key1": 10, "key2": "value2", "key3": True}
        db_data = {"key1": 10, "key2": "value3", "key4": False}

        expected_result = {
            "key2": {"file": "value2", "db": "value3"},
            "key3": {"file": True, "db": None},
            "key4": {"file": None, "db": False},
        }

        differences = compare_data(file_data, db_data)
        self.assertEqual(differences, expected_result)

    def test_compare_data_empty(self):
        file_data = {}
        db_data = {}

        differences = compare_data(file_data, db_data)
        self.assertEqual(differences, {})

    def test_compare_data_identical(self):
        file_data = {"key1": 10, "key2": "value2", "key3": True}
        db_data = {"key1": 10, "key2": "value2", "key3": True}

        differences = compare_data(file_data, db_data)
        self.assertEqual(differences, {})

    def test_compare_data_one_empty(self):
        file_data = {}
        db_data = {"key1": 10, "key2": "value2", "key3": True}

        differences = compare_data(file_data, db_data)
        self.assertEqual(
            differences, {k: {"file": None, "db": v} for k, v in db_data.items()}
        )

    def test_compare_data_different_types(self):
        file_data = {"key1": 10, "key2": "value2", "key3": True}
        db_data = {"key1": 10, "key2": 20, "key3": "True"}

        expected_result = {
            "key2": {"file": "value2", "db": 20},
            "key3": {"file": True, "db": "True"},
        }

        differences = compare_data(file_data, db_data)
        self.assertEqual(differences, expected_result)
