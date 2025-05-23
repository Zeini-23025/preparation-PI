# Ordonnancement MS-RCPSP (Multi-Skill Resource-Constrained Project Scheduling Problem)

Ce projet propose une implémentation Python d’algorithmes pour résoudre le problème MS-RCPSP, un problème d’ordonnancement de tâches avec contraintes de ressources et de compétences multiples.

---

## Description

Le MS-RCPSP vise à planifier des tâches nécessitant différentes compétences, sous contraintes de précédence et de capacité des ressources. L’objectif est de minimiser le **makespan** (durée totale du projet) en tenant compte des disponibilités et des priorités.

Deux approches d’ordonnancement sont comparées :

- **Parallèle** : plusieurs tâches peuvent être exécutées simultanément si les ressources le permettent.
- **Série** : les tâches sont exécutées une à une selon un ordre de priorité.

Critères de priorité disponibles :

- Durée la plus courte (`shortest`)
- Durée la plus longue (`longest`)
- Plus grand nombre de successeurs (`most_successors`)
- Importance maximale (`important`)

---

## Données

- **Tâches** : définies par leur durée, compétences requises, prédécesseurs et importance.
- **Ressources** : chaque compétence a une capacité limitée.

---

## Installation

Assurez-vous d’avoir Python 3, puis installez les dépendances :

```bash
pip install pandas matplotlib seaborn
```

---

## Exécution

Lancez le script principal :

```bash
python main.py
```

Cela génère :

- Un fichier CSV `comparison_ms_rcpsp.csv` avec les résultats.
- Des graphiques PNG comparant le makespan et la durée d’exécution.
- Des diagrammes de Gantt pour la visualisation des plannings.

---

## Structure du code

- `tasks` : dictionnaire des tâches (durée, compétences, prédécesseurs, importance)
- `resources` : dictionnaire des capacités par compétence
- Fonctions d’ordonnancement : `schedule_parallel()`, `schedule_series()`
- Fonctions de priorité : `prio_shortest()`, `prio_longest()`, `prio_most_successors()`, `prio_most_important()`
- Visualisation : `plot_gantt()`

---

## Remarques

- Les ressources sont allouées/libérées dynamiquement.
- La version série suppose une disponibilité infinie des ressources.
- Un cycle dans les précédences génère une erreur.

---

## Exemple d’utilisation

1. Placez vos fichiers de données dans le dossier `data/`.
2. Exécutez le script principal :
    ```bash
    python main.py
    ```
3. Consultez les résultats dans `comparison_ms_rcpsp.csv` et les graphiques dans `figures/`.

---

## Contact

Pour toute question ou suggestion, contactez l’auteur du projet.
