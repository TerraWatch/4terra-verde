from pandas import DataFrame


def transform_col_to_float(df: DataFrame, col: str):
    df.loc[:, col] = df[col].astype(float).round(2)
    return df
