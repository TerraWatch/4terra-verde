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


"The normalized difference vegetation index is a simple, but effective index for quantifying green vegetation. It is a measure of the state of vegetation health based on how plants reflect light at certain wavelengths."
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


"The normalized difference moisture Index (NDMI) is used to determine vegetation water content and monitor droughts."
class NDMI(CopernicusSatelliteMetric):
    def __init__(self):
        self.details = CopernicusSatelliteMetricDetails(
            "NDMI",
            ["B8A", "B11", "SCL"],
            "SENTINEL2_L2A"
        )

    def get_details(self) -> CopernicusSatelliteMetricDetails:
        return self.details

    def get_feature_calc_cube(self, cube: DataCube) -> DataCube:
        b8a = cube.band("B8A")
        b11 = cube.band("B11")
        ndmi = (b8a - b11) / (b8a + b11)

        return ndmi


"The normalized difference water index is most appropriate for water body mapping."
class NDWI(CopernicusSatelliteMetric):
    def __init__(self):
        self.details = CopernicusSatelliteMetricDetails(
            "NDWI",
            ["B03", "B08", "SCL"],
            "SENTINEL2_L2A"
        )

    def get_details(self) -> CopernicusSatelliteMetricDetails:
        return self.details

    def get_feature_calc_cube(self, cube: DataCube) -> DataCube:
        b03 = cube.band("B03")
        b08 = cube.band("B08")
        ndwi = (b03 - b08) / (b03 + b08)

        return ndwi


class CopernicusSatelliteMetricType(Enum):
    NDVI = "ndvi"
    NDMI = "ndmi"
    NDWI = "ndwi"
