import itertools
import os
from typing import Optional, Union, Final, Iterable, Tuple, List, Dict

import openeo
import pandas as pd

from datetime import datetime

from data.models.feature import Feature
from preprocessing.spacial_preparation import SpatialFeaturesGenerator
from data.models.feature_collection import FeatureCollection
from utils.config import Config


class NDVIFeatureGenerator:
    CSV_TITLE: Final[str] = "NDVI timeseries"
    CSV_FORMAT: Final[str] = "CSV"
    AGGREGATE_SPATIAL_REDUCER: Final[str] = "mean"
    PROCESSED_DATA_BATCH_FILENAME: Final[str] = "NDVI_RESULTS_YEAR_MONTH_{}_BATCH_INDEX_{}.csv"
    MAX_BATCH_SIZE: Final[int] = 200

    def __init__(
            self,
            spatial_features_generator: SpatialFeaturesGenerator,
            config: Config
    ):
        self.spatial_features_generator = spatial_features_generator
        self.config = config

    def generate_features_in_batches(self):
        features = self.spatial_features_generator.prepare_spatial_features()

        connection = self._open_connection()

        for year_month, features_batch in self._batch_by_month(features):
            print(f"calculating NDVI for year and month: {year_month}")

            if len(features_batch) > NDVIFeatureGenerator.MAX_BATCH_SIZE:
                # Split the features_batch into smaller batches
                num_batches = self._calculate_number_of_batches(features_batch)
                for i in range(num_batches):
                    start_index = i * NDVIFeatureGenerator.MAX_BATCH_SIZE
                    end_index = min((i + 1) * NDVIFeatureGenerator.MAX_BATCH_SIZE, len(features_batch))

                    smaller_batch = features_batch[start_index:end_index]
                    self._process_batch(smaller_batch, connection, year_month, i)
            else:
                # Process the batch as is
                self._process_batch(features_batch, connection, year_month, 0)

    def _process_batch(self, features_batch, connection, year_month, batch_index):
        start_time = datetime.now()
        ndvi_load_collection, geometries = self._get_ndvi_load_collection_cube(features_batch, connection, year_month)

        # Calculate the mean NDVI for each of the geometries.
        timeseries = ndvi_load_collection.aggregate_spatial(
            geometries=geometries,
            reducer=NDVIFeatureGenerator.AGGREGATE_SPATIAL_REDUCER
        )

        # We now execute this as a batch job and download the timeseries in CSV format.
        job = timeseries.execute_batch(
            out_format=NDVIFeatureGenerator.CSV_FORMAT,
            title=NDVIFeatureGenerator.CSV_TITLE
        )

        filename = os.path.join(
            self.config.PATHS.PROCESSED_DATA_FILE_PATH,
            NDVIFeatureGenerator.PROCESSED_DATA_BATCH_FILENAME.format(year_month, batch_index)
        )

        job.get_results().download_file(filename)
        pd.read_csv(filename, index_col=0).head()

        end_time = datetime.now()
        execution_time = end_time - start_time
        print(f"year and month: {year_month}, batch_index: {batch_index}, finished with time {execution_time}")

    def _open_connection(self):
        connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
        connection.authenticate_oidc()
        return connection

    def _get_ndvi_load_collection_cube(self, features, connection, year_month):
        geometries = self._prepare_load_connection_input(features)

        s2cube = connection.load_collection(
            "SENTINEL2_L2A",
            temporal_extent=[f"{year_month}-01", f"{year_month}-31"],
            bands=["B04", "B08"],
        )

        red = s2cube.band("B04")
        nir = s2cube.band("B08")
        ndvi = (nir - red) / (nir + red)

        return ndvi, geometries

    def _prepare_load_connection_input(self, features):
        fields = FeatureCollection(
            type="FeatureCollection",
            features=features
        )
        return fields.to_dict()

    def _generate_slice(self, slice_range: Optional[Union[slice, int]] = None):
        if isinstance(slice_range, int):
            return slice(slice_range)
        elif slice_range is None:
            return slice(None)
        return slice_range

    def _batch_by_month(self, features: List[Feature]) -> Iterable[Tuple[str, List[Feature]]]:
        """
        Batches features by month and year based on their sample_date.

        Parameters:
        - features: List of Feature objects

        Returns:
        - An iterable of tuples, where each tuple contains:
          - A string representing the month and year (format 'YYYY-MM')
          - A list of Feature objects from that month
        """

        # Helper function to extract month and year from sample_date
        def get_month_year(feature: Feature) -> str:
            date_obj = datetime.strptime(feature.sample_date, '%Y-%m-%d %H:%M:%S')
            return date_obj.strftime('%Y-%m')

        # Group features by month and year
        features.sort(key=lambda f: get_month_year(f))
        grouped_features: Dict[str, List[Feature]] = {
            k: list(g) for k, g in itertools.groupby(features, key=get_month_year)
        }

        # Return each batch of features
        for month_year, batch in grouped_features.items():
            yield month_year, batch

    def _calculate_number_of_batches(self, features_batch):
        return (len(features_batch) + NDVIFeatureGenerator.MAX_BATCH_SIZE - 1) // NDVIFeatureGenerator.MAX_BATCH_SIZE
