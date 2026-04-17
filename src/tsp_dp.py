"""
Held-Karp algorithm: exact TSP solution using dynamic programming.
Charlene: DP implementation
"""

from itertools import combinations
from math import inf
from typing import Dict, List, Tuple


def _validate_cost_matrix(cost_matrix: List[List[float]]) -> None:
    """Validate that the matrix is square before solving."""
    n = len(cost_matrix)
    for row in cost_matrix:
        if len(row) != n:
            raise ValueError("cost_matrix must be square")


def solve_tsp_dp_detailed(
    cost_matrix: List[List[float]], start: int = 0
) -> Tuple[List[int], float, int]:
    """
    Solve TSP exactly using Held-Karp dynamic programming.

    The returned step count matches the Held-Karp visualization slider:
      1 base-case step + one step per filled dp[S][j] state + 1 close-tour step.

    Returns:
        (route as list of city indices, total cost, visualization step count)
    """
    _validate_cost_matrix(cost_matrix)
    n = len(cost_matrix)

    if n == 0:
        return [], 0.0, 0
    if not 0 <= start < n:
        raise ValueError("start must be a valid city index")
    if n == 1:
        return [start], 0.0, 1

    others = [city for city in range(n) if city != start]
    costs: Dict[Tuple[int, int], float] = {}
    parents: Dict[Tuple[int, int], int] = {}

    steps = 1

    for city in others:
        mask = 1 << city
        costs[(mask, city)] = float(cost_matrix[start][city])
        parents[(mask, city)] = start
        steps += 1

    for subset_size in range(2, n):
        for subset in combinations(others, subset_size):
            mask = 0
            for city in subset:
                mask |= 1 << city

            for last in subset:
                prev_mask = mask ^ (1 << last)
                best_cost = inf
                best_parent = start

                for prev in subset:
                    if prev == last:
                        continue
                    candidate = costs[(prev_mask, prev)] + cost_matrix[prev][last]
                    if candidate < best_cost:
                        best_cost = candidate
                        best_parent = prev

                costs[(mask, last)] = best_cost
                parents[(mask, last)] = best_parent
                steps += 1

    full_mask = 0
    for city in others:
        full_mask |= 1 << city

    best_total = inf
    last_city = start
    for city in others:
        candidate = costs[(full_mask, city)] + cost_matrix[city][start]
        if candidate < best_total:
            best_total = candidate
            last_city = city

    steps += 1

    route_reversed = [last_city]
    mask = full_mask
    city = last_city
    while True:
        parent = parents[(mask, city)]
        if parent == start:
            break
        route_reversed.append(parent)
        mask ^= 1 << city
        city = parent

    route = [start] + list(reversed(route_reversed))
    return route, float(best_total), steps


def solve_tsp_dp(cost_matrix: List[List[float]], start: int = 0) -> Tuple[List[int], float]:
    """
    Solve TSP exactly using Held-Karp (DP).

    Args:
        cost_matrix: n x n matrix; cost_matrix[i][j] = cost from i to j
        start: Starting city index

    Returns:
        (route as list of city indices, total cost)
    """
    route, cost, _ = solve_tsp_dp_detailed(cost_matrix, start=start)
    return route, cost
