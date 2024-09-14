from typing import Dict, Any, List


class Geometry:
    def __init__(self, type: str, coordinates: List[List[List[float]]]):
        self.type = type
        self.coordinates = coordinates

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "coordinates": self.coordinates
        }
