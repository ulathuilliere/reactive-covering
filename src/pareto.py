"""Front de Pareto coût / satisfaction par epsilon-contrainte."""
from .milp_complete import build_and_solve
from .evaluate import evaluate


def pareto_front(data, budgets, time_limit=120):
    pts = []
    for b in budgets:
        sol, _ = build_and_solve(data, max_cost=b, time_limit=time_limit)
        ev = evaluate(data, sol)
        pts.append((ev["cost"], ev["nSatisfied"], ev))
    return pts
