from typing import Dict, Any
from xmlrpc.client import DateTime

from data.models.geometry import Geometry


class Feature:
    def __init__(self, type: str, properties: Dict[str, Any], geometry: Geometry, sample_date: DateTime):
        self.type = type
        self.properties = properties
        self.geometry = geometry
        self.sample_date = sample_date

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "properties": self.properties,
            "geometry": self.geometry.to_dict()
        }
