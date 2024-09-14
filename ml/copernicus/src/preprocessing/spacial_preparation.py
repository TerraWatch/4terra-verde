from pandas import DataFrame
from shapely import Polygon
from soil_co2_efflux.data.lucas_soil_data_loader import LucasSoilDataLoader

from data.models.feature import Feature
from data.models.feature_collection import FeatureCollection
from utils.geo import create_polygon_around_point


class SpatialFeaturesGenerator:

    def __init__(self, df: DataFrame):
        self.df = df

    def prepare_spatial_features(
            self,
            df: DataFrame,
            radius: float = 0.0001
    ) -> FeatureCollection:
        """
        Prepares spatial features (GeoJSON FeatureCollection) for NDVI calculations.

        Parameters:
        - df: the dataframe to generate the FeatureCollection for
        - radius: the polygon radius

        Returns:
        - fields: FeatureCollection, geojson formatted collection of spatial features
        """
        features = []

        for index, row in df.iterrows():
            lat = row[LucasSoilDataLoader.LAT_COL]
            long = row[LucasSoilDataLoader.LONG_COL]

            polygon_coordinates = create_polygon_around_point(lat, long, radius)

            feature = Feature(
                type="Feature",
                properties={},
                geometry=Polygon([polygon_coordinates]),
                placeId=index
            )

            features.append(feature)

        return FeatureCollection(
            type="FeatureCollection",
            features=features
        )
