# Couverture réactive par constellation de satellites — Projet Optimisation ISAE 3A COS

Projet en binôme (C. Pralet, ONERA, 2026-2027). Soutenance le 20/11/26, rendu le 04/12/26.

## Installation
```bash
python -m venv .venv && source .venv/bin/activate   # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```
**Gurobi** : la licence d'essai pip est limitée en taille (≈2000 variables/contraintes) et ne suffit pas pour
`data4` / `data2`. Chacun doit demander sa **licence académique gratuite** (compte Gurobi avec mail universitaire,
puis `grbgetkey <clé>` depuis le réseau de l'école ou le VPN).

## Données
L'énoncé et les données appartiennent à l'ONERA : ils sont dans le `.gitignore`.
Copier `data12.json`, `data4.json`, `data2.json` (et `countries.geo.json` pour les cartes) dans `data/`.

## Structure
```
src/io_utils.py       lecture données / écriture solution JSON
src/evaluate.py       coût + requêtes satisfaites par priorité (métriques de l'étape 1)
src/milp_complete.py  MILP Gurobi, passages complets (étape 2)
src/pareto.py         front de Pareto coût / satisfaction par epsilon-contrainte (étape 4)
run_milp.py           python run_milp.py data/data12.json [coût_max]
notebooks/            notebook final (.ipynb) à rendre
results/              solutions générées
```

## Modèle (passages complets)
- `x_p ∈ {0,1}` : passage p réservé ; `y_r ∈ {0,1}` : requête r satisfaite
- `y_r ≤ Σ x_p` sur les passages couvrant un accès de `A_r` (durée d'accès ≥ `minVisiDuration`)
- coût = Σ (`fixedPassCost` + `passCostPerTimeUnit` × durée) · `x_p`
- objectif : max Σ w_prio(r)·y_r − ε·coût, ou max satisfaction sous `coût ≤ budget`

## Résultat de départ
`data12` : 4 passages, coût 1525, 225/225 requêtes satisfaites (optimal prouvé).

## Pistes
- passages partiels (étape 3) : variables de début/fin par passage
- heuristique gloutonne / recherche locale pour comparer au MILP
- front de Pareto (`src/pareto.py`)

## Travail à deux
Une branche par fonctionnalité (`git switch -c feat/glouton`), pull request, relecture par l'autre.
Notebooks : `nbstripout --install` pour éviter des diffs énormes.
