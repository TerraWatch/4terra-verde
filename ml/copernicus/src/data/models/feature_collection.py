from typing import List, Dict, Any

from data.models.feature import Feature


class FeatureCollection:
    def __init__(self, type: str, features: List[Feature]):
        self.type = type
        self.features = features

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.type,
            "features": [feature.to_dict() for feature in self.features]
        }
