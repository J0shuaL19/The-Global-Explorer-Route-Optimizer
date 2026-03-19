# Global Explorer Route Optimizer

**CS 5800 Algorithms — Final Project**  
*Traveling Salesperson Problem (TSP) for Multi-City Trip Planning*

---

## Team

| Member | Role | Responsibilities |
|--------|------|------------------|
| Chengling (Charlene) Lv | Graph & DP | Graph modeling, Held-Karp (DP TSP), experiment design |
| Jiaying (Jasmine) Guo | Data & Approximation | Data collection, MST/greedy algorithms, visualization |
| Ziyong (Joshua) Liu | Testing & Docs | Testing, benchmarking, pseudocode, report & slides |

---

## Overview

Planning a multi-city trip is a puzzle: choosing the wrong order of cities can blow up costs and travel time. This project uses graph algorithms to find the **optimal route** that visits each city once and returns home with minimum cost or time.

- **Input:** Cities (nodes) and travel costs/times between them (weighted edges)
- **Output:** An optimal or near-optimal route visiting all cities once
- **Approach:** Exact solution via Held-Karp (DP), plus approximation algorithms (MST-based, greedy)

---

## Project Scope

- 5–8 cities
- Constant travel costs between cities (static graph)
- Exact solution using dynamic programming (Held-Karp)
- Approximation algorithms for comparison
- Focus on core algorithm logic (no real-time traffic, dynamic pricing, or schedules)

---

## Project Structure

```
CS5800/
├── src/
│   ├── graph.py          # Graph model of travel network
│   ├── tsp_dp.py         # Held-Karp (DP) exact solution
│   ├── tsp_approx.py     # MST-based and greedy approximations
│   └── main.py           # Entry point
├── data/
│   └── cities.json       # City dataset and travel costs
├── tests/
│   └── test_tsp.py       # Basic test cases
├── requirements.txt
└── README.md
```

---

## Setup

```bash
# Clone the repository
git clone <repository-url>
cd CS5800

# Create virtual environment (recommended)
python -m venv venv
venv\Scripts\activate   # Windows
# source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/ -v
```

---

## Usage

```bash
python src/main.py
```

---

## 5-Week Plan

| Week | Focus |
|------|-------|
| 1 | Data collection & graph modeling |
| 2 | Held-Karp (DP) exact solution |
| 3 | Approximation algorithms (MST, greedy) |
| 4 | Evaluation & visualization |
| 5 | Final report & presentation |

---

## License

MIT (or as required by course)
