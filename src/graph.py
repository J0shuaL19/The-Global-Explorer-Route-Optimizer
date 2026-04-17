"""
Graph model for the travel network.
Represents cities as nodes and travel costs as weighted edges.
Charlene: Graph modeling
"""

from typing import List, Sequence


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
        if len(cost_matrix) != len(cities):
            raise ValueError("cost_matrix row count must match number of cities")

        n = len(cities)
        for row in cost_matrix:
            if len(row) != n:
                raise ValueError("cost_matrix must be square")

        self.cities = list(cities)
        self.cost_matrix = [list(row) for row in cost_matrix]
        self.n = n

    def get_cost(self, i: int, j: int) -> float:
        """Return travel cost from city index i to j."""
        return self.cost_matrix[i][j]

    def get_city_name(self, i: int) -> str:
        """Return city name at index i."""
        return self.cities[i]

    def tour_cost(self, route: Sequence[int]) -> float:
        """Return the cycle cost of a route that visits each city once."""
        if len(route) <= 1:
            return 0.0

        total = 0.0
        for idx, city in enumerate(route):
            next_city = route[(idx + 1) % len(route)]
            total += self.get_cost(city, next_city)
        return float(total)

    def route_to_names(self, route: Sequence[int], include_return: bool = True) -> List[str]:
        """Convert a route of city indices into readable city names."""
        if not route:
            return []

        names = [self.get_city_name(city) for city in route]
        if include_return and len(route) > 1:
            names.append(self.get_city_name(route[0]))
        return names

    @classmethod
    def from_dict(cls, data: dict) -> "TravelGraph":
        """Create graph from data dict with 'cities' and 'cost_matrix' keys."""
        return cls(data["cities"], data["cost_matrix"])
