import json


def load_data(path):
    with open(path) as f:
        return json.load(f)


def save_solution(bookings, path):
    with open(path, "w") as f:
        json.dump({"Bookings": bookings}, f)


def load_solution(path):
    with open(path) as f:
        return json.load(f)


def full_booking(p, pass_id):
    """Réservation d'un passage complet."""
    return {"passId": pass_id, "passStart": p["start"], "passEnd": p["end"],
            "bookingStart": p["start"], "bookingEnd": p["end"]}
