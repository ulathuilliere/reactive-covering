"""Usage : python run_milp.py data/data12.json [max_cost]"""
import sys
from src.io_utils import load_data, save_solution
from src.milp_complete import build_and_solve
from src.evaluate import evaluate

path = sys.argv[1]
max_cost = float(sys.argv[2]) if len(sys.argv) > 2 else None
data = load_data(path)
sol, model = build_and_solve(data, max_cost=max_cost, verbose=True)
name = path.split("/")[-1].replace("data", "milp_solution")
save_solution(sol["Bookings"], f"results/{name}")
print(evaluate(data, sol))
