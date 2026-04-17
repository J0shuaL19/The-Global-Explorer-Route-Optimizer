"""
Approximation algorithms for TSP: MST-based 2-approx and greedy heuristics.
Jasmine: Approximation implementation
"""

from math import inf
from typing import List, Tuple


def _validate_cost_matrix(cost_matrix: List[List[float]]) -> None:
    n = len(cost_matrix)
    for row in cost_matrix:
        if len(row) != n:
            raise ValueError("cost_matrix must be square")


def _tour_cost(cost_matrix: List[List[float]], route: List[int]) -> float:
    if len(route) <= 1:
        return 0.0

    total = 0.0
    for idx, city in enumerate(route):
        next_city = route[(idx + 1) % len(route)]
        total += cost_matrix[city][next_city]
    return float(total)


def solve_tsp_mst_detailed(
    cost_matrix: List[List[float]], start: int = 0
) -> Tuple[List[int], float, int]:
    """
    Solve TSP using the MST preorder traversal heuristic.

    The returned step count matches the MST visualization slider:
      n Prim build steps + Euler walk traversal steps + shortcut decision steps
      + 1 close step + 1 final-summary step.

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

    in_tree = [False] * n
    best_weight = [inf] * n
    parent = [-1] * n

    in_tree[start] = True
    for city in range(n):
        if city == start:
            continue
        best_weight[city] = cost_matrix[start][city]
        parent[city] = start

    for _ in range(n - 1):
        next_city = -1
        next_weight = inf
        for city in range(n):
            if in_tree[city]:
                continue
            if best_weight[city] < next_weight or (
                best_weight[city] == next_weight and city < next_city
            ):
                next_weight = best_weight[city]
                next_city = city

        in_tree[next_city] = True

        for city in range(n):
            if in_tree[city]:
                continue
            weight = cost_matrix[next_city][city]
            if weight < best_weight[city] or (
                weight == best_weight[city] and next_city < parent[city]
            ):
                best_weight[city] = weight
                parent[city] = next_city

    tree = [[] for _ in range(n)]
    for city in range(n):
        if city == start:
            continue
        tree[parent[city]].append(city)
        tree[city].append(parent[city])

    for neighbors in tree:
        neighbors.sort()

    tree_walk: List[int] = []

    def _euler_dfs(node: int, from_node: int) -> None:
        tree_walk.append(node)
        for neighbor in tree[node]:
            if neighbor == from_node:
                continue
            _euler_dfs(neighbor, node)
            tree_walk.append(node)

    _euler_dfs(start, -1)

    route: List[int] = []
    seen = set()
    for city in tree_walk:
        if city not in seen:
            route.append(city)
            seen.add(city)

    traverse_steps = max(len(tree_walk) - 1, 0)
    shortcut_steps = max(len(tree_walk) - 1, 0)
    steps = n + traverse_steps + shortcut_steps + 2

    return route, _tour_cost(cost_matrix, route), steps


def solve_tsp_mst(cost_matrix: List[List[float]], start: int = 0) -> Tuple[List[int], float]:
    """
    Solve TSP using MST-based 2-approximation.

    Returns:
        (route as list of city indices, total cost)
    """
    route, cost, _ = solve_tsp_mst_detailed(cost_matrix, start=start)
    return route, cost


def solve_tsp_greedy_detailed(
    cost_matrix: List[List[float]], start: int = 0
) -> Tuple[List[int], float, int]:
    """
    Solve TSP using greedy nearest-neighbor heuristic.

    The returned step count matches the greedy visualization slider:
      1 initialize step + (n - 1) pick-next-city steps + 1 close-tour step.

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

    route = [start]
    visited = {start}
    current = start
    steps = 1

    while len(route) < n:
        best_city = -1
        best_cost = inf
        for city in range(n):
            if city in visited:
                continue
            candidate = cost_matrix[current][city]
            if candidate < best_cost or (candidate == best_cost and city < best_city):
                best_cost = candidate
                best_city = city
        route.append(best_city)
        visited.add(best_city)
        current = best_city
        steps += 1

    steps += 1

    return route, _tour_cost(cost_matrix, route), steps


def solve_tsp_greedy(cost_matrix: List[List[float]], start: int = 0) -> Tuple[List[int], float]:
    """
    Solve TSP using greedy nearest-neighbor heuristic.

    Returns:
        (route as list of city indices, total cost)
    """
    route, cost, _ = solve_tsp_greedy_detailed(cost_matrix, start=start)
    return route, cost
