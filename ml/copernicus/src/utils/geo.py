from typing import List
from shapely.geometry import Polygon, Point

def create_polygon_around_point(lat: float, lon: float, radius: float) -> List[List[float]]:
    center_point = Point(lon, lat)

    buffer_polygon: Polygon = center_point.buffer(radius)

    # Extract the exterior coordinates of the polygon and convert them into a list of lists [lon, lat]
    coordinates: List[List[float]] = [list(coord) for coord in buffer_polygon.exterior.coords]

    # for coord in coordinates:
    #     print(f"{coord[0]}, {coord[1]}")
    return coordinates
