import numpy as np
import json


class KMeans:
    def __init__(self, json_url: str):
        with open(json_url, "r") as f:
           self.centers = np.array(json.load(f))

    def __call__(self, x, y):
        return np.argmin(((self.centers - np.array([x, y]))**2).sum(axis=1))

kmean = KMeans("NN_models/kmeans_centers.json")