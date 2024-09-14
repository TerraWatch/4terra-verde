import os

from data.copernicus_metrics_loader import CopernicusMetricsLoader
from data.models.copernicus_satellite_metric_type import CopernicusSatelliteMetricType
from feature_engineering.copernicus_feature_generator import CopernicusFeatureGenerator
from feature_engineering.copernicus_satellite_metric_factory import copernicus_satellite_metric_factory
from preprocessing.spacial_preparation import SpatialFeaturesGenerator
from soil_co2_efflux.data.data_writer import DataWriter
from soil_co2_efflux.data.lucas_soil_data_loader import LucasSoilDataLoader
from soil_co2_efflux.utils.config import Config as SoilCo2EffluxConfig
from utils.config import Config

soil_co2_efflux_config = SoilCo2EffluxConfig()
local_soil_data_writer = DataWriter()
local_soil_data_loader = LucasSoilDataLoader(soil_co2_efflux_config)
lucas_soil_data = local_soil_data_loader.load_processed_data_csv()
#
spatial_features_generator = SpatialFeaturesGenerator(lucas_soil_data)
config = Config()

for feature_type in CopernicusSatelliteMetricType:
    metric_type = copernicus_satellite_metric_factory(feature_type)
    print(f"Generated feature for {feature_type.name}: {feature_type}")
    copernicus_feature_generator = CopernicusFeatureGenerator(
        metric_type,
        spatial_features_generator,
        config
    )

    copernicus_feature_generator.generate()

copernicus_metrics_loader = CopernicusMetricsLoader(config)
ndvi_raw_copernicus_metrics_data = copernicus_metrics_loader.load_raw_data_csv('NDVI_RESULTS_YEAR_MONTH_*.csv')

local_soil_data_writer.add_column_and_save(
    lucas_soil_data,
    ndvi_raw_copernicus_metrics_data,
    'NDVI',
    os.path.join(
        config.PATHS.PROCESSED_DATA_FILE_PATH,
        LucasSoilDataLoader.PROCESSED_DATA_FILENAME
    )
)