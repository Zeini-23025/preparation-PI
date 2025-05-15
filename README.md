# Ordonnancement MC-RCPSP (Multi-Criteria Resource-Constrained Project Scheduling Problem)

Ce projet implémente un algorithme d'ordonnancement de tâches sous contraintes de ressources, avec prise en compte du coût et du temps d'exécution. Deux implémentations sont proposées : l'une en **Python**, l'autre en **C++**.

## Structure du projet

```
project/
├── src/
│   ├── main.py        # Entrée principale Python
│   └── main.cpp       # Entrée principale C++
├── exp/
│   ├── code_1.py      # Code détaillé en Python
│   └── code_1.cpp     # Code détaillé en C++
└── README.md
```

## Fonctionnalités

- Programmation des tâches avec dépendances.
- Gestion des ressources limitées.
- Optimisation du coût total.
- Calcul du makespan (durée totale du projet).
- Affichage d’un diagramme de Gantt (version Python uniquement).

## Exécution

### Python

1. Assurez-vous d'avoir Python 3 et `matplotlib` installés :
```bash
pip install matplotlib
```

2. Lancez le programme :
```bash
python src/main.py
```

### C++

1. Compilez avec g++ :
```bash
g++ src/main.cpp -o schedule
```

2. Exécutez :
```bash
./schedule
```

## Auteurs

- Implémentation Python et C++ par notre équipe de projet.
