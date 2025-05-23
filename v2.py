import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------- DÉFINITION DES DONNÉES ------------

tasks = {
    'A': (4, ['dev'], [], 10),
    'B': (3, ['dev'], ['A'], 8),
    'C': (2, ['test'], ['A'], 6),
    'D': (5, ['dev', 'test'], ['B', 'C'], 9),
    'E': (3, ['dev'], ['C'], 5),
}

resources = {'dev': 2, 'test': 1}

# ----------- PRIORITÉS -------------

def prio_shortest(task):
    return tasks[task][0]

def prio_longest(task):
    return -tasks[task][0]

def prio_most_successors(task):
    return -sum(1 for t in tasks if task in tasks[t][2])

def prio_most_important(task):
    return -tasks[task][3]

priorities = {
    'shortest': prio_shortest,
    'longest': prio_longest,
    'most_successors': prio_most_successors,
    'important': prio_most_important,
}

# ----------- ALGORITHMES -------------

def schedule_parallel(prio_func):
    time_now = 0
    schedule = []
    finished = set()
    running = []
    remaining = set(tasks.keys())
    skill_usage = {k: 0 for k in resources}

    while remaining or running:
        # Libérer ressources
        for t, end in running[:]:
            if end <= time_now:
                running.remove((t, end))
                finished.add(t)
                for skill in tasks[t][1]:
                    skill_usage[skill] -= 1

        # Tâches prêtes
        ready = [t for t in remaining if all(p in finished for p in tasks[t][2])]
        ready.sort(key=prio_func)

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
            break

    makespan = max(e for _, _, e in schedule) if schedule else 0
    return schedule, makespan

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

        # On suppose qu'on a au moins 1 ressource pour chaque compétence
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
    # Ordonner tâches pour l'affichage
    task_names = sorted(set(t for t,_,_ in schedule))
    task_pos = {t:i for i,t in enumerate(task_names)}

    for t, start, end in schedule:
        ax.barh(task_pos[t], end-start, left=start, height=0.4)
        ax.text(start + (end-start)/2, task_pos[t], t, va='center', ha='center', color='white', fontsize=9)

    ax.set_yticks(list(task_pos.values()))
    ax.set_yticklabels(task_names)
    ax.set_xlabel('Temps')
    ax.set_title(title)
    ax.invert_yaxis()  # Tâche A en haut

# ----------- EXÉCUTION ET COMPARAISON -------------

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

    # CSV
    df = pd.DataFrame(results)
    df.to_csv('src/comparison_ms_rcpsp.csv', index=False)

    # Graphiques comparaison
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

    # Affichage Gantt : 2 colonnes, 4 lignes = 8 graphiques
    fig, axs = plt.subplots(4, 2, figsize=(12, 14), sharex=True)
    for ax, (sched, title) in zip(axs.flatten(), schedules_for_gantt):
        plot_gantt(sched, ax, title)
    plt.tight_layout()
    plt.savefig("src/gantt_schedules.png")
    plt.show()

if __name__ == "__main__":
    run_all()
