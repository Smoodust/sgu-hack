import numpy as np
import json


class KMeans:
    """A class to load precomputed cluster centers and find the nearest cluster for points."""

    def __init__(self, json_url: str) -> None:
        """Initialize cluster centers from a JSON file.
        
        Args:
            json_url: Path to JSON file containing cluster centers data.
        """

        with open(json_url, "r") as f:
           self.centers = np.array(json.load(f))

    def __call__(self, x: float, y: float) -> int:
        """Find the nearest cluster center index for a given (x, y) point.
        
        Args:
            x: Horizontal coordinate of the point
            y: Vertical coordinate of the point
            
        Returns:
            Index of the closest cluster center
        """
        point = np.array([x, y])
        squared_distances = np.sum((self.centers - point) ** 2, axis=1)
        return np.argmin(squared_distances)

kmean = KMeans("NN_models/kmeans_centers.json")