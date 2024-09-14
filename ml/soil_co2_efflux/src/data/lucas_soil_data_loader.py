from typing import Final, List

from data.data_loader import DataLoader
from utils.config import Config


class LucasSoilDataLoader(DataLoader):

    OC_COL = "OC"
    LAT_COL = "TH_LAT"
    LONG_COL = "TH_LONG"

    COLUMNS: Final[List[str]] = [
        OC_COL, LAT_COL, LONG_COL,
    ]

    RAW_DATA_FILENAME: Final[str] = "LUCAS-SOIL-2018.csv"
    PROCESSED_DATA_FILENAME: Final[str] = "LUCAS-SOIL-PROCESSED-2018.csv"

    def __init__(self, config: Config):
        super().__init__(
            config,
            self.RAW_DATA_FILENAME,
            self.COLUMNS
        )

    def load_raw_data_csv(self):
        return super().load_raw_data_csv()
