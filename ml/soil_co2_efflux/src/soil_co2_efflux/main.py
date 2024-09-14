import os

from soil_co2_efflux.data.data_writer import DataWriter
from soil_co2_efflux.data.lucas_soil_data_loader import LucasSoilDataLoader
from soil_co2_efflux.preprocessing.lucas_soil_data_cleaning import clean_oc
from soil_co2_efflux.utils.config import Config

config = Config()
local_soil_data_loader = LucasSoilDataLoader(config)
data = local_soil_data_loader.load_raw_data_csv()

cleaned_data = clean_oc(data)

data_writer = DataWriter()
data_writer.save_to_csv(
    cleaned_data,
    os.path.join(
        config.PATHS.PROCESSED_DATA_FILE_PATH,
        LucasSoilDataLoader.PROCESSED_DATA_FILENAME
    )
)
