"""
Graph model for the travel network.
Represents cities as nodes and travel costs as weighted edges.
Charlene: Graph modeling
"""

from typing import List


class TravelGraph:
    """
    Weighted graph representing cities (nodes) and travel costs (edges).
    """

    def __init__(self, cities: List[str], cost_matrix: List[List[float]]):
        """
        Args:
            cities: List of city names (order matches cost_matrix indices)
            cost_matrix: Adjacency matrix; cost_matrix[i][j] = cost from city i to j
        """
        self.cities = cities
        self.cost_matrix = cost_matrix
        self.n = len(cities)

    def get_cost(self, i: int, j: int) -> float:
        """Return travel cost from city index i to j."""
        return self.cost_matrix[i][j]

    def get_city_name(self, i: int) -> str:
        """Return city name at index i."""
        return self.cities[i]

    @classmethod
    def from_dict(cls, data: dict) -> "TravelGraph":
        """Create graph from data dict with 'cities' and 'cost_matrix' keys."""
        return cls(data["cities"], data["cost_matrix"])
