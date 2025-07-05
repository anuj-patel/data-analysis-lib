"""
Module for calculating statistics on Stack Overflow survey data.
"""
from typing import Union, List, Dict, Any, Optional
import pandas as pd
import numpy as np


def describe(df: pd.DataFrame, include: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Generate descriptive statistics for numeric columns in the DataFrame.
    
    Args:
        df: The DataFrame to analyze
        include: List of column names to include. If None, all numeric columns are included.
    
    Returns:
        pd.DataFrame: A DataFrame containing count, mean, median, std, min, and max for each numeric column
    
    Examples:
        >>> import pandas as pd
        >>> df = pd.DataFrame({
        ...     'age': [25, 30, 35, 40, 45],
        ...     'years_coding': [1, 5, 10, 15, 20]
        ... })
        >>> describe(df)
                   age  years_coding
        count     5.0           5.0
        mean     35.0          10.2
        median   35.0          10.0
        std       7.9           7.5
        min      25.0           1.0
        max      45.0          20.0
    """
    # Filter columns if include is specified
    if include is not None:
        df = df[include].copy()
    
    # Get only numeric columns
    numeric_df = df.select_dtypes(include=['number'])
    
    # Calculate statistics
    stats = pd.DataFrame({
        'count': numeric_df.count(),
        'mean': numeric_df.mean(),
        'median': numeric_df.median(),
        'std': numeric_df.std(),
        'min': numeric_df.min(),
        'max': numeric_df.max()
    }).T
    
    return stats


def mean(data: Union[pd.Series, List[float]]) -> float:
    """
    Calculate the mean of a Series or list of values.
    
    Args:
        data: A pandas Series or list of numeric values
    
    Returns:
        float: The mean value
    """
    if isinstance(data, pd.Series):
        return data.mean()
    return sum(data) / len(data) if data else float('nan')


def median(data: Union[pd.Series, List[float]]) -> float:
    """
    Calculate the median of a Series or list of values.
    
    Args:
        data: A pandas Series or list of numeric values
    
    Returns:
        float: The median value
    """
    if isinstance(data, pd.Series):
        return data.median()
    
    if not data:
        return float('nan')
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_data[mid-1] + sorted_data[mid]) / 2
    else:
        return sorted_data[mid]


def mode(data: Union[pd.Series, List[Any]]) -> Union[Any, List[Any]]:
    """
    Calculate the mode (most frequent value) of a Series or list.
    
    Args:
        data: A pandas Series or list of values
    
    Returns:
        The most frequent value or a list of values if there are multiple modes
    """
    if isinstance(data, pd.Series):
        mode_result = data.mode()
        return mode_result[0] if len(mode_result) == 1 else mode_result.tolist()
    
    if not data:
        return float('nan')
    
    # Count occurrences
    counts: Dict[Any, int] = {}
    for value in data:
        counts[value] = counts.get(value, 0) + 1
    
    # Find the maximum count
    max_count = max(counts.values())
    
    # Get all values with the maximum count
    modes = [value for value, count in counts.items() if count == max_count]
    
    return modes[0] if len(modes) == 1 else modes