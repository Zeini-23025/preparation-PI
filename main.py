import matplotlib.pyplot as plt

# definition d une tâche
class Task:
    def __init__(self, name, duration, resource, cost_per_unit, predecessors=[]):
        self.name = name
        self.duration = duration
        self.resource = resource
        self.cost_per_unit = cost_per_unit
        self.predecessors = predecessors
        self.start_time = None
        self.end_time = None

def schedule_tasks(tasks, max_resource):
    time = 0
    scheduled = []
    ongoing = []

    while len(scheduled) < len(tasks):
        available_tasks = [t for t in tasks if t not in scheduled and
                           all(p in [s.name for s in scheduled] for p in t.predecessors)]
        available_tasks.sort(key=lambda x: x.cost_per_unit) 

        for task in available_tasks:
            if task.resource <= max_resource:
                task.start_time = time
                task.end_time = time + task.duration
                scheduled.append(task)
                time = task.end_time
                break

    makespan = max(t.end_time for t in scheduled)
    total_cost = sum(t.duration * t.cost_per_unit for t in scheduled)

    return scheduled, makespan, total_cost

def draw_gantt_chart(tasks):
    fig, gnt = plt.subplots()
    gnt.set_title("Diagramme de Gantt - Ordonnancement MC-RCPSP")
    gnt.set_xlabel("Temps")
    gnt.set_ylabel("Tâches")

    gnt.set_yticks(range(10, 10 * len(tasks) + 1, 10))
    gnt.set_yticklabels([task.name for task in tasks])
    gnt.grid(True)

    for i, task in enumerate(tasks):
        gnt.broken_barh([(task.start_time, task.duration)], (10 * i, 9),
                        facecolors=('tab:blue'))

    plt.tight_layout()
    plt.show()

# Exemple
tasks = [
    Task("A1", 3, 2, 5),
    Task("A2", 2, 3, 4, ["A1"]),
    Task("A3", 4, 2, 3, ["A1"]),
]

scheduled, makespan, cost = schedule_tasks(tasks, max_resource=4)

print(f"Durée totale (makespan) : {makespan}")
print(f"Coût total : {cost}")
for task in scheduled:
    print(f"{task.name} : {task.start_time} → {task.end_time}")

draw_gantt_chart(scheduled)
