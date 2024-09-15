import pandas as pd
from typing import Optional


class DataWriter:

    def save_to_csv(
            self,
            df: pd.DataFrame,
            file_path: str,
            index: bool = False,
            float_format: Optional[str] = None,
            header: bool = True
    ) -> None:
        """
        Saves a pandas DataFrame to a CSV file.

        Parameters:
        - df: pandas DataFrame to be saved
        - file_path: string, path to the output CSV file
        - index: boolean, whether to write row names (index)
        - float_format: string, format string for floating point numbers (e.g., '.2f' for 2 decimal places)
        - header: boolean, whether to write column names
        """
        if df.empty:
            raise ValueError("The DataFrame is empty and cannot be saved.")

        df.to_csv(file_path, index=index, float_format=float_format, header=header)

        print(f"DataFrame successfully saved to {file_path}")

    def add_column_and_save(
            self,
            df_to_update: pd.DataFrame,
            df_with_band: pd.DataFrame,
            new_column_name: str,
            file_path: str,
            column_name_to_copy: str = 'band_unnamed'
    ) -> None:
        """
        Adds a new column from df_with_band to df_to_update and saves to a CSV.

        Parameters:
        - df_to_update: DataFrame to which the new column will be added
        - df_with_band: DataFrame containing the values for the new column
        - new_column_name: Name of the new column to add
        - file_path: Path where the updated CSV will be saved
        """
        if len(df_to_update) != len(df_with_band):
            raise ValueError("DataFrames have different lengths. Cannot align the rows.")

        df_to_update[new_column_name] = df_with_band[column_name_to_copy].values

        self.save_to_csv(df_to_update, file_path)
