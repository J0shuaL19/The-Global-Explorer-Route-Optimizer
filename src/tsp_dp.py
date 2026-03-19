"""
Held-Karp algorithm: exact TSP solution using dynamic programming.
Charlene: DP implementation
"""

from typing import List, Tuple

# TODO: Implement Held-Karp algorithm
# Time: O(n^2 * 2^n), Space: O(n * 2^n)


def solve_tsp_dp(cost_matrix: List[List[float]], start: int = 0) -> Tuple[List[int], float]:
    """
    Solve TSP exactly using Held-Karp (DP).

    Args:
        cost_matrix: n x n matrix; cost_matrix[i][j] = cost from i to j
        start: Starting city index

    Returns:
        (route as list of city indices, total cost)
    """
    n = len(cost_matrix)
    if n == 0:
        return [], 0.0
    if n == 1:
        return [0], 0.0

    # Placeholder: return trivial route until implementation
    route = list(range(n))
    cost = sum(
        cost_matrix[route[i]][route[(i + 1) % n]] for i in range(n)
    )
    return route, cost
