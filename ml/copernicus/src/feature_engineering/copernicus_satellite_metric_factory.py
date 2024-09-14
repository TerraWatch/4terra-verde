from data.models.copernicus_satellite_metric_type import CopernicusSatelliteMetricType, CopernicusSatelliteMetric, NDVI, Band04, Band08


def copernicus_satellite_metric_factory(type: CopernicusSatelliteMetricType) -> CopernicusSatelliteMetric:
    if type == CopernicusSatelliteMetricType.NDVI:
        return NDVI()
    elif type == CopernicusSatelliteMetricType.BAND04:
        return Band04()
    elif type == CopernicusSatelliteMetricType.BAND08:
        return Band08()
    else:
        raise ValueError(f"Unknown copernicus feature type: {type}")