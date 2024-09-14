import itertools
import os
from typing import Final, Iterable, Tuple, List, Dict

import numpy as np
import openeo
import pandas as pd

from datetime import datetime

import scipy
from openeo import DataCube

from data.models.copernicus_satellite_metric_type import CopernicusSatelliteMetric
from data.models.feature import Feature
from preprocessing.spacial_preparation import SpatialFeaturesGenerator
from data.models.feature_collection import FeatureCollection
from utils.config import Config
from utils.date import get_max_days, get_year_month


class CopernicusFeatureGenerator:
    CSV_TITLE: Final[str] = "{} timeseries"
    CSV_FORMAT: Final[str] = "CSV"
    AGGREGATE_SPATIAL_REDUCER: Final[str] = "mean"
    PROCESSED_DATA_BATCH_FILENAME: Final[str] = "{}_RESULTS_YEAR_MONTH_{}_BATCH_INDEX_{}.csv"
    MAX_BATCH_SIZE: Final[int] = 50

    def __init__(
            self,
            copernicus_satellite_metric: CopernicusSatelliteMetric,
            spatial_features_generator: SpatialFeaturesGenerator,
            config: Config,
    ):
        self.copernicus_satellite_metric = copernicus_satellite_metric
        self.spatial_features_generator = spatial_features_generator
        self.config = config

    def generate(self):
        features = self.spatial_features_generator.prepare_spatial_features()

        connection = self._open_connection()

        for year_month, features_batch in self._batch_by_month(features):
            print(
                f"calculating {self.copernicus_satellite_metric.get_details().feature} for the year and month: {year_month}")

            if len(features_batch) > CopernicusFeatureGenerator.MAX_BATCH_SIZE:
                # Split the features_batch into smaller batches
                num_batches = self._calculate_number_of_batches(features_batch)
                for i in range(num_batches):
                    start_index = i * CopernicusFeatureGenerator.MAX_BATCH_SIZE
                    end_index = min((i + 1) * CopernicusFeatureGenerator.MAX_BATCH_SIZE, len(features_batch))

                    smaller_batch = features_batch[start_index:end_index]
                    self._process_batch(smaller_batch, connection, year_month, i)
            else:
                self._process_batch(features_batch, connection, year_month, 0)

    def _process_batch(self, features_batch, connection, year_month, batch_index):
        start_time = datetime.now()
        feature_load_collection, geometries = self._get_feature_load_collection_cube(
            features_batch,
            connection,
            year_month
        )

        # Calculate the mean feature for each of the geometries.
        timeseries = feature_load_collection.aggregate_spatial(
            geometries=geometries,
            reducer=CopernicusFeatureGenerator.AGGREGATE_SPATIAL_REDUCER
        )

        job = timeseries.execute_batch(
            out_format=CopernicusFeatureGenerator.CSV_FORMAT,
            title=CopernicusFeatureGenerator.CSV_TITLE
        )

        filename = os.path.join(
            self.config.PATHS.PROCESSED_DATA_FILE_PATH,
            CopernicusFeatureGenerator.PROCESSED_DATA_BATCH_FILENAME.format(
                self.copernicus_satellite_metric.get_details().feature,
                year_month,
                batch_index
            )
        )

        job.get_results().download_file(filename)
        pd.read_csv(filename, index_col=0).head()

        end_time = datetime.now()
        execution_time = end_time - start_time
        print(f"year and month: {year_month}, batch_index: {batch_index}, finished with time {execution_time}")

    def _get_feature_load_collection_cube(self, features, connection, year_month):
        geometries = self._prepare_load_connection_input(features)
        year, month = year_month.split('-')
        max_month_days = get_max_days(int(year), int(month))

        s2cube = connection.load_collection(
            self.copernicus_satellite_metric.get_details().sentinel,
            temporal_extent=[f"{year_month}-01", f"{year_month}-{max_month_days}"],
            bands=self.copernicus_satellite_metric.get_details().bands,
        )

        feature_masked: DataCube = self._apply_cloud_mask(s2cube)

        return feature_masked, geometries

    def _apply_cloud_mask(self, s2cube):
        scl = s2cube.band("SCL")
        mask = ~((scl == 4) | (scl == 5))

        # 2D gaussian kernel
        g = scipy.signal.windows.gaussian(11, std=1.6)
        kernel = np.outer(g, g)
        kernel = kernel / kernel.sum()

        # Morphological dilation of mask: convolution + threshold
        mask = mask.apply_kernel(kernel)
        mask = mask > 0.1

        return self.copernicus_satellite_metric.get_feature_calc_cube(s2cube).mask(mask)

    def _prepare_load_connection_input(self, features):
        fields = FeatureCollection(
            type="FeatureCollection",
            features=features
        )
        return fields.to_dict()

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

        # Group features by month and year
        features.sort(key=lambda f: get_year_month(f))
        grouped_features: Dict[str, List[Feature]] = {
            k: list(g) for k, g in itertools.groupby(features, key=get_year_month)
        }

        # Return each batch of features
        for month_year, batch in grouped_features.items():
            yield month_year, batch

    def _calculate_number_of_batches(self, features_batch):
        return (len(features_batch) + CopernicusFeatureGenerator.MAX_BATCH_SIZE - 1)

    def _open_connection(self):
        connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
        connection.authenticate_oidc()
        return connection
