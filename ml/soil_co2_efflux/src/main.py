import os

from data.data_writer import DataWriter
from data.lucas_soil_data_loader import LucasSoilDataLoader
from preprocessing.lucas_soil_data_cleaning import clean_oc
from utils.config import Config

config = Config()
local_soil_data_loader = LucasSoilDataLoader(config)
data = local_soil_data_loader.load_raw_data_csv()

cleaned_data = clean_oc(data)

data_writer = DataWriter()
data_writer.save_to_csv(cleaned_data, os.path.join(config.PATHS.PROCESSED_DATA_FILE_PATH, LucasSoilDataLoader.PROCESSED_DATA_FILENAME))
