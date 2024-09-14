import os
import pandas as pd

from abc import ABC, abstractmethod

from soil_co2_efflux.utils.config import Config


class DataLoader(ABC):

    def __init__(self, config: Config, raw_filename: str, processed_filename: str, columns: list[str]):
        self.config = config
        self.raw_filename = raw_filename
        self.processed_filename = processed_filename
        self.columns = columns

    @abstractmethod
    def load_raw_data_csv(self):
        try:
            return pd.read_csv(
                os.path.join(self.config.PATHS.RAW_DATA_FILE_PATH, self.raw_filename),
                usecols=self.columns,
            )
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None

    @abstractmethod
    def load_processed_data_csv(self):
        try:
            return pd.read_csv(
                os.path.join(self.config.PATHS.PROCESSED_DATA_FILE_PATH, self.processed_filename),
                usecols=self.columns,
            )
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return None
