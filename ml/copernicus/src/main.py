from data.models.copernicus_satellite_metric_type import CopernicusSatelliteMetricType
from feature_engineering.copernicus_feature_generator import CopernicusFeatureGenerator
from feature_engineering.copernicus_satellite_metric_factory import copernicus_satellite_metric_factory
from preprocessing.spacial_preparation import SpatialFeaturesGenerator
from soil_co2_efflux.data.lucas_soil_data_loader import LucasSoilDataLoader
from soil_co2_efflux.utils.config import Config as SoilCo2EffluxConfig
from utils.config import Config

soil_co2_efflux_config = SoilCo2EffluxConfig()
local_soil_data_loader = LucasSoilDataLoader(soil_co2_efflux_config)
lucas_soil_data = local_soil_data_loader.load_processed_data_csv()

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
