"""Évaluation d'une solution : coût, requêtes satisfaites (par priorité)."""


def covered_accesses(data, bookings):
    """Ensemble des accès couverts (>= minVisiDuration dans la réservation)."""
    min_d = data["minVisiDuration"]
    cov = set()
    for b in bookings:
        p = data["Passes"][b["passId"]]
        for aid in p["accessIds"]:
            a = data["Accesses"][aid]
            overlap = min(a["end"], b["bookingEnd"]) - max(a["start"], b["bookingStart"])
            if overlap >= min_d:
                cov.add(aid)
    return cov


def cost(data, bookings):
    return sum(data["fixedPassCost"] + data["passCostPerTimeUnit"] * (b["bookingEnd"] - b["bookingStart"])
               for b in bookings)


def evaluate(data, solution):
    bookings = solution["Bookings"]
    ids = [b["passId"] for b in bookings]
    assert len(ids) == len(set(ids)), "au plus une réservation par passage"
    cov = covered_accesses(data, bookings)
    sat = {1: 0, 2: 0, 3: 0}
    tot = {1: 0, 2: 0, 3: 0}
    for r in data["ObservationRequests"]:
        tot[r["priority"]] += 1
        if any(a in cov for a in r["accessIds"]):
            sat[r["priority"]] += 1
    return {"cost": cost(data, bookings), "nPasses": len(bookings),
            "satisfied": sat, "total": tot,
            "nSatisfied": sum(sat.values()), "nTotal": sum(tot.values())}
