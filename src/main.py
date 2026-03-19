"""
Global Explorer Route Optimizer - Entry point.
CS 5800 Algorithms Final Project
"""

import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from graph import TravelGraph
from tsp_dp import solve_tsp_dp
from tsp_approx import solve_tsp_greedy, solve_tsp_mst


def main():
    # Load sample data
    data_path = Path(__file__).parent.parent / "data" / "cities.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    graph = TravelGraph.from_dict(data)
    cost_matrix = graph.cost_matrix
    cities = graph.cities

    print("Global Explorer Route Optimizer")
    print("=" * 40)
    print(f"Cities: {', '.join(cities)}\n")

    # Run algorithms (placeholders for now)
    route_dp, cost_dp = solve_tsp_dp(cost_matrix)
    route_greedy, cost_greedy = solve_tsp_greedy(cost_matrix)
    route_mst, cost_mst = solve_tsp_mst(cost_matrix)

    print("DP (Held-Karp):     ", [cities[i] for i in route_dp], f"-> cost: {cost_dp}")
    print("Greedy:             ", [cities[i] for i in route_greedy], f"-> cost: {cost_greedy}")
    print("MST 2-approx:       ", [cities[i] for i in route_mst], f"-> cost: {cost_mst}")
    print("\n(Note: algorithms are placeholders; full implementation in progress)")


if __name__ == "__main__":
    main()
