from abc import ABC, abstractmethod
from enum import Enum
from typing import List

from openeo import DataCube


class CopernicusSatelliteMetricDetails:
    def __init__(
            self,
            feature: str,
            bands: List[str],
            sentinel: str,
    ):
        self.feature = feature
        self.bands = bands
        self.sentinel = sentinel


class CopernicusSatelliteMetric(ABC):
    @abstractmethod
    def get_details(self) -> CopernicusSatelliteMetricDetails:
        """Method to define the cube function of the copernicus satellite metric"""
        pass

    @abstractmethod
    def get_feature_calc_cube(self, cube: DataCube) -> DataCube:
        """Method to define the cube function of the copernicus satellite metric"""
        pass


class NDVI(CopernicusSatelliteMetric):
    def __init__(self):
        self.details = CopernicusSatelliteMetricDetails(
            "NDVI",
            ["B04", "B08", "SCL"],
            "SENTINEL2_L2A"
        )

    def get_details(self) -> CopernicusSatelliteMetricDetails:
        return self.details

    def get_feature_calc_cube(self, cube: DataCube) -> DataCube:
        red = cube.band("B04")
        nir = cube.band("B08")
        ndvi = (nir - red) / (nir + red)

        return ndvi


class Band04(CopernicusSatelliteMetric):
    def __init__(self):
        self.details = CopernicusSatelliteMetricDetails(
            "Band04",
            ["B04", "SCL"],
            "SENTINEL2_L2A"
        )

    def get_details(self) -> CopernicusSatelliteMetricDetails:
        return self.details

    def get_feature_calc_cube(self, cube: DataCube) -> DataCube:
        red = cube.band("B04")
        return red


class Band08(CopernicusSatelliteMetric):
    def __init__(self):
        self.details = CopernicusSatelliteMetricDetails(
            "Band08",
            ["B08", "SCL"],
            "SENTINEL2_L2A"
        )

    def get_details(self) -> CopernicusSatelliteMetricDetails:
        return self.details

    def get_feature_calc_cube(self, cube: DataCube) -> DataCube:
        nir = cube.band("B08")
        return nir


class CopernicusSatelliteMetricType(Enum):
    NDVI = "ndvi"
    BAND04 = "band04"
    BAND08 = "band08"
