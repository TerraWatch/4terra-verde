from feature_engineering.ndvi_generator import NDVIFeatureGenerator
from preprocessing.spacial_preparation import SpatialFeaturesGenerator
from soil_co2_efflux.data.lucas_soil_data_loader import LucasSoilDataLoader
from soil_co2_efflux.utils.config import Config
from utils.config import Config as copernicus_config

config = Config()
local_soil_data_loader = LucasSoilDataLoader(config)
lucas_soil_data = local_soil_data_loader.load_processed_data_csv()

spatial_features_generator = SpatialFeaturesGenerator(lucas_soil_data)
ndvi_generator = NDVIFeatureGenerator(spatial_features_generator, copernicus_config)
ndvi_generator.generate_features_in_batches()
