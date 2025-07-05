"""
Module for creating subsets of Stack Overflow survey data.
"""
from typing import Iterable, Union, List, Any
import pandas as pd


def filter_by_column(df: pd.DataFrame, column: str, values: Iterable) -> pd.DataFrame:
    """
    Return a subset of rows where the specified column's values match those in the provided iterable.

    Args:
        df: The DataFrame to filter
        column: The column name to filter on
        values: An iterable of values to match

    Returns:
        pd.DataFrame: A filtered DataFrame containing only rows where the column's
                     value is in the values iterable. Index is preserved.

    Raises:
        KeyError: If the specified column doesn't exist in the DataFrame
        ValueError: If the values iterable is empty

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'country': ['USA', 'Canada', 'UK', 'USA', 'Australia'],
        ...     'age': [25, 30, 35, 40, 45]
        ... })
        >>> filtered_df = filter_by_column(df, 'country', ['USA', 'UK'])
        >>> print(filtered_df)
           country  age
        0      USA   25
        2       UK   35
        3      USA   40
    """
    # Check if column exists in DataFrame
    if column not in df.columns:
        available_columns = list(df.columns)
        raise KeyError(f"Column '{column}' not found in DataFrame. Available columns: {available_columns}")

    # Convert values to list if it's not already
    values_list = list(values)

    # Check if values list is empty
    if not values_list:
        raise ValueError("Values list cannot be empty")

    # Filter the DataFrame
    filtered_df = df[df[column].isin(values_list)].copy()

    # Check if any rows were found
    if filtered_df.empty:
        unique_values = df[column].dropna().unique()
        print(f"Warning: No rows found matching values {values_list}")
        print(f"Available values in column '{column}': {list(unique_values)[:20]}...")  # Show first 20 values

    return filtered_df


def filter_by_value_range(df: pd.DataFrame, column: str, min_value: Any = None, max_value: Any = None) -> pd.DataFrame:
    """
    Return a subset of rows where the specified column's values are within the given range.

    Args:
        df: The DataFrame to filter
        column: The column name to filter on
        min_value: The minimum value (inclusive), or None for no minimum
        max_value: The maximum value (inclusive), or None for no maximum

    Returns:
        pd.DataFrame: A filtered DataFrame containing only rows where the column's
                     value is within the specified range. Index is preserved.

    Raises:
        KeyError: If the specified column doesn't exist in the DataFrame

    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'country': ['USA', 'Canada', 'UK', 'USA', 'Australia'],
        ...     'age': [25, 30, 35, 40, 45]
        ... })
        >>> filtered_df = filter_by_value_range(df, 'age', 30, 40)
        >>> print(filtered_df)
           country  age
        1    Canada   30
        2        UK   35
        3       USA   40
    """
    # Check if column exists in DataFrame
    if column not in df.columns:
        available_columns = list(df.columns)
        raise KeyError(f"Column '{column}' not found in DataFrame. Available columns: {available_columns}")

    result = df.copy()

    if min_value is not None:
        result = result[result[column] >= min_value]

    if max_value is not None:
        result = result[result[column] <= max_value]

    return result