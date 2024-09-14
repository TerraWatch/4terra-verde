from typing import Any

from pandas import DataFrame

# Used for local debugging
def replace_value_occurrences(df: DataFrame, filter_col: str, filter_val: Any, target_value: Any):
    df[filter_col] = df[filter_col].replace(filter_val, target_value)
    return df

# Used for local debugging
def count_value_occurrences(df: DataFrame, filter_col: str, filter_val: Any):
    return (df[filter_col] == filter_val).sum()

# Used for local debugging
def count_col_values(df: DataFrame, filter_col: str):
    return df[filter_col].value_counts()