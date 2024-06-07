from typing import Any, Dict


def compare_data(
    file_data: Dict[str, Any], db_data: Dict[str, Any]
) -> Dict[str, Dict[str, Any]]:
    """
    Compare data between file and database and return the differences.

    Args:
        file_data (Dict[str, Any]): A dictionary representing data from a file.
        db_data (Dict[str, Any]): A dictionary representing data from a database.

    Returns:
        Dict[str, Dict[str, Any]]: A dictionary containing the differences between
        the file and database data.
    """
    differences = {}
    all_keys = set(file_data.keys()).union(db_data.keys())

    for key in all_keys:
        file_value = file_data.get(key)
        db_value = db_data.get(key)
        if file_value != db_value:
            differences[key] = {"file": file_value, "db": db_value}

    return differences
