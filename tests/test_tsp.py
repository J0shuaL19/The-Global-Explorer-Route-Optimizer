"""
Automated tests and printable comparison report for the TSP project.
Joshua: Testing
"""

import json
import sys
from pathlib import Path
from typing import Callable, Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from graph import TravelGraph
from tsp_dp import solve_tsp_dp, solve_tsp_dp_detailed
from tsp_approx import (
    solve_tsp_greedy,
    solve_tsp_greedy_detailed,
    solve_tsp_mst,
    solve_tsp_mst_detailed,
)

PROJECT_ROOT = Path(__file__).parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "cities.json"

Solver = Callable[[List[List[float]], int], Tuple[List[int], float, int]]


def _format_number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}"


def _load_graph() -> TravelGraph:
    with open(DATA_PATH, encoding="utf-8") as file:
        data = json.load(file)
    return TravelGraph.from_dict(data)


def _assert_valid_tour(cost_matrix: List[List[float]], route: List[int], start: int) -> None:
    n = len(cost_matrix)
    assert len(route) == n
    assert route[0] == start
    assert len(set(route)) == n
    assert set(route) == set(range(n))


def _route_cost(cost_matrix: List[List[float]], route: List[int]) -> float:
    if len(route) <= 1:
        return 0.0
    return float(
        sum(cost_matrix[route[i]][route[(i + 1) % len(route)]] for i in range(len(route)))
    )


def _format_route(graph: TravelGraph, route: List[int]) -> str:
    return " -> ".join(graph.route_to_names(route, include_return=True))


def _collect_comparison_rows(graph: TravelGraph):
    algorithms: List[Tuple[str, Solver]] = [
        ("DP (Held-Karp)", solve_tsp_dp_detailed),
        ("Greedy", solve_tsp_greedy_detailed),
        ("MST 2-approx", solve_tsp_mst_detailed),
    ]

    rows = []
    for start, city_name in enumerate(graph.cities):
        start_rows = []
        dp_route, dp_cost, dp_steps = solve_tsp_dp_detailed(graph.cost_matrix, start=start)
        _assert_valid_tour(graph.cost_matrix, dp_route, start)
        start_rows.append(
            {
                "start": city_name,
                "algorithm": "DP (Held-Karp)",
                "cost": dp_cost,
                "steps": dp_steps,
                "gap_vs_dp": 0.0,
                "route": _format_route(graph, dp_route),
            }
        )

        for algorithm_name, solver in algorithms[1:]:
            route, cost, steps = solver(graph.cost_matrix, start=start)
            _assert_valid_tour(graph.cost_matrix, route, start)
            start_rows.append(
                {
                    "start": city_name,
                    "algorithm": algorithm_name,
                    "cost": cost,
                    "steps": steps,
                    "gap_vs_dp": 0.0 if dp_cost == 0 else ((cost - dp_cost) / dp_cost) * 100,
                    "route": _format_route(graph, route),
                }
            )

        rows.append(start_rows)
    return rows


def print_detailed_report() -> None:
    graph = _load_graph()
    comparison_rows = _collect_comparison_rows(graph)

    print("Detailed TSP Comparison Report")
    print("=" * 120)
    print(f"Dataset: {', '.join(graph.cities)}")

    for start_rows in comparison_rows:
        start_city = start_rows[0]["start"]

        print(f"\nStart city: {start_city}")
        print("-" * 120)
        print(f"{'Algorithm':<18}{'Cost':>10}{'Steps':>10}{'Gap vs DP':>12}  Route")
        for row in start_rows:
            print(
                f"{row['algorithm']:<18}{_format_number(row['cost']):>10}{row['steps']:>10}"
                f"{row['gap_vs_dp']:>11.2f}%  {row['route']}"
            )


def test_empty_graph():
    """Empty graph should return empty route with zero cost."""
    route, cost = solve_tsp_dp([])
    assert route == []
    assert cost == 0.0


def test_single_city():
    """Single city: route is [0], cost is 0."""
    cost_matrix = [[0]]
    route, cost = solve_tsp_dp(cost_matrix)
    assert route == [0]
    assert cost == 0.0


def test_two_cities():
    """Two cities: route visits both, cost is round-trip."""
    cost_matrix = [
        [0, 10],
        [10, 0],
    ]
    route, cost = solve_tsp_dp(cost_matrix)
    assert route == [0, 1]
    assert cost == 20.0


def test_three_cities_symmetric():
    """Three cities with symmetric costs."""
    cost_matrix = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0],
    ]
    for start in range(3):
        route, cost = solve_tsp_dp(cost_matrix, start=start)
        _assert_valid_tour(cost_matrix, route, start)
        assert cost == 6.0


def test_graph_from_dict():
    """TravelGraph loads correctly from dict."""
    data = {
        "cities": ["A", "B", "C"],
        "cost_matrix": [[0, 1, 2], [1, 0, 3], [2, 3, 0]],
    }
    graph = TravelGraph.from_dict(data)
    assert graph.cities == ["A", "B", "C"]
    assert graph.get_cost(0, 1) == 1
    assert graph.get_city_name(2) == "C"
    assert graph.tour_cost([0, 1, 2]) == 6.0


def test_greedy_returns_valid_route():
    """Greedy returns a valid tour and its cost matches the route."""
    cost_matrix = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
    route, cost = solve_tsp_greedy(cost_matrix, start=1)
    _assert_valid_tour(cost_matrix, route, start=1)
    assert cost == _route_cost(cost_matrix, route)


def test_mst_returns_valid_route():
    """MST approximation returns a valid tour and its cost matches the route."""
    cost_matrix = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
    route, cost = solve_tsp_mst(cost_matrix, start=2)
    _assert_valid_tour(cost_matrix, route, start=2)
    assert cost == _route_cost(cost_matrix, route)


def test_real_dataset_all_starts():
    """All algorithms should return valid tours for each start city in the real dataset."""
    graph = _load_graph()
    for start in range(graph.n):
        dp_route, dp_cost, _ = solve_tsp_dp_detailed(graph.cost_matrix, start=start)
        greedy_route, greedy_cost, _ = solve_tsp_greedy_detailed(graph.cost_matrix, start=start)
        mst_route, mst_cost, _ = solve_tsp_mst_detailed(graph.cost_matrix, start=start)

        _assert_valid_tour(graph.cost_matrix, dp_route, start)
        _assert_valid_tour(graph.cost_matrix, greedy_route, start)
        _assert_valid_tour(graph.cost_matrix, mst_route, start)

        assert dp_cost == _route_cost(graph.cost_matrix, dp_route)
        assert greedy_cost == _route_cost(graph.cost_matrix, greedy_route)
        assert mst_cost == _route_cost(graph.cost_matrix, mst_route)
        assert dp_cost <= greedy_cost
        assert dp_cost <= mst_cost


if __name__ == "__main__":
    test_empty_graph()
    test_single_city()
    test_two_cities()
    test_three_cities_symmetric()
    test_graph_from_dict()
    test_greedy_returns_valid_route()
    test_mst_returns_valid_route()
    test_real_dataset_all_starts()
    print("All automated checks passed.\n")
    print_detailed_report()
