import itertools
import os
from typing import Optional, Union, Final, Iterable, Tuple, List

import openeo
import pandas as pd

from datetime import datetime

from preprocessing.spacial_preparation import SpatialFeaturesGenerator
from data.models.feature_collection import FeatureCollection
from utils.config import Config


class NDVIFeatureGenerator:
    BATCH_SIZE: Final[int] = 200
    CSV_TITLE: Final[str] = "NDVI timeseries"
    CSV_FORMAT: Final[str] = "CSV"
    AGGREGATE_SPATIAL_REDUCER: Final[str] = "mean"
    PROCESSED_DATA_FILENAME_BATCH: Final[str] = "NDVI_RESULTS_BATCH_{}.csv"

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

        for index, features_batch in self._chunk_creator(features, NDVIFeatureGenerator.BATCH_SIZE):
            print("index: {}, features_batch: {}".format(index, features_batch))

            start_time = datetime.now()
            ndvi_load_collection, geometries = self._get_ndvi_load_collection_cube(features_batch, connection)

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
                NDVIFeatureGenerator.PROCESSED_DATA_FILENAME_BATCH.format(index)
            )

            job.get_results().download_file(filename)
            pd.read_csv(filename, index_col=0).head()

            end_time = datetime.now()

            execution_time = end_time - start_time
            print("index: {}, features_batch: {} finished with time {}".format(index, features_batch, execution_time))

    def _open_connection(self):
        connection = openeo.connect(url="openeo.dataspace.copernicus.eu")
        connection.authenticate_oidc()
        return connection

    def _get_ndvi_load_collection_cube(self, features, connection):
        geometries = self._prepare_load_connection_input(features)

        s2cube = connection.load_collection(
            "SENTINEL2_L2A",
            temporal_extent=["2018-07-06", "2018-07-08"],
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

    def _chunk_creator(self, iterable: Iterable, batch_size: int) -> Iterable[Tuple[int, List]]:
        """
        Creates chunks from an iterable with a specified batch size, and also returns the index of each chunk.

        Parameters:
        - iterable: the input iterable to be chunked
        - batch_size: the size of each chunk

        Returns:
        - An iterable of tuples, where each tuple contains:
          - The index of the chunk
          - A list of items in the chunk
        """
        args = [iter(iterable)] * batch_size
        chunks = itertools.zip_longest(*args, fillvalue=None)

        for index, chunk in enumerate(chunks):
            # Convert chunk to a list, removing None values
            chunk_list = [item for item in chunk if item is not None]
            yield index, chunk_list
