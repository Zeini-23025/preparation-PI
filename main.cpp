#include <iostream>
#include <vector>
#include <map>
#include <set>
#include <tuple>
#include <algorithm>
#include <chrono>

using namespace std;
using namespace std::chrono;

struct Task {
    int duration;
    vector<string> skills;
    vector<string> predecessors;
    int importance;
};

map<string, Task> tasks = {
    {"A", {4, {"dev"}, {}, 10}},
    {"B", {3, {"dev"}, {"A"}, 8}},
    {"C", {2, {"test"}, {"A"}, 6}},
    {"D", {5, {"dev", "test"}, {"B", "C"}, 9}},
    {"E", {3, {"dev"}, {"C"}, 5}},
};

map<string, int> resources = {{"dev", 2}, {"test", 1}};

// Fonctions de priorité
int prio_shortest(const string& t) { return tasks[t].duration; }
int prio_longest(const string& t) { return -tasks[t].duration; }

int prio_most_successors(const string& t) {
    int count = 0;
    for (const auto& [id, task] : tasks) {
        if (find(task.predecessors.begin(), task.predecessors.end(), t) != task.predecessors.end()) {
            count++;
        }
    }
    return -count;
}

int prio_most_important(const string& t) {
    return -tasks[t].importance;
}

typedef int (*PrioFunc)(const string&);

// Ordonnancement parallèle
pair<vector<tuple<string, int, int>>, int> schedule_parallel(PrioFunc prio_func) {
    int time_now = 0;
    vector<tuple<string, int, int>> schedule;
    set<string> finished, remaining;
    vector<pair<string, int>> running;
    map<string, int> skill_usage;

    for (auto& [k, v] : resources) skill_usage[k] = 0;
    for (auto& [k, _] : tasks) remaining.insert(k);

    while (!remaining.empty() || !running.empty()) {
        for (auto it = running.begin(); it != running.end(); ) {
            if (it->second <= time_now) {
                string t = it->first;
                for (auto& s : tasks[t].skills) {
                    skill_usage[s]--;
                }
                finished.insert(t);
                it = running.erase(it);
            } else ++it;
        }

        vector<string> ready;
        for (const auto& t : remaining) {
            bool all_done = true;
            for (const auto& p : tasks[t].predecessors) {
                if (finished.find(p) == finished.end()) {
                    all_done = false;
                    break;
                }
            }
            if (all_done) ready.push_back(t);
        }

        sort(ready.begin(), ready.end(), [&](const string& a, const string& b) {
            return prio_func(a) < prio_func(b);
        });

        for (const auto& t : ready) {
            bool can_start = true;
            for (auto& s : tasks[t].skills) {
                if (skill_usage[s] >= resources[s]) {
                    can_start = false;
                    break;
                }
            }
            if (can_start) {
                for (auto& s : tasks[t].skills) skill_usage[s]++;
                int start = time_now;
                int end = start + tasks[t].duration;
                schedule.emplace_back(t, start, end);
                running.emplace_back(t, end);
                remaining.erase(t);
            }
        }

        if (!running.empty()) {
            int next_time = running[0].second;
            for (auto& [_, end] : running) {
                next_time = min(next_time, end);
            }
            time_now = next_time;
        }
    }

    int makespan = 0;
    for (const auto& entry : schedule) {
        makespan = max(makespan, get<2>(entry));
    }
    return {schedule, makespan};
}

// Ordonnancement en série
pair<vector<tuple<string, int, int>>, int> schedule_series(PrioFunc prio_func) {
    int current_time = 0;
    vector<tuple<string, int, int>> schedule;
    set<string> finished, remaining;
    for (auto& [k, _] : tasks) remaining.insert(k);

    while (!remaining.empty()) {
        vector<string> ready;
        for (const auto& t : remaining) {
            bool all_done = true;
            for (const auto& p : tasks[t].predecessors) {
                if (finished.find(p) == finished.end()) {
                    all_done = false;
                    break;
                }
            }
            if (all_done) ready.push_back(t);
        }

        if (ready.empty()) {
            cerr << "Erreur: cycle ou précédence invalide" << endl;
            exit(1);
        }

        sort(ready.begin(), ready.end(), [&](const string& a, const string& b) {
            return prio_func(a) < prio_func(b);
        });

        string t = ready[0];
        int start = current_time;
        int end = start + tasks[t].duration;
        schedule.emplace_back(t, start, end);
        finished.insert(t);
        remaining.erase(t);
        current_time = end;
    }

    return {schedule, current_time};
}

// Affichage détaillé du planning
void afficher_schedule(const vector<tuple<string, int, int>>& schedule) {
    for (const auto& [task, start, end] : schedule) {
        cout << " - " << task << " -> start: " << start << ", end: " << end << endl;
    }
}

// Exécution complète
void run_all() {
    vector<pair<string, PrioFunc>> prios = {
        {"shortest", prio_shortest},
        {"longest", prio_longest},
        {"most_successors", prio_most_successors},
        {"important", prio_most_important},
    };

    for (auto& [algo_name, algo] : vector<pair<string, decltype(&schedule_series)>>{
            {"series", schedule_series},
            {"parallel", schedule_parallel}}) {

        for (auto& [prio_name, prio_func] : prios) {
            auto start_time = high_resolution_clock::now();
            auto [sched, makespan] = algo(prio_func);
            auto end_time = high_resolution_clock::now();
            auto duration = duration_cast<microseconds>(end_time - start_time).count();

            cout << "\n[" << algo_name << " - " << prio_name << "] "
                 << "Makespan: " << makespan
                 << ", Temps: " << duration << " µs" << endl;

            afficher_schedule(sched);
        }
    }
}

// Main
int main() {
    run_all();
    return 0;
}
