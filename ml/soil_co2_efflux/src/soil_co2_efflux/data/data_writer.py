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
        # Ensure the DataFrame is not empty
        if df.empty:
            raise ValueError("The DataFrame is empty and cannot be saved.")

        # Save the DataFrame to a CSV file
        df.to_csv(file_path, index=index, float_format=float_format, header=header)

        print(f"DataFrame successfully saved to {file_path}")