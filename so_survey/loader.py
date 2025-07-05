"""
Module for loading Stack Overflow survey data from Excel files.
"""
from typing import Optional, Dict, Any, Union
import pandas as pd
import os


def load_survey(file_path: str, sheet_name: Union[str, int, None] = 0, **kwargs: Any) -> pd.DataFrame:
    """
    Load a Stack Overflow survey from an Excel file into a pandas DataFrame.

    Args:
        file_path: Path to the Excel file (.xlsx)
        sheet_name: Name or index of the sheet to read (default: 0 for first sheet)
        **kwargs: Additional arguments to pass to pandas.read_excel

    Returns:
        pandas.DataFrame: DataFrame containing the survey data with inferred dtypes
                         and missing values represented as NaN

    Examples:
        >>> df = load_survey("path/to/survey.xlsx")
        >>> print(df.shape)
        (1000, 50)

        >>> # Load specific sheet
        >>> df = load_survey("path/to/survey.xlsx", sheet_name="Survey_Data")

        >>> # Load second sheet by index
        >>> df = load_survey("path/to/survey.xlsx", sheet_name=1)
    """
    # Validate file extension
    if not file_path.lower().endswith(('.xlsx', '.xls')):
        raise ValueError(f"File must be an Excel file (.xlsx or .xls), got: {file_path}")

    # Check if file exists
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Set default parameters but allow overriding via kwargs
    params: Dict[str, Any] = {
        "na_values": ["NA", "N/A", "", "NULL", "null", "NaN"],
        "keep_default_na": True,
        "dtype": None,  # Let pandas infer dtypes
        "engine": "openpyxl",  # Use openpyxl engine for .xlsx files
    }
    params.update(kwargs)

    try:
        # Load the Excel file into a DataFrame
        result = pd.read_excel(file_path, sheet_name=sheet_name, **params)

        # Handle the case where pandas returns a dict of DataFrames
        if isinstance(result, dict):
            if sheet_name is None:
                # If no sheet specified and we got a dict, take the first sheet
                first_sheet_name = list(result.keys())[0]
                df = result[first_sheet_name]
                print(f"Loaded Excel file: {os.path.basename(file_path)}")
                print(f"Sheet: {first_sheet_name} (first sheet)")
            else:
                # This shouldn't happen with our current logic, but handle it
                raise RuntimeError(f"Unexpected dict result when sheet_name={sheet_name}")
        else:
            # Normal case - we got a DataFrame
            df = result
            print(f"Loaded Excel file: {os.path.basename(file_path)}")
            if isinstance(sheet_name, str):
                print(f"Sheet: {sheet_name}")
            elif isinstance(sheet_name, int):
                print(f"Sheet index: {sheet_name}")
            else:
                print(f"Sheet index: 0 (first sheet)")

        return df

    except Exception as e:
        raise RuntimeError(f"Error loading Excel file {file_path}: {str(e)}")


def list_excel_sheets(file_path: str) -> list:
    """
    List all sheet names in an Excel file.

    Args:
        file_path: Path to the Excel file

    Returns:
        list: List of sheet names

    Examples:
        >>> sheets = list_excel_sheets("survey.xlsx")
        >>> print(sheets)
        ['Survey_Data', 'Metadata', 'Summary']
    """
    if not file_path.lower().endswith(('.xlsx', '.xls')):
        raise ValueError(f"File must be an Excel file (.xlsx or .xls), got: {file_path}")

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    try:
        # Read Excel file to get sheet names
        excel_file = pd.ExcelFile(file_path, engine="openpyxl")
        return excel_file.sheet_names
    except Exception as e:
        raise RuntimeError(f"Error reading Excel file {file_path}: {str(e)}")