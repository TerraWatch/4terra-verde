from data.lucas_soil_data_loader import LucasSoilDataLoader
from preprocessing.lucas_soil_data_cleaning import clean_oc
from utils.config import Config

config = Config()
local_soil_data_loader = LucasSoilDataLoader(config)
data = local_soil_data_loader.load_raw_data_csv()

cleaned_data = clean_oc(data)
