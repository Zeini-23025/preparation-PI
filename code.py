class Task:
    def __init__(self, name, duration, resource, cost, predecessors=[]):
        self.name = name            # Le nom de la tâche
        self.duration = duration    # La durée de la tâche
        self.resource = resource    # Les ressources nécessaires pour la tâche
        self.cost = cost            # Le coût de la tâche par unité de temps
        self.predecessors = predecessors  # Les prédécesseurs de la tâche
        self.start = None           # Le temps de début de la tâche
        self.end = None             # Le temps de fin de la tâche

def schedule(tasks, max_resource):
    time = 0                      # Temps initial
    scheduled = []                # Liste des tâches planifiées

    while len(scheduled) < len(tasks):  # Tant que toutes les tâches ne sont pas planifiées
        # Sélection des tâches prêtes à être planifiées (tâches sans prédécesseurs non planifiés)
        ready = [t for t in tasks if t not in scheduled and all(p in [s.name for s in scheduled] for p in t.predecessors)]
        
        # Tri des tâches prêtes en fonction du coût (priorité aux tâches les moins chères)
        ready.sort(key=lambda x: x.cost)

        for t in ready:
            # Si la tâche peut être exécutée avec les ressources disponibles
            if t.resource <= max_resource:
                t.start = time  # La tâche commence au temps actuel
                t.end = time + t.duration  # La tâche se termine après sa durée
                scheduled.append(t)  # Ajouter la tâche à la liste des tâches planifiées
                time = t.end  # Mettre à jour le temps courant
                break

    # Calcul du makespan (durée totale) et du coût total
    makespan = max(t.end for t in scheduled)
    total_cost = sum(t.cost * t.duration for t in scheduled)

    return makespan, total_cost

# Exemple d'utilisation
tasks = [
    Task("A1", 3, 2, 5),
    Task("A2", 2, 3, 4, ["A1"]),
    Task("A3", 4, 2, 3, ["A1"])
]

makespan, total_cost = schedule(tasks, max_resource=4)
print(f"Durée totale (makespan) : {makespan}")
print(f"Coût total : {total_cost}")

# Affichage des détails des tâches
for task in tasks:
    print(f"{task.name}: Start at {task.start}, End at {task.end}")
