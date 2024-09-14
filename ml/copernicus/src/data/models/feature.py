from typing import Dict, Any

from data.models.geometry import Geometry


class Feature:
    def __init__(self, type: str, properties: Dict[str, Any], geometry: Geometry, placeId: int):
        self.type = type
        self.properties = properties
        self.geometry = geometry
        self.placeId = placeId

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "properties": self.properties,
            "geometry": self.geometry.to_dict()
        }
