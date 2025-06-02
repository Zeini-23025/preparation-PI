#include <iostream>
#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <string>
#include <algorithm>
#include <functional>
#include <set>
#include <map>
#include <optional>

using namespace std;

// Structures
struct Task {
    string name;
    int duration;
    unordered_map<string, int> requiredSkills;
    vector<string> prerequisites;
    int importance;
};

struct Employee {
    string name;
    unordered_set<string> skills;
};

struct ScheduledTask {
    string task;
    int start;
    int end;
    map<string, vector<string>> assignedEmployees;
};

// Données
unordered_map<string, Task> tasks = {
    {"users", { "users", 3, {{"dev", 1}}, {}, 10 }},
    {"assureurs", { "assureurs", 2, {{"dev", 1}}, {}, 8 }},
    {"offres", { "offres", 4, {{"dev", 2}}, {"users", "assureurs"}, 6 }},
    {"contrats", { "contrats", 5, {{"dev", 2}, {"test", 1}}, {"offres"}, 9 }},
    {"paiement", { "paiement", 3, {{"dev", 1}, {"test", 1}}, {"contrats"}, 5 }},
    {"notification", { "notification", 2, {{"dev", 1}}, {"paiement", "users"}, 7 }},
    {"reclamation", { "reclamation", 4, {{"dev", 1}}, {"users", "contrats"}, 6 }},
    {"client", { "client", 3, {{"dev", 1}}, {"users"}, 5 }},
    {"echange", { "echange", 2, {{"dev", 1}}, {"contrats"}, 4 }},
    {"document", { "document", 3, {{"dev", 2}}, {"users", "assureurs"}, 8 }},
    {"message", { "message", 2, {{"dev", 1}}, {"users", "assureurs"}, 7 }},
    {"renouvellement", { "renouvellement", 4, {{"dev", 2}}, {"users", "assureurs", "contrats"}, 9 }}
};

unordered_map<string, Employee> employees = {
    {"Zeiny", {"Zeiny", {"dev", "test"}}},
    {"Nezihe", {"Nezihe", {"dev"}}},
    {"Mli7a", {"Mli7a", {"test"}}},
    {"Zeyd", {"Zeyd", {"dev"}}}
};

// Fonctions de priorité
int prio_shortest(const string& t) { return tasks[t].duration; }
int prio_longest(const string& t) { return -tasks[t].duration; }
int prio_importance(const string& t) { return -tasks[t].importance; }
int prio_successors(const string& t) {
    int count = 0;
    for (const auto& [_, task] : tasks)
        for (const auto& pre : task.prerequisites)
            if (pre == t) count++;
    return -count;
}

// Attribution des employés
optional<map<string, vector<string>>> assignEmployees(
    const unordered_map<string, int>& required,
    const unordered_set<string>& busy) {

    map<string, vector<string>> assigned;
    unordered_map<string, int> toAssign = required;
    unordered_set<string> used;

    for (const auto& [name, emp] : employees) {
        if (busy.count(name)) continue;
        for (const auto& skill : emp.skills) {
            if (toAssign[skill] > 0 && !used.count(name)) {
                assigned[skill].push_back(name);
                toAssign[skill]--;
                used.insert(name);
                break;
            }
        }
    }

    for (const auto& [skill, n] : toAssign)
        if (n > 0) return nullopt;

    return assigned;
}

// Ordonnancement parallèle
vector<ScheduledTask> scheduleParallel(function<int(const string&)> prio) {
    vector<ScheduledTask> schedule;
    unordered_set<string> finished;
    unordered_set<string> remaining;
    for (const auto& [t, _] : tasks) remaining.insert(t);
    int time = 0;
    vector<tuple<string, int, map<string, vector<string>>>> running;

    while (!remaining.empty() || !running.empty()) {
        for (auto it = running.begin(); it != running.end(); ) {
            auto& [t, end, _] = *it;
            if (end <= time) {
                finished.insert(t);
                it = running.erase(it);
            } else ++it;
        }

        unordered_set<string> busy;
        for (const auto& [_, __, empmap] : running)
            for (const auto& [_, emps] : empmap)
                for (const auto& e : emps)
                    busy.insert(e);

        vector<string> ready;
        for (const string& t : remaining) {
            bool ok = true;
            for (const auto& p : tasks[t].prerequisites)
                if (!finished.count(p)) ok = false;
            if (ok) ready.push_back(t);
        }

        sort(ready.begin(), ready.end(), [&](const string& a, const string& b) {
            return prio(a) < prio(b);
        });

        for (const auto& t : ready) {
            auto emp = assignEmployees(tasks[t].requiredSkills, busy);
            if (emp) {
                schedule.push_back({t, time, time + tasks[t].duration, *emp});
                running.emplace_back(t, time + tasks[t].duration, *emp);
                for (const auto& [_, es] : *emp)
                    for (const auto& e : es)
                        busy.insert(e);
                remaining.erase(t);
            }
        }

        if (!running.empty()) {
            int next = std::get<1>(*min_element(running.begin(), running.end(),
                        [](const auto& a, const auto& b) {
                            return get<1>(a) < get<1>(b);
                        }));
            time = next;
        } else if (!remaining.empty()) {
            time++;
        }
    }
    return schedule;
}

// Ordonnancement série
vector<ScheduledTask> scheduleSeries(function<int(const string&)> prio) {
    vector<ScheduledTask> schedule;
    unordered_set<string> finished, remaining;
    for (const auto& [t, _] : tasks) remaining.insert(t);
    int time = 0;

    while (!remaining.empty()) {
        vector<string> ready;
        for (const string& t : remaining) {
            bool ok = true;
            for (const auto& p : tasks[t].prerequisites)
                if (!finished.count(p)) ok = false;
            if (ok) ready.push_back(t);
        }

        sort(ready.begin(), ready.end(), [&](const string& a, const string& b) {
            return prio(a) < prio(b);
        });

        string chosen = ready.front();
        auto emp = assignEmployees(tasks[chosen].requiredSkills, {});
        if (emp) {
            schedule.push_back({chosen, time, time + tasks[chosen].duration, *emp});
            time += tasks[chosen].duration;
            finished.insert(chosen);
            remaining.erase(chosen);
        } else {
            cerr << "Aucune ressource disponible pour " << chosen << endl;
            break;
        }
    }
    return schedule;
}

// Affichage
void printSchedule(const vector<ScheduledTask>& sched) {
    for (const auto& s : sched) {
        cout << "Tâche: " << s.task << " | Début: " << s.start << " | Fin: " << s.end << " | Employés: ";
        for (const auto& [skill, emps] : s.assignedEmployees) {
            cout << "[" << skill << ": ";
            for (const auto& e : emps) cout << e << " ";
            cout << "] ";
        }
        cout << endl;
    }
}

// Vérification des conflits
void verifyAssignments(const vector<ScheduledTask>& schedule) {
    for (const auto& s : schedule) {
        map<string, string> used;
        for (const auto& [skill, emps] : s.assignedEmployees) {
            for (const auto& e : emps) {
                if (used.count(e)) {
                    cout << "⚠️ Conflit: " << e << " affecté à plusieurs compétences dans '" << s.task << "'\n";
                }
                used[e] = skill;
            }
        }
    }
    cout << "✔ Vérification terminée.\n";
}

// Main
int main() {
    vector<pair<string, function<int(const string&)>>> modes = {
        {"Durée la plus courte", prio_shortest},
        {"Durée la plus longue", prio_longest},
        {"Importance", prio_importance},
        {"Successeurs", prio_successors}
    };

    for (const auto& [label, f] : modes) {
        cout << "\n===============================\n" << endl;
        cout << "Ordonnancement PARALLÈLE : " << label << endl;
        cout << "\n================================\n" << endl;
        auto res = scheduleParallel(f);
        printSchedule(res);
        verifyAssignments(res);
        cout << "\n==============================" << endl;
        cout << "\nOrdonnancement SÉRIE : " << label << endl;
        cout << "\n==============================\n" << endl;
        auto seq = scheduleSeries(f);
        printSchedule(seq);
        verifyAssignments(seq);
    }

    return 0;
}
