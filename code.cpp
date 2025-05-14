#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
using namespace std;

struct Task {
string name;
int duration, resource, cost;
vector<string> predecessors;
int start = -1, end = -1;
};

bool ready(const Task& task, const vector<string>& done) {
for (auto& p : task.predecessors)
if (find(done.begin(), done.end(), p) == done.end()) return false;
return true;
}

int main() {
vector<Task> tasks = {
{"A", 2, 2, 5, {}},
{"B", 3, 3, 4, {"A"}},
{"C", 1, 1, 3, {"A"}}
};
int time = 0, max_resource = 4;
vector<string> done;
while (done.size() < tasks.size()) {
for (Task& t : tasks) {
if (t.start == -1 && ready(t, done) && t.resource <= max_resource) {
t.start = time;
t.end = time + t.duration;
done.push_back(t.name);
time = t.end;
break;
}
}
}
return 0;
}