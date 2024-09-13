import os
import pandas as pd

from abc import ABC, abstractmethod
from utils.config import Config


class DataLoader(ABC):

    def __init__(self, config: Config, raw_filename: str, columns: list[str]):
        self.config = config
        self.raw_filename = raw_filename
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
