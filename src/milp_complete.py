"""MILP Gurobi — passages complets.

x[p] = 1 si le passage p est réservé en entier
y[r] = 1 si la requête r est satisfaite (au moins un accès de A_r couvert)
"""
import gurobipy as gp
from gurobipy import GRB
from .io_utils import full_booking


def pass_cost(data, p):
    return data["fixedPassCost"] + data["passCostPerTimeUnit"] * (p["end"] - p["start"])


def usable_accesses(data):
    """Accès couvrables par un passage complet (durée >= minVisiDuration)."""
    m = data["minVisiDuration"]
    return {i: a["passId"] for i, a in enumerate(data["Accesses"]) if a["end"] - a["start"] >= m}


def build_and_solve(data, weights=None, max_cost=None, time_limit=120, mip_gap=0.0, verbose=False):
    """
    weights : poids par priorité {1: w1, 2: w2, 3: w3} (défaut : tous à 1)
    max_cost: contrainte de coût max (epsilon-contrainte) ; sinon le coût est
              pénalisé dans l'objectif avec un poids très faible (départage à satisfaction égale)
    """
    weights = weights or {1: 1, 2: 1, 3: 1}
    P, R = data["Passes"], data["ObservationRequests"]
    acc_pass = usable_accesses(data)

    m = gp.Model("reactive_covering")
    m.Params.OutputFlag = int(verbose)
    m.Params.TimeLimit = time_limit
    m.Params.MIPGap = mip_gap

    x = m.addVars(len(P), vtype=GRB.BINARY, name="x")
    y = m.addVars(len(R), vtype=GRB.BINARY, name="y")

    for r, req in enumerate(R):
        passes_r = {acc_pass[a] for a in req["accessIds"] if a in acc_pass}
        m.addConstr(y[r] <= gp.quicksum(x[p] for p in passes_r), name=f"cov_{r}")

    total_cost = gp.quicksum(pass_cost(data, P[p]) * x[p] for p in range(len(P)))
    sat = gp.quicksum(weights[R[r]["priority"]] * y[r] for r in range(len(R)))
    if max_cost is not None:
        m.addConstr(total_cost <= max_cost, name="budget")
        m.setObjective(sat, GRB.MAXIMIZE)
    else:
        m.setObjective(sat - 1e-4 * total_cost, GRB.MAXIMIZE)
    m.optimize()

    bookings = [full_booking(P[p], p) for p in range(len(P)) if x[p].X > 0.5] if m.SolCount else []
    return {"Bookings": bookings}, m
