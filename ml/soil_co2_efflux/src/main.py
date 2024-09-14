from data.lucas_soil_data_loader import LucasSoilDataLoader
from utils.config import Config

config = Config()
local_soil_data_loader = LucasSoilDataLoader(config)
data = local_soil_data_loader.load_raw_data_csv()
