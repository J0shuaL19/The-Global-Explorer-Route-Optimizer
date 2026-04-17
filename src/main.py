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
from tsp_dp import solve_tsp_dp_detailed
from tsp_approx import solve_tsp_greedy_detailed, solve_tsp_mst_detailed


def _format_number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:.2f}"


def _format_route(graph: TravelGraph, route):
    return " -> ".join(graph.route_to_names(route, include_return=True))


def main():
    data_path = Path(__file__).parent.parent / "data" / "cities.json"
    with open(data_path, encoding="utf-8") as f:
        data = json.load(f)

    graph = TravelGraph.from_dict(data)
    cost_matrix = graph.cost_matrix

    print("Global Explorer Route Optimizer")
    print("=" * 92)
    print(data.get("description", "No dataset description provided."))
    print(f"Cities ({graph.n}): {', '.join(graph.cities)}")

    for start, city_name in enumerate(graph.cities):
        dp_route, dp_cost, dp_steps = solve_tsp_dp_detailed(cost_matrix, start=start)
        greedy_route, greedy_cost, greedy_steps = solve_tsp_greedy_detailed(
            cost_matrix, start=start
        )
        mst_route, mst_cost, mst_steps = solve_tsp_mst_detailed(cost_matrix, start=start)

        runs = [
            ("DP (Held-Karp)", dp_route, dp_cost, dp_steps),
            ("Greedy", greedy_route, greedy_cost, greedy_steps),
            ("MST 2-approx", mst_route, mst_cost, mst_steps),
        ]

        print(f"\nStart city: {city_name}")
        print("-" * 92)
        print(f"{'Algorithm':<18}{'Cost':>10}{'Steps':>10}{'Gap vs DP':>12}  Route")
        for algorithm, route, cost, steps in runs:
            gap = 0.0 if dp_cost == 0 else ((cost - dp_cost) / dp_cost) * 100
            print(
                f"{algorithm:<18}{_format_number(cost):>10}{steps:>10}"
                f"{gap:>11.2f}%  {_format_route(graph, route)}"
            )


if __name__ == "__main__":
    main()
