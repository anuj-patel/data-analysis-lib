"""
Module for cataloging available Stack Overflow survey datasets.
"""
import os
from typing import List, Optional
import pathlib


def list_datasets(directory: Optional[str] = None) -> List[str]:
    """
    List available datasets (Excel files) in the specified directory.

    Args:
        directory: Path to the directory containing dataset files.
                  If None, uses the default data directory.

    Returns:
        List[str]: List of dataset names (filenames without the .xlsx extension)

    Examples:
        >>> list_datasets('/path/to/data')
        ['survey_2020', 'survey_2021', 'survey_2022']
    """
    # If no directory is specified, use the default data directory
    if directory is None:
        # Get the directory of the current file
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Default data directory is a 'data' folder in the same directory as this file
        directory = os.path.join(current_dir, '..', 'data')

    # Ensure the directory exists
    if not os.path.exists(directory):
        return []

    # Get a list of all .xlsx and .xls files in the directory
    excel_files = [
        os.path.splitext(file)[0]  # Remove the extension
        for file in os.listdir(directory)
        if file.lower().endswith(('.xlsx', '.xls'))
    ]

    return excel_files


def get_dataset_path(dataset_name: str, directory: Optional[str] = None) -> str:
    """
    Get the full path to a dataset file.

    Args:
        dataset_name: Name of the dataset (with or without .xlsx extension)
        directory: Path to the directory containing dataset files.
                  If None, uses the default data directory.

    Returns:
        str: Full path to the dataset file

    Examples:
        >>> get_dataset_path('survey_2021')
        '/path/to/data/survey_2021.xlsx'
    """
    # If no directory is specified, use the default data directory
    if directory is None:
        # Get the directory of the current file
        current_dir = pathlib.Path(__file__).parent.absolute()
        # Default data directory is a 'data' folder in the same directory as this file
        directory = os.path.join(current_dir, '..', 'data')

    # Add .xlsx extension if not present
    if not dataset_name.lower().endswith(('.xlsx', '.xls')):
        dataset_name = f"{dataset_name}.xlsx"

    # Return the full path
    return os.path.join(directory, dataset_name)