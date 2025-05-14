#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

using namespace std;

struct Task {
    string name;
    int duration;
    int resource;
    int cost_per_unit;
    vector<string> predecessors;
    int start_time = -1;
    int end_time = -1;
};

bool all_predecessors_done(const Task& task, const vector<string>& done) {
    for (const string& p : task.predecessors) {
        if (find(done.begin(), done.end(), p) == done.end())
            return false;
    }
    return true;
}

int main() {
    vector<Task> tasks = {
        {"A1", 3, 2, 5, {}},
        {"A2", 2, 3, 4, {"A1"}},
        {"A3", 4, 2, 3, {"A1"}}
    };

    int time = 0;
    int max_resource = 4;
    vector<string> scheduled_names;
    vector<Task*> scheduled;

    while (scheduled.size() < tasks.size()) {
        vector<Task*> available;
        for (Task& task : tasks) {
            if (task.start_time == -1 && all_predecessors_done(task, scheduled_names)) {
                available.push_back(&task);
            }
        }

        sort(available.begin(), available.end(), [](Task* a, Task* b) {
            return a->cost_per_unit < b->cost_per_unit;
        });

        for (Task* task : available) {
            if (task->resource <= max_resource) {
                task->start_time = time;
                task->end_time = time + task->duration;
                scheduled.push_back(task);
                scheduled_names.push_back(task->name);
                time = task->end_time;
                break;
            }
        }
    }

    int makespan = 0, total_cost = 0;
    for (Task* t : scheduled) {
        makespan = max(makespan, t->end_time);
        total_cost += t->duration * t->cost_per_unit;
    }

    cout << "Durée totale (makespan) : " << makespan << endl;
    cout << "Coût total : " << total_cost << endl;
    for (Task* t : scheduled) {
        cout << t->name << " : " << t->start_time << " → " << t->end_time << endl;
    }

    return 0;
}
