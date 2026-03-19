"""
Basic test cases for TSP algorithms.
Joshua: Testing
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from graph import TravelGraph
from tsp_dp import solve_tsp_dp
from tsp_approx import solve_tsp_greedy, solve_tsp_mst


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
    assert len(route) == 2
    assert set(route) == {0, 1}
    assert cost == 20.0


def test_three_cities_symmetric():
    """Three cities with symmetric costs."""
    cost_matrix = [
        [0, 1, 2],
        [1, 0, 3],
        [2, 3, 0],
    ]
    route, cost = solve_tsp_dp(cost_matrix)
    assert len(route) == 3
    assert set(route) == {0, 1, 2}
    # Optimal for this graph: 0->1->2->0 = 1+3+2 = 6
    assert cost == 6.0


def test_graph_from_dict():
    """TravelGraph loads correctly from dict."""
    data = {
        "cities": ["A", "B", "C"],
        "cost_matrix": [[0, 1, 2], [1, 0, 3], [2, 3, 0]],
    }
    g = TravelGraph.from_dict(data)
    assert g.cities == ["A", "B", "C"]
    assert g.get_cost(0, 1) == 1
    assert g.get_city_name(2) == "C"


def test_greedy_returns_valid_route():
    """Greedy returns a valid tour (all cities, returns to start)."""
    cost_matrix = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
    route, cost = solve_tsp_greedy(cost_matrix)
    assert len(route) == 3
    assert set(route) == {0, 1, 2}
    assert cost >= 0


def test_mst_returns_valid_route():
    """MST approx returns a valid tour."""
    cost_matrix = [[0, 1, 2], [1, 0, 3], [2, 3, 0]]
    route, cost = solve_tsp_mst(cost_matrix)
    assert len(route) == 3
    assert set(route) == {0, 1, 2}
    assert cost >= 0


if __name__ == "__main__":
    # Run with: python tests/test_tsp.py
    test_empty_graph()
    test_single_city()
    test_two_cities()
    test_three_cities_symmetric()
    test_graph_from_dict()
    test_greedy_returns_valid_route()
    test_mst_returns_valid_route()
    print("All tests passed.")
