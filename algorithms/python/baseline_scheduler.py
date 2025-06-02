import time                      # Pour mesurer la durée d'exécution des algorithmes
import pandas as pd              # Pour gérer facilement les données en tableau (DataFrame) et exporter en CSV
import matplotlib.pyplot as plt  # Pour tracer les graphiques (barres, Gantt, etc.)
import seaborn as sns            # Pour améliorer le style et la lisibilité des graphiques matplotlib

# ----------- DÉFINITION DES DONNÉES ------------
# Dictionnaire des tâches
# Chaque tâche est définie par :
#   durée (int),
#   compétences requises (liste de chaînes),
#   liste des tâches prédécesseurs (liste de chaînes),
#   importance (int)

# Exemple de tâches
# task_id: (durée, [compétences nécessaires], [prédécesseurs], importance)
tasks = {
    'A': (4, ['dev'], [], 10),
    'B': (3, ['dev'], ['A'], 8),
    'C': (2, ['test'], ['A'], 6),
    'D': (5, ['dev', 'test'], ['B', 'C'], 9),
    'E': (3, ['dev'], ['C'], 5),
}

tasks = {
    'users': (3, ['dev'], [], 10),
    'assureurs': (2, ['dev'], [], 8),
    'offres': (4, ['dev'], ['users', 'assureurs'], 6),
    'contrats': (5, ['dev', 'test'], ['users', 'assureurs'], 9),
    'paiement': (3, ['dev', 'test'], ['contrats'], 5),
    'notification': (2, ['dev'], ['paiement', 'users'], 7),
    'reclamation': (4, ['dev'], ['users', 'contrats'], 6),
    'client': (3, ['dev'], ['users'], 5),
    'echange': (2, ['dev'], ['contrats'], 4),
    'document': (3, ['dev'], ['users'], 8),
    'message': (2, ['dev'], ['users', 'assureurs'], 7),
    'renouvellement': (4, ['dev'], ['users', 'contrats'], 9),
}

# Ressources disponibles par compétence
resources = {'dev': 2, 'test': 1}

# ----------- PRIORITÉS -------------
# Fonctions qui définissent les priorités pour le tri des tâches prêtes
# Par exemple, shortest processing time (SPT),
# longest, nombre de successeurs, importance


def prio_shortest(task):
    # Durée la plus courte (SPT)
    # Renvoie la durée de la tâche
    # La tâche avec la durée la plus courte sera priorisée
    # pour être exécutée en premier
    # (tâche la plus courte en premier)
    # (Shortest Processing Time)
    # (SPT)
    return tasks[task][0]


def prio_longest(task):
    # Durée la plus longue (LPT)
    # Renvoie la durée de la tâche
    # La tâche avec la durée la plus longue sera priorisée
    # pour être exécutée en premier
    # (tâche la plus longue en premier)
    # (Longest Processing Time)
    # (LPT)
    return -tasks[task][0]


def prio_most_successors(task):
    # Compte combien de tâches ont 'task' comme prédécesseur
    # Renvoie le nombre de successeurs directs
    # La tâche avec le plus de successeurs sera priorisée
    # pour être exécutée en premier
    # (tâche avec le plus de successeurs en premier)
    # (Most Successors)
    # (MS)
    return -sum(1 for t in tasks if task in tasks[t][2])


def prio_most_important(task):
    # Renvoie l'importance de la tâche
    # La tâche la plus importante sera priorisée
    # pour être exécutée en premier
    # (tâche la plus importante en premier)
    # (Most Important)
    # (MI)
    return -tasks[task][3]


priorities = {
    'shortest': prio_shortest,
    'longest': prio_longest,
    'most_successors': prio_most_successors,
    'important': prio_most_important,
}

# ----------- ALGORITHMES -------------
# Ordonnancement parallèle avec gestion des ressources
#  et contraintes de précédence


def schedule_parallel(prio_func):
    time_now = 0                   # Horloge du système
    schedule = []                  # Liste des tâches programmées (id, start, end)
    finished = set()               # Ensemble des tâches terminées
    running = []                   # Liste des tâches en cours (id, fin)
    remaining = set(tasks.keys())  # Tâches restantes à programmer
    skill_usage = {k: 0 for k in resources}  # Compteur d'utilisation des ressources

    while remaining or running:
        # Libérer les ressources des tâches terminées à l'instant courant
        for t, end in running[:]:
            if end <= time_now:
                running.remove((t, end))
                finished.add(t)
                for skill in tasks[t][1]:
                    skill_usage[skill] -= 1

        # Identifier les tâches prêtes à démarrer (prédécesseurs finis)
        ready = [t for t in remaining if all(p in finished for p in tasks[t][2])]
        ready.sort(key=prio_func)  # Trier selon la fonction de priorité choisie

        # Lancer les tâches prêtes si ressources disponibles
        for t in ready:
            skills = tasks[t][1]
            if all(skill_usage[s] < resources[s] for s in skills):
                for s in skills:
                    skill_usage[s] += 1
                start = time_now
                end = start + tasks[t][0]
                schedule.append((t, start, end))
                running.append((t, end))
                remaining.remove(t)

        # Avancer le temps au prochain événement (fin de tâche)
        if running:
            time_now = min(end for _, end in running)
        else:
            break

    makespan = max(e for _, _, e in schedule) if schedule else 0
    return schedule, makespan

# Ordonnancement en série (une tâche à la fois) avec contraintes de précédence


def schedule_series(prio_func):
    schedule = []
    finished = set()
    remaining = set(tasks.keys())
    current_time = 0

    while remaining:
        ready = [t for t in remaining if all(p in finished for p in tasks[t][2])]
        if not ready:
            raise RuntimeError("Cycle détecté ou problème de précédence")

        ready.sort(key=prio_func)
        t = ready[0]
        dur, skills, _, _ = tasks[t]

        start = current_time
        end = start + dur
        schedule.append((t, start, end))
        finished.add(t)
        remaining.remove(t)
        current_time = end

    makespan = max(e for _, _, e in schedule) if schedule else 0
    return schedule, makespan

# ----------- TRACÉ GANTT -------------


def plot_gantt(schedule, ax, title):
    # Préparer l'axe Y avec les noms des tâches
    task_names = sorted(set(t for t, _, _ in schedule))
    task_pos = {t: i for i, t in enumerate(task_names)}

    # Tracer une barre horizontale par tâche
    for t, start, end in schedule:
        ax.barh(task_pos[t], end-start, left=start, height=0.4)
        ax.text(start + (end-start)/2, task_pos[t], t, va='center', ha='center', color='white', fontsize=9)

    ax.set_yticks(list(task_pos.values()))
    ax.set_yticklabels(task_names)
    ax.set_xlabel('Temps')
    ax.set_title(title)
    ax.invert_yaxis()  # Inverser l'axe Y pour avoir la tâche A en haut

# ----------- EXÉCUTION ET COMPARAISON -------------


def run_all():
    results = []
    schedules_for_gantt = []

    # Tester tous les algorithmes (parallèle et série) avec toutes les priorités
    for algo_type in ['parallel', 'series']:
        for prio_name, prio_func in priorities.items():
            start_time = time.time()    # Démarrer le chrono
            if algo_type == 'parallel':
                sched, mksp = schedule_parallel(prio_func)
            else:
                sched, mksp = schedule_series(prio_func)
            duration = time.time() - start_time  # Mesurer durée d'exécution
            results.append({
                'algo': algo_type,
                'priority': prio_name,
                'makespan': mksp,
                'duration_sec': duration
            })
            schedules_for_gantt.append((
                sched,
                f"{algo_type.capitalize()} - {prio_name}"
                ))
            print(f"[{algo_type} - {prio_name}] Makespan: {mksp}, Durée: {duration:.4f}s")

    # Exporter résultats dans un fichier CSV
    df = pd.DataFrame(results)
    df.to_csv('figures/comparison_ms_rcpsp.csv', index=False)

    # Tracer graphiques comparatifs pour le makespan
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='priority', y='makespan', hue='algo')
    plt.title("Makespan selon algorithme et priorité")
    plt.savefig("figures/makespan_comparison.png")
    plt.show()

    # Tracer graphiques comparatifs pour la durée d'exécution
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='priority', y='duration_sec', hue='algo')
    plt.title("Durée d'exécution selon algorithme et priorité")
    plt.savefig("figures/duration_comparison.png")
    plt.show()

    # Afficher les diagrammes de Gantt pour chaque ordonnancement testé
    fig, axs = plt.subplots(4, 2, figsize=(20, 16), sharex=True)
    for ax, (sched, title) in zip(axs.flatten(), schedules_for_gantt):
        plot_gantt(sched, ax, title)
    plt.tight_layout()
    plt.savefig("figures/gantt_schedules.png")
    plt.show()

    fig_index = 1

    for algo_type in ['parallel', 'series']:
        for prio_name, prio_func in priorities.items():
            start_time = time.time()
            if algo_type == 'parallel':
                sched, mksp = schedule_parallel(prio_func)
            else:
                sched, mksp = schedule_series(prio_func)
            duration = time.time() - start_time
            results.append({
                'algo': algo_type,
                'priority': prio_name,
                'makespan': mksp,
                'duration_sec': duration
            })

            # Affichage console
            print(f"[{algo_type} - {prio_name}] Makespan: {mksp}, Durée: {duration:.4f}s")

            # Tracer et sauvegarder figure Gantt individuelle
            fig, ax = plt.subplots(figsize=(10, 4))
            plot_gantt(sched, ax, f"{algo_type.capitalize()} - {prio_name}")
            plt.tight_layout()
            plt.savefig(f"figures/gantt_schedule_{fig_index}_{algo_type}_{prio_name}.png")
            plt.show()
            plt.close(fig)
            fig_index += 1

# Point d'entrée du script


if __name__ == "__main__":
    run_all()
