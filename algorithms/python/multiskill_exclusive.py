#             ------------------ employés multiskills MAIS 1 skill/tâche max ---------------
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------- DÉFINITION DES DONNÉES ------------

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

employees = [
    {'name': 'Zeiny', 'skills': ['dev', 'test']},
    {'name': 'Nezihe', 'skills': ['dev']},
    {'name': 'Mli7a', 'skills': ['test']},
    {'name': 'Zeyd', 'skills': ['dev']},
]

# Ressources disponibles
resources = {}
for emp in employees:
    for skill in emp['skills']:
        resources[skill] = resources.get(skill, 0) + 1

# ----------- PRIORITÉS -------------


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

# ----------- AFFECTATION DES EMPLOYÉS (selon compétence) -------------


def assign_employees(task_skills, busy_emps):
    assigned = {}
    available = [e for e in employees if e['name'] not in busy_emps]

    for skill, needed in task_skills.items():
        assigned[skill] = []
        candidates = [e for e in available if skill in e['skills']]
        for c in candidates:
            # Vérifie que cet employé n'est pas déjà affecté à une compétence dans cette tâche
            if len(assigned[skill]) < needed and c['name'] not in sum(assigned.values(), []):
                assigned[skill].append(c['name'])

    if all(len(assigned[s]) >= task_skills[s] for s in task_skills):
        return assigned
    return None  # Pas assez d'employés disponibles

# ----------- ALGO PARALLÈLE -------------


def schedule_parallel(prio_func):
    time_now = 0
    schedule = []
    finished = set()
    running = []
    remaining = set(tasks.keys())

    while remaining or running:
        # Libération des tâches terminées
        for t, end, emp_used in running[:]:
            if end <= time_now:
                running.remove((t, end, emp_used))
                finished.add(t)

        # Employés occupés à ce moment
        busy_emps = set(e for _, _, emp in running for e in sum(emp.values(), []))

        # Tâches prêtes
        ready = [t for t in remaining if all(p in finished for p in tasks[t][2])]
        ready.sort(key=prio_func)

        for t in ready:
            dur, skills, _, _ = tasks[t]
            assigned = assign_employees(skills, busy_emps)
            if assigned:
                print(f"Tâche '{t}' démarrée à {time_now} avec affectation : {assigned}")
                schedule.append((t, time_now, time_now + dur, assigned))
                running.append((t, time_now + dur, assigned))
                busy_emps.update(sum(assigned.values(), []))
                remaining.remove(t)

        if running:
            time_now = min(end for _, end, _ in running)
        elif remaining:
            time_now += 1

    makespan = max(e for _, _, e, _ in schedule) if schedule else 0
    return schedule, makespan

# ----------- ALGO SÉRIE -------------


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

        # Affectation simple pour séries (pas de conflits car séquentiel)
        assigned = assign_employees(tasks[t][1], [])
        schedule.append((t, current_time, current_time + dur, assigned))
        finished.add(t)
        remaining.remove(t)
        current_time += dur

    makespan = max(e for _, _, e, _ in schedule) if schedule else 0
    return schedule, makespan

# ----------- GRAPHIQUE GANTT -------------


def plot_gantt(schedule, ax, title):
    task_names = sorted(set(t for t, _, _, _ in schedule))
    task_pos = {t: i for i, t in enumerate(task_names)}

    for t, start, end, _ in schedule:
        ax.barh(task_pos[t], end - start, left=start, height=0.4)
        ax.text((start + end) / 2, task_pos[t], t, va='center', ha='center', color='white', fontsize=9)

    ax.set_yticks(list(task_pos.values()))
    ax.set_yticklabels(task_names)
    ax.set_xlabel('Temps')
    ax.set_title(title)
    ax.invert_yaxis()

# ----------- VÉRIFICATION QUE UN EMPLOYÉ N'A QU'UNE COMPÉTENCE PAR TÂCHE -------------


def verify_single_skill_per_employee(schedule):
    for t, start, end, assigned in schedule:
        emp_skills = {}
        for skill, emps in assigned.items():
            for emp in emps:
                if emp in emp_skills:
                    print(f"⚠️ Violation: L'employé {emp} affecté à plusieurs compétences dans la tâche '{t}'")
                emp_skills[emp] = skill
    print("Vérification terminée.")

# ----------- EXÉCUTION -------------


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
            # Vérifier la contrainte
            verify_single_skill_per_employee(sched)

    df = pd.DataFrame(results)
    df.to_csv('figures/comparison_ms_rcpsp.csv', index=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='priority', y='makespan', hue='algo')
    plt.title("Makespan selon algorithme et priorité")
    plt.savefig("figures/makespan_comparison.png")
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x='priority', y='duration_sec', hue='algo')
    plt.title("Durée d'exécution selon algorithme et priorité")
    plt.savefig("figures/duration_comparison.png")
    plt.show()

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


# ----------- LANCEMENT -------------

if __name__ == "__main__":
    run_all()
