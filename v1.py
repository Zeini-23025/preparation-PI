import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------- DÉFINITION DES DONNÉES ------------

# Exemple de tâches
# task_id: (durée, [compétences nécessaires], [prédécesseurs], importance)
tasks = {
    'A': (4, ['dev'], [], 10),
    'B': (3, ['dev'], ['A'], 8),
    'C': (2, ['test'], ['A'], 6),
    'D': (5, ['dev', 'test'], ['B', 'C'], 9),
    'E': (3, ['dev'], ['C'], 5),
}

# Ressources disponibles : compétences et nombre de ressources par compétence
resources = {'dev': 2, 'test': 1}

# ----------- PRIORITÉS -------------

def prio_shortest(task):      # Durée la plus courte (SPT)
    return tasks[task][0]

def prio_longest(task):       # Durée la plus longue (LPT)
    return -tasks[task][0]

def prio_most_successors(task):
    # Nombre de successeurs directs
    return -sum(1 for t in tasks if task in tasks[t][2])

def prio_most_important(task):
    # Importance / poids
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
        # Libérer les ressources des tâches terminées
        for t, end in running[:]:
            if end <= time_now:
                running.remove((t, end))
                finished.add(t)
                for skill in tasks[t][1]:
                    skill_usage[skill] -= 1

        # Identifier les tâches prêtes
        ready = [t for t in remaining if all(p in finished for p in tasks[t][2])]

        # Trier selon la priorité
        ready.sort(key=prio_func)

        # Démarrer les tâches prêtes si ressources dispo
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

        if running:
            time_now = min(end for _, end in running)
        else:
            # Aucune tâche en cours et aucune prête
            break

    makespan = max(e for _, _, e in schedule) if schedule else 0
    return schedule, makespan

# ----------- ALGORITHME SÉRIE -------------

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

        # Vérifier ressources pour cette tâche (1 tâche à la fois)
        if all(resources[s] >= 1 for s in skills):
            start = current_time
            end = start + dur
            schedule.append((t, start, end))
            finished.add(t)
            remaining.remove(t)
            current_time = end
        else:
            # Attente si ressources pas dispo (rare en série)
            current_time += 1

    makespan = max(e for _, _, e in schedule) if schedule else 0
    return schedule, makespan

# ----------- EXÉCUTION ET COMPARAISON -------------

def run_all():
    results = []
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
            print(f"[{algo_type} - {prio_name}] Makespan: {mksp}, Durée: {duration:.4f}s")

    # Enregistrer dans CSV
    df = pd.DataFrame(results)
    df.to_csv('src/comparison_ms_rcpsp.csv', index=False)

    # Graphiques
    plt.figure(figsize=(10,6))
    sns.barplot(data=df, x='priority', y='makespan', hue='algo')
    plt.title("Makespan selon algorithme et priorité")
    plt.savefig("src/makespan_comparison.png")
    plt.show()

    plt.figure(figsize=(10,6))
    sns.barplot(data=df, x='priority', y='duration_sec', hue='algo')
    plt.title("Durée d'exécution selon algorithme et priorité")
    plt.savefig("src/duration_comparison.png")
    plt.show()

if __name__ == "__main__":
    run_all()
