#             ------------------ employés multiskills autorisés  -----------------


import time                      # Pour mesurer la durée d'exécution des algorithmes
import pandas as pd              # Pour manipuler les données tabulaires
import matplotlib.pyplot as plt  # Pour les graphiques (Gantt, comparatifs)
import seaborn as sns            # Pour un meilleur style graphique

# ----------- DÉFINITION DES DONNÉES ------------

# Tâches avec durée, compétences requises, prédécesseurs, importance
tasks = {
    'users': (3, {'dev': 1}, [], 10),
    'assureurs': (2, {'dev': 1}, [], 8),
    'offres': (4, {'dev': 2}, ['users', 'assureurs'], 6),
    'contrats': (5, {'dev': 2, 'test': 1}, ['offres'], 9),
    'paiement': (3, {'dev': 1, 'test': 1}, ['contrats'], 5),
    'notification': (2, {'dev': 1}, ['paiement', 'users'], 7),
    'reclamation': (4, {'dev': 1}, ['users', 'contrats'], 6),
    'client': (3, {'dev': 1}, ['users'], 5),
    'echange': (2, {'dev': 1}, ['contrats'], 4),
    'document': (3, {'dev': 2}, ['users', 'assureurs'], 8),
    'message': (2, {'dev': 1}, ['users', 'assureurs'], 7),
    'renouvellement': (4, {'dev': 2}, ['users', 'assureurs', 'contrats'], 9),
}

# Liste des employés et leurs compétences
employees = [
    {'name': 'Alice', 'skills': ['dev', 'test']},
    {'name': 'Bob', 'skills': ['dev']},
    {'name': 'Charlie', 'skills': ['test']},
    {'name': 'Dave', 'skills': ['dev']},
]

# Déduction automatique des ressources disponibles par compétence
resources = {}
for emp in employees:
    for skill in emp['skills']:
        resources[skill] = resources.get(skill, 0) + 1

# ----------- FONCTIONS DE PRIORITÉ -------------

def prio_shortest(task):
    # Priorité basée sur la durée de la tâche (Shortest Processing Time)
    return tasks[task][0]

def prio_longest(task):
    # Priorité basée sur la durée de la tâche (Longest Processing Time)
    return -tasks[task][0]

def prio_most_successors(task):
    # Priorité basée sur le nombre de successeurs (tâches qui dépendent de celle-ci)
    return -sum(1 for t in tasks if task in tasks[t][2])

def prio_most_important(task):
    # Priorité basée sur l'importance de la tâche
    # (plus l'importance est élevée, plus la tâche est prioritaire)
    return -tasks[task][3]

priorities = {
    'shortest': prio_shortest,
    'longest': prio_longest,
    'most_successors': prio_most_successors,
    'important': prio_most_important,
}

# ----------- ALGORITHME PARALLÈLE -------------

def schedule_parallel(prio_func):
    time_now = 0
    schedule = []
    finished = set()
    running = []
    remaining = set(tasks.keys())
    skill_usage = {k: 0 for k in resources}

    while remaining or running:
        for t, end in running[:]:
            if end <= time_now:
                running.remove((t, end))
                finished.add(t)
                for skill, count in tasks[t][1].items():
                    skill_usage[skill] -= count

        ready = [t for t in remaining if all(p in finished for p in tasks[t][2])]
        ready.sort(key=prio_func)

        for t in ready:
            skill_req = tasks[t][1]
            if all(skill_usage[s] + skill_req[s] <= resources[s] for s in skill_req):
                for s in skill_req:
                    skill_usage[s] += skill_req[s]
                start = time_now
                end = start + tasks[t][0]
                schedule.append((t, start, end))
                running.append((t, end))
                remaining.remove(t)

        if running:
            time_now = min(end for _, end in running)
        elif remaining:
            time_now += 1  # Avancer le temps s'il y a un blocage

    makespan = max(e for _, _, e in schedule) if schedule else 0
    return schedule, makespan

# ----------- ALGORITHME EN SÉRIE -------------

def schedule_series(prio_func):
    schedule = []
    finished = set()
    remaining = set(tasks.keys())
    current_time = 0

    while remaining:
        ready = [t for t in remaining if all(p in finished for p in tasks[t][2])]
        if not ready:
            raise RuntimeError("Cycle détecté ou tâche bloquée")
        ready.sort(key=prio_func)
        t = ready[0]
        dur = tasks[t][0]

        start = current_time
        end = start + dur
        schedule.append((t, start, end))
        finished.add(t)
        remaining.remove(t)
        current_time = end

    makespan = max(e for _, _, e in schedule) if schedule else 0
    return schedule, makespan

# ----------- GRAPHIQUE DE GANTT -------------

def plot_gantt(schedule, ax, title):
    task_names = sorted(set(t for t, _, _ in schedule))
    task_pos = {t: i for i, t in enumerate(task_names)}

    for t, start, end in schedule:
        ax.barh(task_pos[t], end-start, left=start, height=0.4)
        ax.text(start + (end-start)/2, task_pos[t], t, va='center', ha='center', color='white', fontsize=9)

    ax.set_yticks(list(task_pos.values()))
    ax.set_yticklabels(task_names)
    ax.set_xlabel('Temps')
    ax.set_title(title)
    ax.invert_yaxis()

# ----------- EXÉCUTION DES TESTS -------------

def run_all():
    results = []
    schedules_for_gantt = []

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
            schedules_for_gantt.append((sched, f"{algo_type.capitalize()} - {prio_name}"))
            print(f"[{algo_type} - {prio_name}] Makespan: {mksp}, Durée: {duration:.4f}s")

    df = pd.DataFrame(results)
    df.to_csv('../../figures/comparison_ms_rcpsp.csv', index=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='priority', y='makespan', hue='algo')
    plt.title("Makespan selon algorithme et priorité")
    plt.savefig("../../figures/makespan_comparison.png")
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='priority', y='duration_sec', hue='algo')
    plt.title("Durée d'exécution selon algorithme et priorité")
    plt.savefig("../../figures/duration_comparison.png")
    plt.show()

    fig, axs = plt.subplots(4, 2, figsize=(20, 16), sharex=True)
    for ax, (sched, title) in zip(axs.flatten(), schedules_for_gantt):
        plot_gantt(sched, ax, title)
    plt.tight_layout()
    plt.savefig("../../figures/gantt_schedules.png")
    plt.show()

# ----------- LANCEMENT -------------
if __name__ == "__main__":
    run_all()
