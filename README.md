# Couverture réactive par constellation de satellites — Projet Optimisation ISAE 3A COS

Projet en binôme (C. Pralet, ONERA, 2026-2027). Soutenance le 20/11/26, rendu le 04/12/26.

## Installation
```bash
python -m venv .venv && source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install gurobipy pandas matplotlib ipykernel
```
**Gurobi** : la licence d'essai pip est limitée en taille (≈2000 variables/contraintes) et ne suffit pas pour
`data4` / `data2`. Chacun doit demander sa **licence académique gratuite** (compte Gurobi avec mail universitaire,
puis `grbgetkey <clé>` depuis le réseau de l'école ou le VPN).

## Structure
```
data/                                  instances (data12, data4, data2) + solutions fournies
src/reactive_covering.ipynb            notebook fourni (solveur de base aléatoire)
src/solution1_reactive_covering.ipynb  MILP passages complets (data12)
src/solution2_reactive_covering.ipynb  MILP passages partiels (data12)
src/etude_complete.ipynb               étude complète : métriques, glouton, MILP, comparaison 3 instances, Pareto
src/countries.geo.json                 fond de carte pour plotSolution
```
Les notebooks se lancent depuis `src/` (les données sont lues dans `../data/`).

## Modèles
- `x_p ∈ {0,1}` : passage p réservé ; en partiel `debut_p`, `fin_p` (fenêtre réservée) et `z_a ∈ {0,1}` (accès couvert)
- accès couvert si le chevauchement fenêtre / accès ≥ `minVisiDuration` (30 s)
- coût = Σ (`fixedPassCost` + `passCostPerTimeUnit` × durée réservée)
- objectif : min coût en satisfaisant tout, ou max satisfaction pondérée sous `coût ≤ budget` (Pareto)

## Résultats (coût minimal, toutes requêtes satisfaites, ≤ 2 min)
| instance | solution fournie | glouton complets | MILP complets | glouton partiels | MILP partiels |
|---|---|---|---|---|---|
| data12 | 3245 | 2122 | 1525 (opt.) | 1453 | 1078 |
| data4  | 14870 | 10021 | 9991 (opt.) | 6258 | ≈5995 |
| data2  | 19824 | 17055 | 16847 (opt.) | 11372 | 10872 (opt.) |

## Travail à deux
Une branche par fonctionnalité (`git switch -c feat/xxx`), pull request, relecture par l'autre.
Notebooks : `nbstripout --install` pour éviter des diffs énormes.
