from data.models.copernicus_satellite_metric_type import CopernicusSatelliteMetricType, CopernicusSatelliteMetric, NDVI, \
    NDMI, NDWI


def copernicus_satellite_metric_factory(type: CopernicusSatelliteMetricType) -> CopernicusSatelliteMetric:
    if type == CopernicusSatelliteMetricType.NDVI:
        return NDVI()
    if type == CopernicusSatelliteMetricType.NDMI:
        return NDMI()
    elif type == CopernicusSatelliteMetricType.NDWI:
        return NDWI()
    else:
        raise ValueError(f"Unknown copernicus feature type: {type}")