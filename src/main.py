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

# Exemples
tasks = [
    Task("A1", 3, 2, 5),
    Task("A2", 2, 3, 4, ["A1"]),
    Task("A3", 4, 2, 3, ["A1"]),
]


tasks4 = [
    Task("T1", 2, 2, 10),
    Task("T2", 1, 1, 5),
    Task("T3", 3, 2, 8, ["T1"]),
    Task("T4", 2, 2, 6, ["T1"]),
    Task("T5", 4, 1, 7, ["T2", "T3"]),
    Task("T6", 2, 2, 4, ["T4"]),
    Task("T7", 1, 1, 3, ["T5", "T6"]),
]

tasks20 = [
    Task("T1", 2, 1, 10),
    Task("T2", 3, 2, 8),
    Task("T3", 1, 1, 6, ["T1"]),
    Task("T4", 2, 2, 7, ["T1"]),
    Task("T5", 4, 2, 5, ["T2"]),
    Task("T6", 1, 1, 9, ["T3", "T4"]),
    Task("T7", 2, 3, 6, ["T5"]),
    Task("T8", 3, 2, 4),
    Task("T9", 1, 1, 7, ["T6"]),
    Task("T10", 2, 1, 6, ["T6"]),
    Task("T11", 2, 2, 5, ["T7"]),
    Task("T12", 3, 1, 4),
    Task("T13", 2, 2, 5, ["T11"]),
    Task("T14", 1, 1, 6, ["T12"]),
    Task("T15", 2, 2, 8, ["T13", "T14"]),
    Task("T16", 3, 3, 6),
    Task("T17", 1, 1, 7, ["T9", "T10"]),
    Task("T18", 2, 2, 6, ["T15"]),
    Task("T19", 3, 2, 5, ["T17"]),
    Task("T20", 1, 1, 9, ["T18", "T19"]),
]

tasks30 = [
    Task("T1", 2, 2, 9),
    Task("T2", 3, 1, 8),
    Task("T3", 1, 1, 7),
    Task("T4", 2, 2, 6, ["T1"]),
    Task("T5", 3, 1, 5, ["T1", "T2"]),
    Task("T6", 2, 2, 4, ["T2"]),
    Task("T7", 1, 1, 3, ["T3"]),
    Task("T8", 3, 2, 6, ["T4"]),
    Task("T9", 2, 3, 5, ["T5"]),
    Task("T10", 1, 1, 4, ["T6"]),
    Task("T11", 2, 2, 3, ["T7"]),
    Task("T12", 3, 1, 6, ["T8"]),
    Task("T13", 2, 2, 5, ["T9"]),
    Task("T14", 1, 1, 4, ["T10"]),
    Task("T15", 2, 3, 3, ["T11"]),
    Task("T16", 3, 2, 6, ["T12"]),
    Task("T17", 1, 1, 5, ["T13"]),
    Task("T18", 2, 1, 4, ["T14", "T15"]),
    Task("T19", 1, 2, 3, ["T16"]),
    Task("T20", 2, 1, 6, ["T17"]),
    Task("T21", 3, 2, 5, ["T18"]),
    Task("T22", 1, 1, 4, ["T19"]),
    Task("T23", 2, 2, 3, ["T20"]),
    Task("T24", 1, 1, 2, ["T21"]),
    Task("T25", 2, 2, 6, ["T22"]),
    Task("T26", 1, 1, 5, ["T23"]),
    Task("T27", 2, 2, 4, ["T24"]),
    Task("T28", 1, 1, 3, ["T25"]),
    Task("T29", 2, 3, 2, ["T26", "T27"]),
    Task("T30", 3, 2, 1, ["T28", "T29"]),
]



scheduled, makespan, cost = schedule_tasks(tasks, max_resource=4)

print(f"Durée totale (makespan) : {makespan}")
print(f"Coût total : {cost}")
for task in scheduled:
    print(f"{task.name} : {task.start_time} → {task.end_time}")

draw_gantt_chart(scheduled)

