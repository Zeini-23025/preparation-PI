# Ordonnancement MS-RCPSP (Multi-Skill Resource-Constrained Project Scheduling Problem)

Ce projet propose une implémentation en **Python** *et* en **C++** d’algorithmes pour résoudre le problème MS-RCPSP, un problème d’ordonnancement de tâches avec contraintes de ressources et de compétences multiples.

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

## Installation (Python)

Assurez-vous d’avoir Python 3, puis installez les dépendances :

```bash
pip install pandas matplotlib seaborn
```

---

## Exécution Python

Lancez le script principal :

```bash
python main.py
```

Cela génère :

- Un fichier CSV `comparison_ms_rcpsp.csv` avec les résultats.
- Des graphiques PNG comparant le makespan et la durée d’exécution.
- Des diagrammes de Gantt pour la visualisation des plannings.

---

## Exécution C++

Une version C++ du projet est disponible dans le fichier `main.cpp`.  
Cette version permet également de calculer le makespan et d’afficher l’ordre d’exécution des tâches avec leur heure de début et de fin.

### Compilation :

```bash
g++ main.cpp -o main
```

### Exécution :

```bash
./main
```

La sortie affiche l’ordre des tâches, leurs temps de démarrage et de fin, ainsi que le makespan.

---

## Structure du code

- `tasks` : dictionnaire des tâches (durée, compétences, prédécesseurs, importance)
- `resources` : dictionnaire des capacités par compétence
- Fonctions d’ordonnancement (Python) : `schedule_parallel()`, `schedule_series()`
- Fonctions de priorité : `prio_shortest()`, `prio_longest()`, `prio_most_successors()`, `prio_most_important()`
- Visualisation (Python) : `plot_gantt()`
- Implémentation C++ dans `main.cpp` : lecture, tri topologique, allocation, affichage détaillé

---

## Remarques

- Les ressources sont allouées/libérées dynamiquement.
- La version série suppose une disponibilité infinie des ressources.
- Un cycle dans les précédences génère une erreur.
- La version C++ affiche également pour chaque tâche :  
  `A -> start: 0, end: 3` ; `C -> start: 3, end: 7` ; etc.

---

## Exemple d’utilisation

1. Placez vos fichiers de données dans le dossier `data/`.
2. Exécutez le script Python :
    ```bash
    python main.py
    ```
3. Ou compilez et exécutez la version C++ :
    ```bash
    g++ main.cpp -o main
    ./main
    ```
4. Consultez les résultats dans `comparison_ms_rcpsp.csv`, les graphiques dans `figures/`, et les ordonnancements en console (C++).

---

