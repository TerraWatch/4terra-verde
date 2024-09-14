from typing import List

from pandas import DataFrame

from data.models.geometry import Geometry
from soil_co2_efflux.data.lucas_soil_data_loader import LucasSoilDataLoader

from data.models.feature import Feature
from utils.geo import create_polygon_around_point


class SpatialFeaturesGenerator:

    def __init__(self, df: DataFrame):
        self.df = df

    def prepare_spatial_features(
            self,
            radius: float = 0.0001
    ) -> List[Feature]:
        """
        Prepares spatial features (GeoJSON FeatureCollection) for NDVI calculations.

        Parameters:
        - df: the dataframe to generate the FeatureCollection for
        - radius: the polygon radius

        Returns:
        - fields: List[Feature], geojson formatted collection of spatial features
        """
        features = []

        for index, row in self.df.iterrows():
            lat = row[LucasSoilDataLoader.LAT_COL]
            long = row[LucasSoilDataLoader.LONG_COL]
            sample_date = row[LucasSoilDataLoader.SURVEY_DATE_COL]

            try:
                polygon_coordinates = create_polygon_around_point(lat, long, radius)
                feature = Feature(
                    type="Feature",
                    properties={},
                    geometry=Geometry(
                        type="Polygon",
                        coordinates=[polygon_coordinates]
                    ),
                    sample_date=sample_date
                )
                features.append(feature)
            except ValueError:
                continue

        return features
