import os
from typing import Final, List

import pandas as pd

from utils.config import Config
import glob


class CopernicusMetricsLoader:
    DATE_COL = "date"
    FEATURE_INDEX_COL = "feature_index"
    BAND_UNNAMED_COL = "band_unnamed"

    COLUMNS: Final[List[str]] = [
        DATE_COL, FEATURE_INDEX_COL, BAND_UNNAMED_COL
    ]

    def __init__(self, config: Config):
        self.config = config

    def load_raw_data_csv(self, file_pattern: str):
        try:
            file_path_with_pattern = os.path.join(self.config.PATHS.RAW_DATA_FILE_PATH, file_pattern)
            file_paths = glob.glob(file_path_with_pattern)

            processed_dfs = [self._process_file(file_path) for file_path in file_paths]

            combined_df = pd.concat(processed_dfs, ignore_index=True)

            return combined_df
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None

    def _process_file(self, file_path):
        df = pd.read_csv(file_path, parse_dates=['date'])

        df[CopernicusMetricsLoader.DATE_COL] = pd.to_datetime(df[CopernicusMetricsLoader.DATE_COL], errors='coerce')
        df = df.dropna(subset=[CopernicusMetricsLoader.BAND_UNNAMED_COL])

        df[CopernicusMetricsLoader.BAND_UNNAMED_COL] = pd.to_numeric(
            df[CopernicusMetricsLoader.BAND_UNNAMED_COL],
            errors='coerce'
        )

        # Group by date and feature_index, and calculate the average of band_unnamed
        processed_df = df.groupby(
            [CopernicusMetricsLoader.FEATURE_INDEX_COL], as_index=False
        )[CopernicusMetricsLoader.BAND_UNNAMED_COL].mean()

        return processed_df
