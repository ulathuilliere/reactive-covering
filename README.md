# Couverture réactive par constellation de satellites

Projet optimisation ISAE 3A COS (C. Pralet, ONERA, 2026-2027), en binôme.
Soutenance le 20/11/26, rendu le 04/12/26. Sujet : `talkReactiveCovering.pdf`.

## Installation

```bash
python -m venv .venv && source .venv/bin/activate
pip install gurobipy matplotlib jupyter
```

La licence Gurobi installée par pip est limitée (environ 2000 variables/contraintes). Elle suffit pour `sol12_1`
mais pas pour les autres notebooks. Il faut la licence académique (compte Gurobi avec l'adresse de l'école,
puis `grbgetkey <clé>` depuis le réseau de l'école ou le VPN).

## Organisation

```
data/      data12/4/2.json, solutions fournies solution12/4/2.json, countries.geo.json
src/       notebooks (à lancer depuis src/, les chemins sont en ../data et ../results)
results/   solutions produites, results/<notebook>.json (ex. results/sol12_1.json)
```

Les trois jeux de données ont les mêmes 69 passages et 3571 accès, seules les requêtes changent :

| | requêtes | priorités |
|---|---|---|
| data12 | 225 | 225 de prio 1 (une par AOI) |
| data4 | 2234 | 225 prio 1, 2009 prio 2 |
| data2 | 6867 | 225 prio 1, 2009 prio 2, 4633 prio 3 |

## Notebooks

Base commune : chargement des données, `evaluate` (coût, requêtes satisfaites par priorité, AOIs couvertes ;
un accès est couvert si la réservation le recouvre au moins 30 s) et `plotSolution`.
Sur data12 on maximise d'abord le nombre de requêtes satisfaites puis on minimise le coût (`solve_lexico`).

- `sol12_1` : passages complets. Une binaire par passage, chaque requête doit être couverte par un passage
  qui contient un de ses accès. On paie tout le passage. Couverture d'ensembles classique, résolue tout de suite.
- `sol12_2` : passages partiels avec big-M. Début et fin par passage, une binaire par accès couvert. On ne paie
  que la durée réservée. Bonne solution trouvée vite mais pas de preuve d'optimum en 2 min (big-M trop faible).
- `sol12_3` : même problème que le 2, autre modèle. Dans une fenêtre optimale le début vaut `fin d'un accès - 30`
  et la fin `début d'un accès + 30` (ou `début + 30`). On énumère toutes ces fenêtres (63 034, les mêmes pour les
  trois jeux de données) et on en choisit au plus une par passage. Relaxation beaucoup plus forte.
- `sol4`, `sol2` : modèle 3 adapté à data4 et data2.
  - Pas de phase "max requêtes" : la plus grande fenêtre de chaque passage couvre tous ses accès, donc toutes les
    requêtes sont satisfiables en même temps. On les impose directement et on minimise le coût.
  - Une variable `z_a` par accès (accès couvert) au lieu de sommer les fenêtres de chaque requête : environ 2.9M
    non-zéros au lieu de 11M (data4) et 20M (data2).
  - Solution de départ donnée à Gurobi : la plus grande fenêtre de chaque passage.

## Résultats

| | passages | coût | requêtes |
|---|---|---|---|
| data12, solution fournie | 9 | 3245 | 225/225 |
| data12, `sol12_1` | 4 | 1525 (optimal) | 225/225 |
| data12, `sol12_2` / `sol12_3` | 4 | 1078 (optimal) | 225/225 |
| data4, solution fournie | 43 | 14870 | 2234/2234 |
| data4, `sol4` | | à mesurer | |
| data2, solution fournie | 58 | 19824 | 6867/6867 |
| data2, `sol2` | 47 | 10872 (optimal) | 6867/6867 |

La solution fournie vient d'un glouton qui prend les passages dans un ordre aléatoire et réserve chaque passage
en entier, d'où le coût élevé.

Les optimums 1078 et 10872 ont aussi été vérifiés avec HiGHS sur le modèle de `sol12_3` / `sol2`. Sur data4, HiGHS n'a pas
trouvé de solution en 300 s (sans solution de départ) : c'est le cas le plus dur, à tester avec Gurobi.

## Suite

- data4 : vérifier le gap obtenu en 2 min, sinon ajouter une meilleure solution de départ (glouton)
- heuristique gloutonne / recherche locale pour comparer au MILP
- front de Pareto coût / satisfaction (contrainte de coût max), avec les priorités

## Travail à deux

Une branche par fonctionnalité, pull request, relecture par l'autre.
`nbstripout --install` pour éviter les gros diffs sur les notebooks.
