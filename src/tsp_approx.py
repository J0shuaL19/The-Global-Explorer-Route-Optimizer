"""
Approximation algorithms for TSP: MST-based 2-approx and greedy heuristics.
Jasmine: Approximation implementation
"""

from typing import List, Tuple

# TODO: Implement MST-based 2-approximation
# TODO: Implement greedy (nearest neighbor) heuristic


def solve_tsp_mst(cost_matrix: List[List[float]], start: int = 0) -> Tuple[List[int], float]:
    """
    Solve TSP using MST-based 2-approximation.

    Returns:
        (route as list of city indices, total cost)
    """
    n = len(cost_matrix)
    if n <= 1:
        return list(range(n)), 0.0

    # Placeholder
    route = list(range(n))
    cost = sum(
        cost_matrix[route[i]][route[(i + 1) % n]] for i in range(n)
    )
    return route, cost


def solve_tsp_greedy(cost_matrix: List[List[float]], start: int = 0) -> Tuple[List[int], float]:
    """
    Solve TSP using greedy nearest-neighbor heuristic.

    Returns:
        (route as list of city indices, total cost)
    """
    n = len(cost_matrix)
    if n <= 1:
        return list(range(n)), 0.0

    # Placeholder
    route = list(range(n))
    cost = sum(
        cost_matrix[route[i]][route[(i + 1) % n]] for i in range(n)
    )
    return route, cost
